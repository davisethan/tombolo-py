import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plottable import ColumnDefinition, Table


def _significance(pval):
    if pval < 0.001:
        return "***"
    if pval < 0.01:
        return "**"
    if pval < 0.05:
        return "*"
    if pval < 0.1:
        return "."
    return ""


def _text_width(strings: list[str], fontsize: float, pad: float = 0.1) -> float:
    fig = plt.figure()
    texts = [fig.text(0, 0, s, fontsize=fontsize) for s in strings]
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    px_per_in = fig.bbox.width / fig.get_figwidth()
    max_in = max(t.get_window_extent(renderer).width for t in texts) / px_per_in
    plt.close(fig)
    return max_in + pad


def _forest(data: dict, ref: str, interval_label: str = "[95% CI]") -> plt.Figure:
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


def _barh(data: dict) -> plt.Figure:
    pipelines = sorted(data, key=data.get)
    values = [data[p] for p in pipelines]

    n = len(pipelines)
    row_height = 0.5
    fontsize = row_height * 24
    linewidth = row_height * 1.8

    fig, ax = plt.subplots(figsize=(6, n * row_height + 1))
    bars = ax.barh(pipelines, values, color="dimgray")

    ax.bar_label(bars, fmt="{:.3f}", padding=4, fontsize=fontsize)
    ax.tick_params(labelsize=fontsize, width=linewidth)
    for spine in ax.spines.values():
        spine.set_linewidth(linewidth)

    ax.set_xlim(0, 1)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    return fig


def _grid(data: dict) -> plt.Figure:
    def _cell(data, row, col):
        arr = []
        if "md" in data:
            md = data["md"][row][col]
            arr.append(f"{md:+.4f}")
        if "lower" in data and "upper" in data:
            lo = data["lower"][row][col]
            hi = data["upper"][row][col]
            arr.append(f"[{lo:.4f}, {hi:.4f}]")
        if "pval" in data:
            p = data["pval"][row][col]
            arr.append(f"p={p:.4f}")
            arr.append(_significance(p))
        return "\n".join(arr)

    pipelines = list(next(iter(data.values())).keys())
    n = len(pipelines)

    text_arr = np.array(
        [[_cell(data, r, c) if r != c else r for c in pipelines] for r in pipelines]
    )

    cell_size = 2.2
    linewidth = cell_size * 0.9
    fontsize = cell_size * 6.5

    fig, ax = plt.subplots(figsize=(n * cell_size, n * cell_size))
    ax.set_xlim(0, n)
    ax.set_ylim(n, 0)

    for i in range(n):
        for j in range(n):
            kw = {"fontweight": "bold"} if i == j else {}
            ax.text(
                j + 0.5,
                i + 0.5,
                text_arr[i, j],
                ha="center",
                va="center",
                fontsize=fontsize,
                **kw,
            )

    for k in range(1, n):
        ax.axhline(k, color="black", linewidth=linewidth)
        ax.axvline(k, color="black", linewidth=linewidth)

    ax.add_patch(
        plt.Rectangle(
            (0, 0),
            n,
            n,
            edgecolor="black",
            facecolor="gainsboro",
            linewidth=linewidth,
            clip_on=False,
        )
    )

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    fig.tight_layout()
    return fig


def _table(data: dict) -> plt.Figure:
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
