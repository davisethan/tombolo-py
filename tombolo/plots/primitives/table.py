import matplotlib.pyplot as plt
import pandas as pd
from plottable import ColumnDefinition, Table

from .utils import _text_width


def _value(v: float) -> str:
    return "< 0.001" if v < 0.001 else f"{v:.3f}"


def _dataframe(data: dict) -> pd.DataFrame:
    d = {}
    if "q" in data and "q_df" in data:
        d[rf"$\mathbf{{Q}}$(df={data['q_df']})"] = _value(data["q"])
    if "q_pval" in data:
        d["p-value"] = _value(data["q_pval"])
    if "i2" in data:
        d[r"$\mathbf{I^2}$"] = _value(data["i2"])
    if "i2_lower" in data and "i2_upper" in data:
        d["95% CI"] = f"[{_value(data['i2_lower'])}, {_value(data['i2_upper'])}]"
    if "tau2" in data:
        d[r"$\boldsymbol{\tau}\mathbf{^2}$"] = _value(data["tau2"])
    if "tau" in data:
        d[r"$\boldsymbol{\tau}$"] = _value(data["tau"])
    if "sd" in data:
        d["SD"] = _value(data["sd"])
    if "sd_lower" in data and "sd_upper" in data:
        d["95% CrI"] = f"[{_value(data['sd_lower'])}, {_value(data['sd_upper'])}]"
    if "rhat_max" in data:
        d[r"$\mathbf{\hat{R}}$"] = _value(data["rhat_max"])
    if "ess_bulk_min" in data:
        d["ESS bulk"] = _value(data["ess_bulk_min"])
    if "ess_tail_min" in data:
        d["ESS tail"] = _value(data["ess_tail_min"])
    return pd.DataFrame([d])


def _table(data: dict) -> plt.Figure:
    df = _dataframe(data)
    df.insert(0, "_idx", "")

    fontsize = 10
    col_widths = {
        col: _text_width([col] + [str(v) for v in df[col]], fontsize, pad=0.3)
        for col in df.columns[1:]
    }

    col_defs = [
        ColumnDefinition("_idx", title="", width=0),
        *[
            ColumnDefinition(col, textprops={"ha": "center"}, width=col_widths[col])
            for col in df.columns[1:]
        ],
    ]

    fig_w = sum(col_widths.values())
    fig, ax = plt.subplots(figsize=(fig_w, 0.8))
    t = Table(df, ax=ax, index_col="_idx", column_definitions=col_defs)
    for cell in t.col_label_row.cells:
        cell.text.set_fontweight("bold")

    fig.tight_layout()
    return fig
