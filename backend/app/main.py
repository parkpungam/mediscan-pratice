import os,re,secrets,hashlib,uuid,time,asyncpg,bcrypt
from datetime import timedelta
from contextlib import asynccontextmanager
from asyncpg.exceptions import UniqueViolationError
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI,Request,Response,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
pool=None; attempts={}; WINDOW=900; _lifespan_context=None
SHORT_SESSION_SECONDS=3*60*60; LONG_SESSION_SECONDS=30*24*60*60; ABSOLUTE_SESSION_SECONDS=30*24*60*60; RESEND_COOLDOWN_SECONDS=300
ENV=os.getenv('ENVIRONMENT','development')
_DUMMY_PASSWORD_HASH=bcrypt.hashpw(b'x',bcrypt.gensalt(rounds=12))
@asynccontextmanager
async def lifespan(app):
 global pool
 pool=await asyncpg.create_pool(host=os.getenv('PGHOST','localhost'),port=int(os.getenv('PGPORT','5432')),database=os.getenv('PGDATABASE','mediscan_note'),user=os.getenv('PGUSER','postgres'),password=os.getenv('PGPASSWORD',''))
 try: yield
 finally:
  if pool: await pool.close()
app=FastAPI(lifespan=lifespan)
def dev_shortcuts_enabled(environment=None, enabled=None):
 return (ENV if environment is None else environment)=='development' and (os.getenv('ENABLE_DEV_AUTH_SHORTCUTS','false') if enabled is None else enabled)=='true'
DEV=dev_shortcuts_enabled()
app.add_middleware(CORSMiddleware,allow_origins=[os.getenv('FRONTEND_ORIGIN','http://localhost:8080')],allow_credentials=True,allow_methods=['*'],allow_headers=['Content-Type'])
email_re=re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'); symbols=r'''!@#$%^&*()\-_=+\[\]{};:'",.<>/?\\|`~'''
def norm(v): return re.sub(r'\s','',v).lower()
def sha(v): return hashlib.sha256(v.encode()).hexdigest()
def newtoken(): return secrets.token_urlsafe(32)
def session_idle_seconds(keep_signed_in): return LONG_SESSION_SECONDS if keep_signed_in else SHORT_SESSION_SECONDS
def session_expiry(now,created_at,keep_signed_in): return min(now+timedelta(seconds=session_idle_seconds(keep_signed_in)),created_at+timedelta(seconds=ABSOLUTE_SESSION_SECONDS))
def password_ok(v): return 8<=len(v)<=64 and not re.search(r'\s',v) and bool(re.search('[A-Za-z]',v) and re.search(r'\d',v) and re.search('['+symbols+']',v))
def password_matches(password,password_hash=None): return bcrypt.checkpw(password.encode(),password_hash.encode() if password_hash else _DUMMY_PASSWORD_HASH)
def limited(k,n):
 now=time.time(); a=[x for x in attempts.get(k,[]) if now-x<WINDOW]; attempts[k]=a; return len(a)>=n,max(1,int(WINDOW-(now-a[0]))) if a else WINDOW
def record(k): attempts.setdefault(k,[]).append(time.time())
def error(code,status,msg=None,headers=None):
 return Response(content='{"code":"'+code+'"'+((',"message":"'+msg+'"') if msg else '')+'}',status_code=status,media_type='application/json',headers=headers)
async def startup():
 global _lifespan_context; _lifespan_context=lifespan(app); await _lifespan_context.__aenter__()
async def shutdown():
 global _lifespan_context
 if _lifespan_context: await _lifespan_context.__aexit__(None,None,None); _lifespan_context=None
@app.exception_handler(UniqueViolationError)
async def unique_violation(request,exc):
 constraint=getattr(exc,'constraint_name',None)
 if constraint=='users_email_key': return error('EMAIL_TAKEN',409)
 if constraint=='user_profiles_nickname_key': return error('NICKNAME_TAKEN',409)
 return error('CONFLICT',409)
@app.get('/health')
async def health(): return {'status':'ok'}
@app.get('/v1/auth/email-availability')
async def email_available(email:str): return {'available':not bool(await pool.fetchval('select 1 from users where email=$1',norm(email)))}
@app.get('/v1/users/nickname-availability')
async def nickname_available(nickname:str): return {'available':not bool(await pool.fetchval('select 1 from user_profiles where nickname=$1',nickname))}
class Register(BaseModel):
 email:str; password:str; nickname:str; major:str; majorOther:str=''; signupSource:str=''; signupSourceOther:str=''; termsAccepted:bool; privacyAccepted:bool; ageConfirmed:bool; marketingAccepted:bool=False
@app.post('/v1/auth/register',status_code=201)
async def register(b:Register):
 e=norm(b.email)
 if not(email_re.match(e) and len(e)<=254 and password_ok(b.password) and b.nickname and b.major and b.termsAccepted and b.privacyAccepted and b.ageConfirmed): return error('INVALID_REGISTRATION',400)
 async with pool.acquire() as c:
  async with c.transaction():
   if await c.fetchval('select 1 from users where email=$1',e): return error('EMAIL_TAKEN',409)
   if await c.fetchval('select 1 from user_profiles where nickname=$1',b.nickname): return error('NICKNAME_TAKEN',409)
   uid=uuid.uuid4(); h=bcrypt.hashpw(b.password.encode(),bcrypt.gensalt(rounds=12)).decode(); major=b.majorOther if b.major=='기타 보건의료계열' else b.major; signup_source=b.signupSourceOther if b.signupSource=='기타' else b.signupSource
   await c.execute('insert into users(id,email,password_hash,age_14_plus_confirmed_at) values($1,$2,$3,now())',uid,e,h)
   await c.execute('insert into user_profiles(user_id,nickname,major,major_status,signup_source) values($1,$2,$3,$4,$5)',uid,b.nickname,major,b.major,signup_source or None)
   for name,required,agreed in [('terms',True,True),('privacy',True,True),('age_14_plus',True,True),('marketing',False,b.marketingAccepted)]: await c.execute('insert into user_consents(id,user_id,terms_id,terms_version,required,agreed,agreed_at) values($1,$2,$3,$4,$5,$6,case when $6 then now() end)',uuid.uuid4(),uid,name,'v1',required,agreed)
   t=newtoken(); await c.execute("insert into email_verifications(id,user_id,token_hash,expires_at) values($1,$2,$3,now()+interval '24 hours')",uuid.uuid4(),uid,sha(t)); return {'status':'verification_pending',**({'developmentToken':t} if DEV else {})}
