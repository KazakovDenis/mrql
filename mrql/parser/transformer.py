from lark import Transformer, Tree

from mrql.utils.json import json_loads


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
