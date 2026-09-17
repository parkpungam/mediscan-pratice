import asyncio,os,uuid,bcrypt,asyncpg
from dotenv import load_dotenv
load_dotenv('.env')
if os.getenv('ENVIRONMENT','development')!='development' or os.getenv('ENABLE_DEV_AUTH_SHORTCUTS','false')!='true': raise SystemExit('development shortcuts must be explicitly enabled')
password=os.getenv('DEV_TEST_PASSWORD')
if not password: raise SystemExit('DEV_TEST_PASSWORD is required')
async def run():
 c=await asyncpg.connect(host=os.environ['PGHOST'],port=int(os.environ['PGPORT']),database=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])
 try:
  email=os.getenv('DEV_TEST_EMAIL','test@example.local'); row=await c.fetchrow('select id from users where email=$1',email)
  if not row:
   uid=uuid.uuid4(); h=bcrypt.hashpw(password.encode(),bcrypt.gensalt(rounds=12)).decode(); await c.execute('insert into users(id,email,password_hash,age_14_plus_confirmed_at,email_verified_at) values($1,$2,$3,now(),now())',uid,email,h); await c.execute('insert into user_profiles(user_id,nickname,major,major_status) values($1,$2,$3,$4)',uid,'devtester','nonmajor','seed')
  else: await c.execute('update users set email_verified_at=coalesce(email_verified_at,now()) where id=$1',row['id'])
 finally: await c.close()
asyncio.run(run())