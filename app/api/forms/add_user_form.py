from typing import Optional

from app.api.forms.check_user_form import CheckUserForm
from fastapi import Request


class AddUserForm(CheckUserForm):
    """
    Form class to add user.

    Args:
        CheckUserForm: ihnerited basic form.
    """

    def __init__(self, request: Request) -> None:
        """
        Form initialization.
        CheckUser form (inherited) initialized as well.

        Args:
            request (Request): from which form will be taken
        """
        super().__init__(request=request)
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self) -> None:
        """
        Load data form form fields (username, email, password).
        """
        try:
            form = await super().load_data()
            self.email = form["email"]
            self.password = form["password"]
        except KeyError:
            self.errors.append("all requested data must be present within the form!")
            pass

    async def is_valid(self) -> bool:
        # TODO: add regex for email validation
        """
        Validate form username (for presence), email (for presence), password 
        (for presence and length).
        Not validated against database here.

        Returns:
            bool:
                True if validation went ok for all fields
                False if some fields were validated negatively
        """
        if not self.username or self.username.startswith(" "):
            self.errors.append("Valid username is required")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 5:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False
