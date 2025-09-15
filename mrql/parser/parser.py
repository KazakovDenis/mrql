from lark import Lark, Transformer, Tree

from mrql.utils.json import json_loads


def load_parser(path: str = 'mrql/grammar/mrql.lark') -> Lark:
    with open(path) as f:
        grammar = f.read()
    return Lark(grammar, parser='lalr', propagate_positions=True)


class PipelineTransformer(Transformer):
    @staticmethod
    def match_stage(items: list[Tree]) -> dict[str, str | list[Tree]]:
        field = items[0].children[0].children[-1].value  # ty: ignore
        value = json_loads(items[0].children[-1].children[-1].value)  # ty: ignore
        return {'type': 'match', 'field': field, 'value': value}

    @staticmethod
    def limit_stage(items: list[Tree]) -> dict[str, str | list[Tree]]:
        return {'type': 'limit', 'value': int(items[0].children[0].value)}  # ty: ignore

    @staticmethod
    def stage(items: list[Tree]) -> Tree:
        return items[0]

    @staticmethod
    def pipeline(items: list[Tree]) -> dict[str, str | list[Tree]]:
        return {'type': 'pipeline', 'stages': items}
