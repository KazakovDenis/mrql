from typing import Any

from mrql.codegen.base import BaseCompiler


class PythonCompiler(BaseCompiler):
    def compile(self, **params) -> list[dict[str, Any]]:
        pipeline = []
        for stage in self._ir.get('stages', []):
            stage_type = stage.get('type')
            handler = getattr(self, f'_compile_{stage_type}', None)
            if handler is None:
                raise NotImplementedError(f'Unknown stage: {stage_type}')
            pipeline.append(handler(stage, params))
        return pipeline

    def _compile_match(self, stage: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
        expr = self._compile_expr(stage['expr'], params)

        if isinstance(expr, dict) and '$eq' in expr:
            left, right = expr['$eq']
            if isinstance(left, str) and not left.startswith('$'):
                return {'$match': {left: right}}
            elif isinstance(right, str) and not right.startswith('$'):
                return {'$match': {right: left}}

        return {'$match': expr}

    def _compile_limit(self, stage: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
        expr = self._compile_expr(stage['value'], params)
        return {'$limit': int(expr)}

    def _compile_expr(self, node: dict[str, Any], params: dict[str, Any]) -> Any:
        node_type = node.get('type')

        if node_type == 'var':
            return node['name']

        if node_type == 'string':
            return node['value']

        if node_type == 'number':
            return int(node['value'])

        if node_type == 'param':
            # подставляем значение из params
            name = node['name']
            if name not in params:
                raise ValueError(f'Parameter {name} not provided')
            return params.get(name)

        if node_type == 'field_ref':
            return '$' + '.'.join(node['path'])

        if node_type == 'array':
            return [self._compile_expr(item, params) for item in node['items']]

        if node_type == 'func_call':
            return {f'${node["name"]}': [self._compile_expr(arg, params) for arg in node['args']]}

        if 'op' in node:
            op = node['op']
            args = [self._compile_expr(arg, params) for arg in node['args']]
            return {f'${op}': args}

        raise NotImplementedError(f'Unsupported expr node: {node}')
