import jsonschema

from .run import _run

_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "studlab": {"type": "string"},
            "treat1": {"type": "string"},
            "treat2": {"type": "string"},
            "TE": {"type": "number"},
            "seTE": {"type": "number"},
        },
        "required": ["studlab", "treat1", "treat2", "TE", "seTE"],
        "additionalProperties": False,
    },
}


def nma(data: list[dict], greater_is_better: bool = True) -> dict:
    """Run a frequentist random-effects network meta-analysis.

    Uses the `netmeta` R package (DL estimator, t-distribution confidence intervals).

    Args:
        data: Pairwise contrast data. Each element requires:
            `studlab` (str), `treat1` (str), `treat2` (str),
            `TE` (float, mean difference treat1 − treat2), `seTE` (float).
        greater_is_better: If `True`, higher values rank better (e.g. accuracy).
            If `False`, lower values rank better (e.g. error rate).

    Returns:
        A dict with keys:

        - `ranking`: P-score per treatment (0–1, higher = better rank).
        - `league`: Pairwise `md`, `lower`, `upper`, `z`, `pval` — each a treatment × treatment matrix.
        - `heterogeneity`: `tau2`, `tau`, `i2`, `i2_lower`, `i2_upper`, `q`, `q_df`, `q_pval`.
        - `prediction`: Prediction interval `lower` and `upper` — each a treatment × treatment matrix.

    Raises:
        jsonschema.ValidationError: If `data` does not match the expected schema.
        RuntimeError: If the R process returns an error.
    """
    jsonschema.validate(instance=data, schema=_schema)
    return _run("nma", data, greater_is_better)