class Token(BaseModel): token:str
@app.post('/v1/auth/verify-email')
async def verify(b:Token):
 async with pool.acquire() as c:
  row=await c.fetchrow('select id,user_id from email_verifications where token_hash=$1 and used_at is null and expires_at>now()',sha(b.token))
  if not row:return error('INVALID_OR_EXPIRED_TOKEN',400)
  await c.execute('update email_verifications set used_at=now() where id=$1',row['id']); await c.execute('update users set email_verified_at=now() where id=$1',row['user_id']); return {'status':'verified'}
class Email(BaseModel): email:str
@app.post('/v1/auth/resend-verification')
async def resend(b:Email):
 async with pool.acquire() as c:
  u=await c.fetchrow('select id,email_verified_at from users where email=$1',norm(b.email))
  if not u or u['email_verified_at']: return {'status':'verification_pending'}
  last_sent=await c.fetchval('select max(created_at) from email_verifications where user_id=$1',u['id'])
  if last_sent:
   elapsed=await c.fetchval('select extract(epoch from now()-$1::timestamptz)',last_sent)
   if elapsed < RESEND_COOLDOWN_SECONDS:
    retry=max(1,int(RESEND_COOLDOWN_SECONDS-elapsed)); return error('RESEND_COOLDOWN',429,'인증 메일은 5분 후에 다시 요청할 수 있습니다.',{'Retry-After':str(retry)})
  await c.execute('update email_verifications set used_at=now() where user_id=$1 and used_at is null',u['id'])
  t=newtoken()
  await c.execute("insert into email_verifications(id,user_id,token_hash,expires_at) values($1,$2,$3,now()+interval '24 hours')",uuid.uuid4(),u['id'],sha(t))
  return {'status':'verification_pending',**({'developmentToken':t} if DEV else {})}
class Login(BaseModel): email:str; password:str; keepSignedIn:bool=False
@app.post('/v1/auth/login')
async def login(b:Login,request:Request,response:Response):
 e=norm(b.email); ip=request.client.host; be,retry1=limited('e:'+e,10); bi,retry2=limited('i:'+ip,20)
 if be or bi:return error('TOO_MANY_LOGIN_ATTEMPTS',429,'너무 많은 로그인 시도가 있었습니다. 잠시 후 다시 시도해 주세요.',{'Retry-After':str(max(retry1,retry2))})
 async with pool.acquire() as c:
  row=await c.fetchrow('select u.id,u.email,u.password_hash,u.email_verified_at,p.nickname from users u join user_profiles p on p.user_id=u.id where u.email=$1',e)
  if not password_matches(b.password,row['password_hash'] if row else None): record('e:'+e);record('i:'+ip);return error('INVALID_CREDENTIALS',401,'이메일 또는 비밀번호가 올바르지 않습니다.')
  attempts.pop('e:'+e,None);attempts.pop('i:'+ip,None);t=newtoken();idle=session_idle_seconds(b.keepSignedIn);await c.execute("insert into auth_sessions(id,user_id,token_hash,expires_at,keep_signed_in) values($1,$2,$3,now()+($4 * interval '1 second'),$5)",uuid.uuid4(),row['id'],sha(t),idle,b.keepSignedIn);response.set_cookie('msn_session',t,httponly=True,samesite='lax',secure=ENV!='development',max_age=idle);return {'user':{'email':row['email'],'nickname':row['nickname'],'emailVerified':bool(row['email_verified_at'])}}
async def session(request:Request):
 t=request.cookies.get('msn_session');
 if not t:return None
 async with pool.acquire() as c:
  row=await c.fetchrow("select s.id,s.keep_signed_in,u.id as user_id,u.email,u.email_verified_at,p.nickname from auth_sessions s join users u on u.id=s.user_id join user_profiles p on p.user_id=u.id where s.token_hash=$1 and s.expires_at>now() and s.created_at+interval '30 days'>now()",sha(t))
  if not row:return None
  await c.execute("update auth_sessions set expires_at=least(now()+($2 * interval '1 second'),created_at+interval '30 days') where id=$1",row['id'],session_idle_seconds(row['keep_signed_in']))
  return row
@app.post('/v1/auth/logout',status_code=204)
async def logout(request:Request,response:Response):
 t=request.cookies.get('msn_session');
 if t: await pool.execute('delete from auth_sessions where token_hash=$1',sha(t))
 return Response(status_code=204,headers={'Set-Cookie':'msn_session=; Max-Age=0; Path=/; HttpOnly; SameSite=Lax'})
@app.get('/v1/users/me')
async def me(request:Request):
 u=await session(request)
 if not u:return error('UNAUTHENTICATED',401)
 return {'email':u['email'],'nickname':u['nickname'],'emailVerified':bool(u['email_verified_at'])}
