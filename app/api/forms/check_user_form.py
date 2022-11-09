from typing import List, Optional

from app.api.forms.abstract_form import AbstractForm
from fastapi import Request


class CheckUserForm(AbstractForm):
    """
    Basic form class to be inherited by other forms.
    Inherits AbstractForm to pass it forward to the children.

    Args:
        AbstractForm: basic abstract helper class
    """

    def __init__(self, request: Request) -> None:
        """
        Initialize form.
        self: request, errors, username created.

        Args:
            request (Request): from which form data will be taken.
        """
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None

    async def load_data(self):
        """
        Load username from the form.

        Returns:
            request taken form to be inherited by the children.
        """
        form = await self.request.form()
        self.username = form.get(
            "username"
        )
        return form

    async def is_valid(self) -> bool:
        """
        Check for any errors within form.
        Errors can be added after from instantation
        to transmit messages to UI within HTML response.

        Returns:
            bool:
                True in no errors
                False if errors present
        """
        if not self.errors:
            return True
        else:
            return False
