import databases
import sqlalchemy
from app.core.config import settings
from ormar import ModelMeta

database = databases.Database(settings.DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ModelMeta):
    metadata = metadata
    database = database


engine = sqlalchemy.create_engine(settings.DB_URL)
