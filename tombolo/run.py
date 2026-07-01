import json
import os
import subprocess

import jsonschema


_image = os.getenv("TOMBOLO", "ethandavisecd/tombolo:latest")


def _run(method: str, data: list[dict], greater_is_better: bool) -> dict:
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "data": data,
            "greater_is_better": greater_is_better,
        },
        "id": 1,
    }
    proc = subprocess.run(
        ["docker", "run", "--rm", "-i", _image],
        input=json.dumps(request).encode(),
        capture_output=True,
        check=True,
    )
    response = json.loads(proc.stdout)
    if "error" in response:
        raise RuntimeError(response["error"]["message"])
    return response["result"]


def nma(data: list[dict], greater_is_better: bool = True) -> dict:
    """Run a frequentist random-effects network meta-analysis.

    Uses the `netmeta` R package (DL estimator, t-distribution confidence intervals).

    Parameters:
    - `data`: Pairwise contrast data. Each element requires `studlab` (str), `treat1` (str),
      `treat2` (str), `TE` (float, mean difference treat1 − treat2), `seTE` (float).
    - `greater_is_better`: If `True`, higher values rank better (e.g. accuracy).
      If `False`, lower values rank better (e.g. error rate).

    Returns a dict with:
    - `ranking`: P-score per treatment (0–1, higher = better rank).
    - `league`: Pairwise `md`, `lower`, `upper`, `z`, `pval` — each a treatment × treatment matrix.
    - `heterogeneity`: `tau2`, `tau`, `i2`, `i2_lower`, `i2_upper`, `q`, `q_df`, `q_pval`.
    - `prediction`: Prediction interval `lower` and `upper` — each a treatment × treatment matrix.

    Raises `jsonschema.ValidationError` if `data` does not match the expected schema,
    or `RuntimeError` if the R process returns an error.
    """
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
    jsonschema.validate(instance=data, schema=_schema)
    return _run("nma", data, greater_is_better)


def bnma(data: list[dict], greater_is_better: bool = True) -> dict:
    """Run a Bayesian random-effects network meta-analysis.

    Uses the `gemtc` R package with JAGS (normal likelihood, identity link).

    Parameters:
    - `data`: Arm-level summary data. Each element requires `study` (str), `treatment` (str),
      `mean` (float), `std.dev` (float), `sampleSize` (int).
    - `greater_is_better`: If `True`, higher values rank better (e.g. accuracy).
      If `False`, lower values rank better (e.g. error rate).

    Returns a dict with:
    - `ranking`: SUCRA per treatment (0–1, higher = better rank).
    - `league`: Pairwise posterior median `md` and 95% credible interval `lower`, `upper` — each a treatment × treatment matrix.
    - `heterogeneity`: Posterior `sd`, `sd_lower`, `sd_upper` (2.5th–97.5th percentile).
    - `convergence`: `rhat_max`, `ess_bulk_min`, `ess_tail_min` across all model parameters.

    Raises `jsonschema.ValidationError` if `data` does not match the expected schema,
    or `RuntimeError` if the R process returns an error.
    """
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
    jsonschema.validate(instance=data, schema=_schema)
    return _run("bnma", data, greater_is_better)
