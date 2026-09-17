import asyncio
import uuid

import httpx

from app import main
from app.main import password_ok


def test_password_policy():
    assert password_ok('Ab1!valid')
    assert not password_ok('abcd1234')
    assert not password_ok('abcd1234가')
    assert not password_ok('Ab1! xyz0')


def test_development_shortcuts_require_both_flags():
    assert main.dev_shortcuts_enabled('development', 'true')
    assert not main.dev_shortcuts_enabled('development', 'false')
    assert not main.dev_shortcuts_enabled('production', 'true')
    assert not main.dev_shortcuts_enabled('production', 'false')

def test_password_matches_uses_dummy_hash_when_user_is_missing(monkeypatch):
    compared_hashes = []

    def checkpw(password, password_hash):
        compared_hashes.append(password_hash)
        return False

    monkeypatch.setattr(main.bcrypt, 'checkpw', checkpw)
    assert not main.password_matches('wrong-password')
    assert compared_hashes == [main._DUMMY_PASSWORD_HASH]


def test_auth_http_contract_with_local_postgres():
    asyncio.run(_exercise_auth_http_contract())


def _registration(email, nickname, **overrides):
    payload = {
        'email': email,
        'password': 'Ab1!valid',
        'nickname': nickname,
        'major': '방사선학과',
        'majorOther': '',
        'signupSource': '',
        'signupSourceOther': '',
        'termsAccepted': True,
        'privacyAccepted': True,
        'ageConfirmed': True,
        'marketingAccepted': False,
    }
    payload.update(overrides)
    return payload


async def _exercise_auth_http_contract():
    marker = uuid.uuid4().hex
    emails = []

    def identity(label):
        email = f'pytest-auth-{marker}-{label}@example.local'
        emails.append(email)
        return email, f'pytest{marker[:8]}{label}'

    original_env, original_dev = main.ENV, main.DEV
    main.attempts.clear()
    await main.startup()
    transport = httpx.ASGITransport(app=main.app, client=('127.0.0.1', 43123))
    try:
        async with httpx.AsyncClient(transport=transport, base_url='http://testserver') as client:
            other_email, other_nickname = identity('other')
            response = await client.post('/v1/auth/register', json=_registration(
                other_email,
                other_nickname,
                major='기타 보건의료계열',
                majorOther='임상병리학과',
                signupSource='기타',
                signupSourceOther='교수님추천',
            ))
            assert response.status_code == 201
            profile = await main.pool.fetchrow(
                'select major, signup_source from user_profiles p join users u on u.id=p.user_id where u.email=$1',
                other_email,
            )
            assert dict(profile) == {'major': '임상병리학과', 'signup_source': '교수님추천'}

            user_email, user_nickname = identity('selected')
            response = await client.post('/v1/auth/register', json=_registration(
                user_email,
                user_nickname,
                majorOther='이전화면잔재값',
            ))
            assert response.status_code == 201
            profile = await main.pool.fetchrow(
                'select major from user_profiles p join users u on u.id=p.user_id where u.email=$1',
                user_email,
            )
            assert profile['major'] == '방사선학과'

            duplicate_email, duplicate_nickname = identity('duplicate-email')
            response = await client.post('/v1/auth/register', json=_registration(duplicate_email, duplicate_nickname))
            assert response.status_code == 201
            response = await client.post('/v1/auth/register', json=_registration(duplicate_email, f'{duplicate_nickname}x'))
            assert response.status_code == 409
            duplicate_nickname_email, _ = identity('duplicate-nickname')
            response = await client.post('/v1/auth/register', json=_registration(duplicate_nickname_email, duplicate_nickname))
            assert response.status_code == 409

            main.DEV = True
            dev_email, dev_nickname = identity('dev-token')
            response = await client.post('/v1/auth/register', json=_registration(dev_email, dev_nickname))
            assert response.status_code == 201 and 'developmentToken' in response.json()
            main.DEV = False
            prod_email, prod_nickname = identity('no-dev-token')
            response = await client.post('/v1/auth/register', json=_registration(prod_email, prod_nickname))
            assert response.status_code == 201 and 'developmentToken' not in response.json()

            main.attempts.clear()
            response = await client.post('/v1/auth/login', json={'email': user_email, 'password': 'Ab1!valid'})
            assert response.status_code == 200
            assert (await client.get('/v1/users/me')).status_code == 200
            assert (await client.post('/v1/auth/logout')).status_code == 204
            assert (await client.get('/v1/users/me')).status_code == 401

            main.attempts.clear()
            for _ in range(10):
                response = await client.post('/v1/auth/login', json={'email': 'email-limit@example.local', 'password': 'wrong'})
                assert response.status_code == 401
            response = await client.post('/v1/auth/login', json={'email': 'email-limit@example.local', 'password': 'wrong'})
            assert response.status_code == 429 and response.headers['Retry-After']

            main.attempts.clear()
            for index in range(20):
                response = await client.post('/v1/auth/login', json={'email': f'ip-limit-{index}@example.local', 'password': 'wrong'})
                assert response.status_code == 401
            response = await client.post('/v1/auth/login', json={'email': 'ip-limit-final@example.local', 'password': 'wrong'})
            assert response.status_code == 429

            main.attempts.clear()
            for _ in range(5):
                assert (await client.post('/v1/auth/login', json={'email': user_email, 'password': 'wrong'})).status_code == 401
            assert (await client.post('/v1/auth/login', json={'email': user_email, 'password': 'Ab1!valid'})).status_code == 200
            for _ in range(10):
                assert (await client.post('/v1/auth/login', json={'email': user_email, 'password': 'wrong'})).status_code == 401

            main.ENV, main.DEV = 'production', False
            secure_email, secure_nickname = identity('secure-cookie')
            response = await client.post('/v1/auth/register', json=_registration(secure_email, secure_nickname))
            assert 'developmentToken' not in response.json()
            response = await client.post('/v1/auth/login', json={'email': secure_email, 'password': 'Ab1!valid'})
            assert 'Secure' in response.headers['set-cookie']
    finally:
        main.ENV, main.DEV = original_env, original_dev
        main.attempts.clear()
        if main.pool:
            await main.pool.execute('delete from users where email = any($1::text[])', emails)
        await main.shutdown()