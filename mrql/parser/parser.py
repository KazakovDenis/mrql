from lark import Lark


def load_parser(path: str = 'mrql/grammar/mrql.lark') -> Lark:
    with open(path) as f:
        grammar = f.read()
    return Lark(grammar, parser='lalr', propagate_positions=True)
