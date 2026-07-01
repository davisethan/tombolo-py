import jsonschema
import matplotlib.pyplot as plt

from .primitives.table import _table

_nma_heterogeneity = {
    "type": "object",
    "required": ["tau2", "tau", "i2", "i2_lower", "i2_upper", "q", "q_df", "q_pval"],
    "properties": {
        "tau2": {"type": "number", "minimum": 0},
        "tau": {"type": "number", "minimum": 0},
        "i2": {"type": "number", "minimum": 0, "maximum": 1},
        "i2_lower": {"type": "number", "minimum": 0, "maximum": 1},
        "i2_upper": {"type": "number", "minimum": 0, "maximum": 1},
        "q": {"type": "number", "minimum": 0},
        "q_df": {"type": "integer", "minimum": 0},
        "q_pval": {"type": "number", "minimum": 0, "maximum": 1},
    },
}

_bnma_heterogeneity = {
    "type": "object",
    "required": ["sd", "sd_lower", "sd_upper"],
    "properties": {
        "sd": {"type": "number", "minimum": 0},
        "sd_lower": {"type": "number", "minimum": 0},
        "sd_upper": {"type": "number", "minimum": 0},
    },
}

_schema = {
    "type": "object",
    "required": ["heterogeneity"],
    "properties": {
        "heterogeneity": {"oneOf": [_nma_heterogeneity, _bnma_heterogeneity]}
    },
}


def heterogeneity_table(data: dict) -> plt.Figure:
    """Summary table of heterogeneity statistics.

    Args:
        data: Result dict from `tombolo.nma` or `tombolo.bnma`. Only `heterogeneity` is used.

    Returns:
        For NMA results: Q statistic, p-value, I², and τ.
        For BNMA results: posterior SD and 95% credible interval.
    """
    jsonschema.validate(instance=data, schema=_schema)
    return _table(data["heterogeneity"])
