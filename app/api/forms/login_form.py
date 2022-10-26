from typing import Optional

from app.api.forms.check_user_form import CheckUserForm
from fastapi import Request


class LoginForm(CheckUserForm):
    def __init__(self, request: Request):
        super().__init__(request=request)
        self.password: Optional[str] = None

    async def load_data(self):
        form = await super().load_data()
        self.username = form['username']
        self.password = form['password']

    async def is_valid(self):
        if not self.username:
            self.errors.append("Username is required")
        if not self.password or not len(self.password) >= 5:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False
