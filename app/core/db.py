import databases
import ormar
import sqlalchemy

from app.core.config import settings

database = databases.Database(settings.DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(
        max_length=128, unique=True, nullable=False)
    email: str = ormar.String(
        max_length=40, unique=True, nullable=False)
    password: str = ormar.String(min_length=5,
                                 max_length=100,
                                 encrypt_secret=settings.DB_SECRET,
                                 encrypt_backend=ormar.EncryptBackends.FERNET,
                                 unique=False,
                                 nullable=False)
    is_active: bool = ormar.Boolean(default=True, nullable=False)


engine = sqlalchemy.create_engine(settings.DB_URL)
metadata.create_all(engine)
