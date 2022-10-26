from abc import ABC, abstractmethod

from fastapi import Request


class AbstractForm(ABC):

    @abstractmethod
    def __init__(self, request: Request) -> None:
        pass

    @abstractmethod
    async def load_data(self):
        pass

    @abstractmethod
    async def is_valid(self) -> bool:
        pass
