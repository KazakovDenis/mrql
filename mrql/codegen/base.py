from abc import ABC, abstractmethod
from typing import Any, NoReturn


class BaseCompiler(ABC):
    def __init__(self, ir: dict[str, Any]) -> None:
        if ir.get('type') != 'pipeline':
            raise ValueError('Only pipelines supported now')
        self._ir = ir

    @abstractmethod
    def compile(self, **params) -> NoReturn:
        raise NotImplementedError
