import matplotlib.pyplot as plt
import pandas as pd

from .utils import _significance, _text_width


def _dataframe(data: dict, ref: str) -> pd.DataFrame:
    comparators = [c for c in data["md"].keys() if c != ref]
    rows = {
        "label": comparators,
        "md": [data["md"][ref][c] for c in comparators],
        "lower": [data["lower"][ref][c] for c in comparators],
        "upper": [data["upper"][ref][c] for c in comparators],
    }
    if "pval" in data:
        rows["pval"] = [data["pval"][ref][c] for c in comparators]
    return pd.DataFrame(rows)


def _forest(data: dict, ref: str, interval_label: str = "[95% CI]") -> plt.Figure:
    df = _dataframe(data, ref).sort_values("md").reset_index(drop=True)
    has_pval = "pval" in df.columns
    n = len(df)
    row_h = 0.2

    labels = df["label"].tolist()
    md_strs = [f"{v:+.3f}" for v in df["md"]]
    interval_strs = [
        f"[{lo:.3f}, {hi:.3f}]" for lo, hi in zip(df["lower"], df["upper"])
    ]
    if has_pval:
        p_strs = [f"{v:.3f}{_significance(v)}" for v in df["pval"]]

    ys = [i * row_h for i in range(n)]

    fontsize = 10
    lbl_w = _text_width(labels + ["Treatment"], fontsize)
    plt_w = 2.0
    md_w = _text_width(md_strs + ["MD"], fontsize)
    ci_w = _text_width(interval_strs + [interval_label], fontsize)
    p_w = _text_width(p_strs + ["p-value"], fontsize) if has_pval else 0

    margin = 0.3
    fig_w = lbl_w + plt_w + md_w + ci_w + p_w
    fig_h = n * row_h + 2 * margin

    bot = margin / fig_h
    h = n * row_h / fig_h
    ylim = (-row_h / 2, ys[-1] + row_h / 2)

    fig = plt.figure(figsize=(fig_w, fig_h))
    ax_lbl = fig.add_axes([0, bot, lbl_w / fig_w, h])
    ax_plt = fig.add_axes([lbl_w / fig_w, bot, plt_w / fig_w, h])
    ax_md = fig.add_axes([(lbl_w + plt_w) / fig_w, bot, md_w / fig_w, h])
    ax_ci = fig.add_axes([(lbl_w + plt_w + md_w) / fig_w, bot, ci_w / fig_w, h])

    ax_lbl.set_ylim(*ylim)
    ax_lbl.axis("off")
    ax_lbl.set_title("Treatment", ha="center", fontweight="bold", fontsize=fontsize)
    for i, label in enumerate(labels):
        ax_lbl.text(0.5, ys[i], label, ha="center", va="center", fontsize=fontsize)

    ax_plt.set_ylim(*ylim)
    ax_plt.set_title(f"{ref} minuend", fontweight="bold", fontsize=fontsize)
    for i, row in df.iterrows():
        ax_plt.hlines(
            ys[i], row["lower"], row["upper"], color="dimgray", linewidth=1.5, zorder=3
        )
        ax_plt.plot(row["md"], ys[i], "s", color="dimgray", markersize=7, zorder=3)
    ax_plt.axvline(0, color="black", linewidth=1.0, linestyle="--", zorder=2)
    ax_plt.spines[["left", "top", "right"]].set_visible(False)
    ax_plt.set_yticks([])

    ax_md.set_ylim(*ylim)
    ax_md.axis("off")
    ax_md.set_title("MD", fontweight="bold", fontsize=fontsize)
    for i, s in enumerate(md_strs):
        ax_md.text(0.5, ys[i], s, ha="center", va="center", fontsize=fontsize)

    ax_ci.set_ylim(*ylim)
    ax_ci.axis("off")
    ax_ci.set_title(interval_label, fontweight="bold", fontsize=fontsize)
    for i, s in enumerate(interval_strs):
        ax_ci.text(0.5, ys[i], s, ha="center", va="center", fontsize=fontsize)

    if has_pval:
        ax_p = fig.add_axes(
            [(lbl_w + plt_w + md_w + ci_w) / fig_w, bot, p_w / fig_w, h]
        )
        ax_p.set_ylim(*ylim)
        ax_p.axis("off")
        ax_p.set_title("p-value", fontweight="bold", fontsize=fontsize)
        for i, s in enumerate(p_strs):
            ax_p.text(0.5, ys[i], s, ha="center", va="center", fontsize=fontsize)

    return fig
