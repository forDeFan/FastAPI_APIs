from app.core.config import settings
from app.core.db.db import BaseMeta
from ormar import Boolean, EncryptBackends, Integer, Model, String


class User(Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = Integer(primary_key=True)
    username: str = String(
        max_length=128, unique=True, nullable=False)
    email: str = String(
        max_length=40, unique=True, nullable=False)
    password: str = String(min_length=5,
                           max_length=100,
                           encrypt_secret=settings.DB_SECRET,
                           encrypt_backend=EncryptBackends.FERNET,
                           unique=False,
                           nullable=False)
    is_active: bool = Boolean(default=True, nullable=False)
