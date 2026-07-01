import matplotlib.pyplot as plt
import numpy as np

from .utils import _significance


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


def _grid(data: dict) -> plt.Figure:
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
