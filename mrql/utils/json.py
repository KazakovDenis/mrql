try:
    import orjson as json
except ImportError:
    import json

json_loads = json.loads
