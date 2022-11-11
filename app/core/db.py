import databases
import sqlalchemy
from app.core.config import settings
from ormar import ModelMeta

database = databases.Database(settings.DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ModelMeta):
    """
    ORM (Ormar) database setup.
    Sqlalchemy used under the sheets as well as Pydantic validation.
    For Ormar project check: 
    https://collerek.github.io/ormar/
    """
    metadata = metadata
    database = database


engine = sqlalchemy.create_engine(settings.DB_URL)
