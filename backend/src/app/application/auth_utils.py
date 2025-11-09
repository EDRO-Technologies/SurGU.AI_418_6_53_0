from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.main.config import JWTConfig


def jwt_encode(payload: dict, jwt_config: JWTConfig) -> str:
    expire_time = datetime.now(UTC) + timedelta(
        seconds=jwt_config.expire_at_seconds
    )
    payload.update(iat=datetime.now(UTC))
    payload.update(exp=expire_time)

    return jwt.encode(
        payload=payload,
        key=jwt_config.private_key.read_text(),
        algorithm=jwt_config.alghorithm,
    )


def jwt_decode(token: str, jwt_config: JWTConfig) -> dict:
    return jwt.decode(
        jwt=token,
        key=jwt_config.public_key.read_text(),
        algorithms=[jwt_config.alghorithm],
    )


def is_valid_password(unhashed_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(unhashed_password.encode(), hashed_password)


def hash_password(unhashed_password: str) -> bytes:
    return bcrypt.hashpw(unhashed_password.encode(), bcrypt.gensalt())
