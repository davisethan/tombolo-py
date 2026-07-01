import matplotlib.pyplot as plt


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
