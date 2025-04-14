from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_token(data: dict, token_type: str = "access"):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    expire = now + \
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) \
        if token_type == "access" \
        else timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": token_type})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None