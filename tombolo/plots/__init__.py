"""Matplotlib figures for visualising NMA and BNMA results.

All functions accept the result dict returned by `tombolo.nma` or `tombolo.bnma`
and return a `matplotlib.figure.Figure`.
"""

from .league_table import league_table
from .forest_plot import forest_plot
from .ranking_plot import ranking_plot
from .heterogeneity_table import heterogeneity_table
from .prediction_table import prediction_table
from .convergence_table import convergence_table

__all__ = [
    league_table.__name__,
    forest_plot.__name__,
    ranking_plot.__name__,
    heterogeneity_table.__name__,
    prediction_table.__name__,
    convergence_table.__name__,
]
