from abc import ABC, abstractmethod

from fastapi import Request


class AbstractForm(ABC):
    """
    Form abstract class to be inherited by all forms.

    Args:
        ABC: abstract helper class
    """

    @abstractmethod
    def __init__(self, request: Request) -> None:
        pass

    @abstractmethod
    async def load_data(self):
        """
        Load all fields from the FastAPI form.
        """
        pass

    @abstractmethod
    async def is_valid(self) -> bool:
        """
        Validation of specified fields within the form.

        Returns:
            bool: 
                True if valid
                False if unvalid
        """
        pass
