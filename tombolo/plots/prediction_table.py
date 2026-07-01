import jsonschema
import matplotlib.pyplot as plt

from .primitives.grid import _grid

_matrix = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "additionalProperties": {"type": ["number", "null"]},
    },
}

_schema = {
    "type": "object",
    "required": ["prediction"],
    "properties": {
        "prediction": {
            "type": "object",
            "required": ["lower", "upper"],
            "properties": {"lower": _matrix, "upper": _matrix},
        }
    },
}


def prediction_table(data: dict) -> plt.Figure:
    """Grid of prediction intervals. Only applicable to NMA results.

    Args:
        data: Result dict from `tombolo.nma`. Only `prediction` is used.

    Returns:
        A matrix where each cell shows the 95% prediction interval for the row
        treatment relative to the column treatment.
    """
    jsonschema.validate(instance=data, schema=_schema)
    return _grid(data["prediction"])
