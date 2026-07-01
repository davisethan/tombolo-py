import re

import jsonschema
import matplotlib.pyplot as plt

from ._utils import _grid, _table, _forest, _barh


def ranking_plot(data: dict) -> plt.Figure:
    """Horizontal bar chart of treatment rankings.

    Parameters:
    - `data`: Result dict from `tombolo.nma` or `tombolo.bnma`. Only `ranking` is used.

    Returns treatments sorted by rank score (P-score for NMA, SUCRA for BNMA).
    """
    _schema = {
        "type": "object",
        "required": ["ranking"],
        "properties": {
            "ranking": {
                "type": "object",
                "additionalProperties": {"type": "number", "minimum": 0, "maximum": 1},
            }
        },
    }
    jsonschema.validate(instance=data, schema=_schema)
    return _barh(data["ranking"])


def league_table(data: dict) -> plt.Figure:
    """Grid of pairwise treatment comparisons.

    Parameters:
    - `data`: Result dict from `tombolo.nma` or `tombolo.bnma`. Only `league` is used.

    Each cell shows the mean difference and confidence (or credible) interval for the row
    treatment relative to the column treatment. Diagonal cells show the treatment name.
    P-values are included for NMA results.
    """
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

    jsonschema.validate(instance=data, schema=_schema)
    return _grid(data["league"])


def heterogeneity_table(data: dict) -> plt.Figure:
    """Summary table of heterogeneity statistics.

    Parameters:
    - `data`: Result dict from `tombolo.nma` or `tombolo.bnma`. Only `heterogeneity` is used.

    For NMA results: Q statistic, p-value, I², and τ.
    For BNMA results: posterior SD and 95% credible interval.
    """
    _nma_heterogeneity = {
        "type": "object",
        "required": [
            "tau2",
            "tau",
            "i2",
            "i2_lower",
            "i2_upper",
            "q",
            "q_df",
            "q_pval",
        ],
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

    jsonschema.validate(instance=data, schema=_schema)
    return _table(data["heterogeneity"])


def forest_plot(data: dict, reference: str) -> plt.Figure:
    """Forest plot of all treatments relative to a reference.

    Parameters:
    - `data`: Result dict from `tombolo.nma` or `tombolo.bnma`. Only `league` is used.
    - `reference`: Name of the reference treatment. All other treatments are plotted
      relative to it, sorted by effect size. Non-alphanumeric characters are normalized to underscores.

    Returns mean differences and confidence (or credible) intervals for each treatment
    versus the reference. P-values are included for NMA results.

    Raises `RuntimeError` if `reference` is not found in the data.
    """
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

    jsonschema.validate(instance=data, schema=_schema)
    ref = re.sub(r"[^A-Za-z0-9_]", "_", reference)
    if ref not in data["league"]["md"]:
        raise RuntimeError("Missing reference")

    label = "[95% CI]" if "pval" in data["league"] else "[95% CrI]"
    return _forest(data["league"], ref, interval_label=label)


def prediction_table(data: dict) -> plt.Figure:
    """Grid of prediction intervals. Only applicable to NMA results.

    Parameters:
    - `data`: Result dict from `tombolo.nma`. Only `prediction` is used.

    Each cell shows the 95% prediction interval for the row treatment relative to the column treatment.
    """
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

    jsonschema.validate(instance=data, schema=_schema)
    return _grid(data["prediction"])


def convergence_table(data: dict) -> plt.Figure:
    """Summary table of MCMC convergence diagnostics. Only applicable to BNMA results.

    Parameters:
    - `data`: Result dict from `tombolo.bnma`. Only `convergence` is used.

    Returns R̂ (max), ESS bulk (min), and ESS tail (min) across all model parameters.
    """
    _schema = {
        "type": "object",
        "required": ["convergence"],
        "properties": {
            "convergence": {
                "type": "object",
                "required": ["rhat_max", "ess_bulk_min", "ess_tail_min"],
                "properties": {
                    "rhat_max": {"type": "number"},
                    "ess_bulk_min": {"type": "number"},
                    "ess_tail_min": {"type": "number"},
                },
            }
        },
    }
    jsonschema.validate(instance=data, schema=_schema)
    return _table(data["convergence"])
