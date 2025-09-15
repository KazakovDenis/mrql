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
            pipeline.append(handler(stage))
        return pipeline

    @staticmethod
    def _compile_match(stage: dict[str, Any]) -> dict[str, Any]:
        return {'$match': {stage['field']: stage['value']}}

    @staticmethod
    def _compile_limit(stage: dict[str, Any]) -> dict[str, Any]:
        return {'$limit': stage['value']}
