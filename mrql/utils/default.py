import threading
from collections.abc import Callable

from lark import Lark

from mrql.codegen.python import PythonCompiler
from mrql.parser.parser import load_parser
from mrql.parser.transformer import PipelineTransformer

_lock = threading.Lock()
_parser = None
_transformer = None


def _compile(parser: Lark, transformer: PipelineTransformer) -> Callable[[str], list[dict]]:
    def inner(query: str) -> list[dict]:
        ast = parser.parse(query)
        ir = transformer.transform(ast)
        return PythonCompiler(ir).compile()

    return inner


def get_default_compiler() -> Callable[[str], list[dict]]:
    global _parser, _transformer  # noqa: PLW0603

    with _lock:
        if _parser is None:
            _parser = load_parser()
        if _transformer is None:
            _transformer = PipelineTransformer()

    return _compile(_parser, _transformer)
