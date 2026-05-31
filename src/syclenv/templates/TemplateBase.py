from abc import abstractmethod
from typing import Protocol

from syclenv.templates import SetupArg


class TemplateBase(Protocol):
    name: str
    description: str

    @abstractmethod
    def __init__(self, args: SetupArg):
        raise NotImplementedError

    @abstractmethod
    def check_prerequisites(self) -> tuple[bool, str]:
        raise NotImplementedError

    @abstractmethod
    def install_prerequisites(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_env(self) -> None:
        raise NotImplementedError
