from ormar import EncryptBackends, Integer, Model, String

from app.core.config import settings
from app.core.db import BaseMeta


class JwtModel(Model):
    """
    Model class for database operations to be checked against Pydantic by Ormar.
    Table used for storing blacklisted JWT tokens.
    """
    class Meta(BaseMeta):
        tablename = "blacklisted_jwt"

    id: int = Integer(primary_key=True)
    token: str = String(
        max_length=680,
        encrypt_secret=settings.DB_SECRET,
        encrypt_backend=EncryptBackends.FERNET,
        unique=True,
        nullable=False,
    )
