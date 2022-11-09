from typing import Optional

from app.api.forms.check_user_form import CheckUserForm
from fastapi import Request


class LoginForm(CheckUserForm):
    """
    Login form class.

    Args:
        CheckUserForm: inherited basic form.
    """
    def __init__(self, request: Request) -> None:
        """
        Form initialization.
        CheckUser form (inherited) initialized as well.

        Args:
            request (Request): from which form will be taken
        """
        super().__init__(request=request)
        self.password: Optional[str] = None

    async def load_data(self) -> None:
        """
        Load username and password from the form.
        """
        form = await super().load_data()
        self.username = form['username']
        self.password = form['password']

    async def is_valid(self) -> bool:
        """
        Validate username (for presence) and password (for presence and length).
        Not validated against database here.

        Returns:
            bool:
                True if all fields validated ok
                False if any fields validated negatively
        """
        if not self.username:
            self.errors.append("Username is required")
        if not self.password or not len(self.password) >= 5:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False
