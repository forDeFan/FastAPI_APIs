from typing import Optional

from app.api.forms.check_user_form import CheckUserForm
from fastapi import Request


class UpdateUserPassForm(CheckUserForm):

    def __init__(self, request: Request) -> None:
        super().__init__(request=request)
        self.old_password: Optional[str] = None
        self.new_password: Optional[str] = None

    async def load_data(self) -> None:
        form = await super().load_data()
        self.old_password = form['old_password']
        self.new_password = form['new_password']

    async def is_valid(self) -> bool:
        if not self.username or self.username.startswith(" "):
            self.errors.append("Username is obligatory")
        if not self.old_password or not len(self.old_password) >= 5:
            self.errors.append("A valid old password is required")
        if not self.new_password or not len(self.new_password) >= 5:
            self.errors.append("A valid new password is required")
        if not self.errors:
            return True
        return False
