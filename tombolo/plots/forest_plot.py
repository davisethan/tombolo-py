import re
import jsonschema
import matplotlib.pyplot as plt

from .primitives.forest import _forest

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


def forest_plot(data: dict, reference: str) -> plt.Figure:
    """Forest plot of all treatments relative to a reference.

    Args:
        data: Result dict from `tombolo.nma` or `tombolo.bnma`. Only `league` is used.
        reference: Name of the reference treatment. All other treatments are plotted
            relative to it, sorted by effect size. Non-alphanumeric characters are
            normalized to underscores.

    Returns:
        Mean differences and confidence (or credible) intervals for each treatment
        versus the reference. P-values are included for NMA results.

    Raises:
        RuntimeError: If `reference` is not found in the data.
    """
    jsonschema.validate(instance=data, schema=_schema)
    ref = re.sub(r"[^A-Za-z0-9_]", "_", reference)
    if ref not in data["league"]["md"]:
        raise RuntimeError("Missing reference")
    label = "[95% CI]" if "pval" in data["league"] else "[95% CrI]"
    return _forest(data["league"], ref, interval_label=label)
