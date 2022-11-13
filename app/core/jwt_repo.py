from typing import Union

from app.core.model.jwt_model import JwtModel


class JwtRepo:
    """
    JWT token repository connecting with JWT Model in Ormar for validation.
    """

    @classmethod
    async def add_to_database(self, token: str) -> None:
        """
        Add token to database in order to black listing if token to be used for antoher login.

        Args:
            token (str): token to be black listed
        """
        await JwtModel.objects.create(token=token)

    @classmethod
    async def get_from_database(
        self, token: str
    ) -> Union[JwtModel, None]:
        """
        Check if token is blacklisted (present in database).

        Args:
            token (str): to be checked against database

        Returns:
            Union[JwtModel, None]:
                JwtModel (token) if blacklisted
                None if token not blacklisted
        """
        db_token = await JwtModel.objects.get_or_none(token=token)
        return db_token
