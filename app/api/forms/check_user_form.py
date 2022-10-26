from typing import List, Optional

from app.api.forms.abstract_form import AbstractForm
from fastapi import Request


class CheckUserForm(AbstractForm):

    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "username"
        )
        return form

    async def is_valid(self) -> bool:
        if not self.errors:
            return True
        else:
            return False
