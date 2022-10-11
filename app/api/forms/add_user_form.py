from typing import Optional

from app.api.forms.check_user_form import Check_User_Form
from fastapi import Request


class Add_User_Form(Check_User_Form):

    def __init__(self, request: Request) -> None:
        super().__init__(request=request)
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self) -> None:
        form = await super().load_data()
        self.email = form['email']
        self.password = form['password']

    async def is_valid(self) -> bool:
        if not self.username or self.username.startswith(" "):
            self.errors.append("Valid username is required")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 5:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False
