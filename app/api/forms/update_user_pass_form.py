from typing import Optional

from app.api.forms.check_user_form import CheckUserForm
from fastapi import Request


class UpdateUserPassForm(CheckUserForm):
    """
    Update user pass form class.

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
        self.old_password: Optional[str] = None
        self.new_password: Optional[str] = None

    async def load_data(self) -> None:
        """
        Load old and new password from the form.
        """
        form = await super().load_data()
        self.old_password = form['old_password']
        self.new_password = form['new_password']

    async def is_valid(self) -> bool:
        """
        Validate form old and new password (for presence and length) along with 
        username (for presence).
        Not validated against database here.

        Returns:
            bool:
                True if all fields validated ok
                False if any fields validated negatively
        """
        if not self.username or self.username.startswith(" "):
            self.errors.append("Username is obligatory")
        if not self.old_password or not len(self.old_password) >= 5:
            self.errors.append("A valid old password is required")
        if not self.new_password or not len(self.new_password) >= 5:
            self.errors.append("A valid new password is required (min. 5 chars lenght)")
        if not self.errors:
            return True
        return False
