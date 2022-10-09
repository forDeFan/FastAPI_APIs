from abc import ABC, abstractmethod
from fastapi import Request


class Abstract_Form(ABC):

    @abstractmethod
    def __init__(self, request: Request):
        pass

    @abstractmethod
    async def load_data(self):
        pass

    @abstractmethod
    async def is_valid(self):
        pass