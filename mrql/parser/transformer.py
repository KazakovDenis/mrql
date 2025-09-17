from typing import Any

from lark import Transformer, Tree, Token


class PipelineTransformer(Transformer):
    @staticmethod
    def pipeline(items: list[Tree | Token]) -> dict[str, list[Tree | Token]]:
        return {
            'type': 'pipeline',
            'stages': items,
        }

    @staticmethod
    def stage(items: list[Tree]) -> Tree:
        return items[0]

    @staticmethod
    def match_stage(items: list[Tree | Token]) -> dict[str, Tree | Token]:
        return {'type': 'match', 'expr': items[0]}

    @staticmethod
    def limit_stage(items: list[Tree | Token]) -> dict[str, Tree | Token]:
        return {'type': 'limit', 'value': items[0]}

    @staticmethod
    def set_stage(items: list[Tree | Token]) -> dict[str, Tree | Token]:
        field, expr = items
        return {'type': 'set', 'field': field, 'expr': expr}

    @staticmethod
    def project_stage(items: list[Tree | Token]) -> dict[str, list[Tree | Token]]:
        return {'type': 'project', 'projections': items}

    @staticmethod
    def project_field(items: list[Tree | Token]) -> dict[str, Tree | Token | dict]:
        return {
            'field': str(items[0]),
            'expr': {'type': 'field_ref', 'value': str(items[0])},
        }

    @staticmethod
    def projection(items: list[Tree | Token]) -> dict[str, Tree | Token]:
        field, expr = items
        return {'field': str(field), 'expr': expr}

    # ---------- logical ----------
    @staticmethod
    def or_(items: list[Tree | Token]) -> dict[str, str | Tree | Token]:
        return {'op': 'or', 'args': items}

    @staticmethod
    def and_(items: list[Any]) -> dict[str, Any]:
        return {'op': 'and', 'args': items}

    # ---------- comparison ----------
    @staticmethod
    def eq(items: list[Any]) -> dict[str, Any]:
        return {'op': 'eq', 'args': items}

    @staticmethod
    def ne(items: list[Any]) -> dict[str, Any]:
        return {'op': 'ne', 'args': items}

    @staticmethod
    def gt(items: list[Any]) -> dict[str, Any]:
        return {'op': 'gt', 'args': items}

    @staticmethod
    def gte(items: list[Any]) -> dict[str, Any]:
        return {'op': 'gte', 'args': items}

    @staticmethod
    def lt(items: list[Any]) -> dict[str, Any]:
        return {'op': 'lt', 'args': items}

    @staticmethod
    def lte(items: list[Any]) -> dict[str, Any]:
        return {'op': 'lte', 'args': items}

    # ---------- arithmetic ----------
    @staticmethod
    def add(items: list[Any]) -> dict[str, Any]:
        return {'op': 'add', 'args': items}

    @staticmethod
    def sub(items: list[Any]) -> dict[str, Any]:
        return {'op': 'sub', 'args': items}

    @staticmethod
    def mul(items: list[Any]) -> dict[str, Any]:
        return {'op': 'mul', 'args': items}

    @staticmethod
    def div(items: list[Any]) -> dict[str, Any]:
        return {'op': 'div', 'args': items}

    @staticmethod
    def neg(items: list[Any]) -> dict[str, Any]:
        return {'op': 'neg', 'arg': items[0]}

    # ---------- atomics ----------
    @staticmethod
    def var(items: list[Any]) -> dict[str, Any]:
        return {'type': 'var', 'name': str(items[0])}

    @staticmethod
    def param(items: list[Token]) -> dict:
        return {'type': 'param', 'name': items[0].value}

    @staticmethod
    def string(items: list[Any]) -> dict[str, Any]:
        return {'type': 'string', 'value': str(items[0])[1:-1]}

    @staticmethod
    def number(items: list[Any]) -> dict[str, Any]:
        return {'type': 'number', 'value': float(items[0])}

    @staticmethod
    def array(items: list[Any]) -> dict[str, Any]:
        return {'type': 'array', 'items': items}

    @staticmethod
    def field_ref(items: list[Any]) -> dict[str, Any]:
        return {'type': 'field_ref', 'path': [str(x) for x in items]}

    @staticmethod
    def value(items: list[Any]) -> float:
        return float(items[0])

    @staticmethod
    def func_call(items: list[Any]) -> dict[str, Any]:
        name = str(items[0])
        args = items[1:]
        return {'type': 'func_call', 'name': name, 'args': args}
