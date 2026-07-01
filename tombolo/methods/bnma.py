import jsonschema

from .run import _run

_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "study": {"type": "string"},
            "treatment": {"type": "string"},
            "mean": {"type": "number"},
            "std.dev": {"type": "number"},
            "sampleSize": {"type": "integer"},
        },
        "required": ["study", "treatment", "mean", "std.dev", "sampleSize"],
        "additionalProperties": False,
    },
}


def bnma(data: list[dict], greater_is_better: bool = True) -> dict:
    """Run a Bayesian random-effects network meta-analysis.

    Uses the `gemtc` R package with JAGS (normal likelihood, identity link).

    Args:
        data: Arm-level summary data. Each element requires:
            `study` (str), `treatment` (str), `mean` (float),
            `std.dev` (float), `sampleSize` (int).
        greater_is_better: If `True`, higher values rank better (e.g. accuracy).
            If `False`, lower values rank better (e.g. error rate).

    Returns:
        A dict with keys:

        - `ranking`: SUCRA per treatment (0–1, higher = better rank).
        - `league`: Pairwise posterior median `md` and 95% credible interval `lower`, `upper` — each a treatment × treatment matrix.
        - `heterogeneity`: Posterior `sd`, `sd_lower`, `sd_upper` (2.5th–97.5th percentile).
        - `convergence`: `rhat_max`, `ess_bulk_min`, `ess_tail_min` across all model parameters.

    Raises:
        jsonschema.ValidationError: If `data` does not match the expected schema.
        RuntimeError: If the R process returns an error.
    """
    jsonschema.validate(instance=data, schema=_schema)
    return _run("bnma", data, greater_is_better)
