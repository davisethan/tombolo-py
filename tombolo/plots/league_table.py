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
    "required": ["league"],
    "properties": {
        "league": {
            "type": "object",
            "required": ["md", "lower", "upper"],
            "properties": {
                "md": _matrix,
                "lower": _matrix,
                "upper": _matrix,
                "pval": _matrix,
            },
        }
    },
}


def league_table(data: dict) -> plt.Figure:
    """Grid of pairwise treatment comparisons.

    Args:
        data: Result dict from `tombolo.nma` or `tombolo.bnma`. Only `league` is used.

    Returns:
        A matrix where each cell shows the mean difference and confidence (or credible)
        interval for the row treatment relative to the column treatment. Diagonal cells
        show the treatment name. P-values are included for NMA results.
    """
    jsonschema.validate(instance=data, schema=_schema)
    return _grid(data["league"])
