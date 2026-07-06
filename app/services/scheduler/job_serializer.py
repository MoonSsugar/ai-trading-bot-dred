from typing import Any

import orjson


def job_serializer(result: dict[str, Any]) -> bytes:
    if isinstance(result.get("r"), Exception):
        result["r"] = str(result["r"])

    return orjson.dumps(result)
