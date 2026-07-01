# tombolo

Python interface to R statistics via Docker.

## Requirements

[Docker](https://docs.docker.com/get-started/get-docker/) must be installed and running, and the tombolo image must be pulled:

```
docker pull ethandavisecd/tombolo:latest
```

## Installation

```
pip install tombolo
```

## Usage

### Network meta-analysis

`nma` expects pairwise contrast data. Each row is a comparison between two treatments within one study, expressed as a mean difference and its standard error:

```python
import tombolo

data = [
    {"studlab": "Study A", "treat1": "X", "treat2": "Y", "TE": 0.32, "seTE": 0.12},
    {"studlab": "Study A", "treat1": "X", "treat2": "Z", "TE": 0.48, "seTE": 0.14},
    {"studlab": "Study B", "treat1": "X", "treat2": "Z", "TE": 0.51, "seTE": 0.18},
    {"studlab": "Study C", "treat1": "Y", "treat2": "Z", "TE": 0.19, "seTE": 0.15},
]

result = tombolo.nma(data, greater_is_better=True)
```

### Bayesian network meta-analysis

`bnma` expects arm-level summary statistics:

```python
data = [
    {"study": "Study A", "treatment": "X", "mean": 0.82, "std.dev": 0.21, "sampleSize": 30},
    {"study": "Study A", "treatment": "Y", "mean": 0.74, "std.dev": 0.19, "sampleSize": 30},
    {"study": "Study B", "treatment": "X", "mean": 0.79, "std.dev": 0.23, "sampleSize": 25},
    {"study": "Study B", "treatment": "Z", "mean": 0.61, "std.dev": 0.25, "sampleSize": 25},
]

result = tombolo.bnma(data, greater_is_better=True)
```

`greater_is_better` controls the direction of ranking. Set to `False` when lower values are preferable (e.g. error rates).

## Plots

```python
from tombolo.plots import (
    ranking_plot,
    league_table,
    forest_plot,
    heterogeneity_table,
    prediction_table,  # nma only
    convergence_table, # bnma only
)

ranking_plot(result)
league_table(result)
forest_plot(result, reference="X")
heterogeneity_table(result)
```

Each function returns a `matplotlib.figure.Figure`.

## Configuration

By default tombolo uses the `ethandavisecd/tombolo:latest` Docker image. To use a different image:

```
export TOMBOLO=myorg/tombolo:v1.0
```
