import matplotlib.pyplot as plt


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
