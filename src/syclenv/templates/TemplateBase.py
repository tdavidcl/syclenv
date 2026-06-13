from abc import ABC, abstractmethod

from syclenv.templates.SetupArg import SetupArg


class TemplateBase(ABC):
    name: str
    description: str

    @abstractmethod
    def __init__(self, args: SetupArg): ...

    @abstractmethod
    def on_check_prerequisites(self) -> tuple[bool, str]: ...

    @abstractmethod
    def on_install_prerequisites(self) -> None: ...

    @abstractmethod
    def create_env(self) -> None: ...
