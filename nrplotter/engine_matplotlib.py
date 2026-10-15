from typing import Sequence, Optional
import matplotlib.pyplot as plt
from nrplotter.models import Series
from nrplotter.style import DEFAULT_WIDTH, DEFAULT_HEIGHT

def use_nr_style():
    plt.rcParams["font.family"] = "monospace"
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"
    plt.rcParams["grid.color"] = "#e6e6e6"
    plt.rcParams["grid.linestyle"] = "-"
    plt.rcParams["grid.linewidth"] = 0.8
    plt.rcParams["axes.edgecolor"] = "#333333"

def render_matplotlib(
    series_list: Sequence[Series],
    title: str = "Plot",
    x_label: str = "X axis",
    y_label: str = "Y axis",
    output_path: str = "plot.png",
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    show: bool = False,
    auto_boundaries: bool = True,
    x_min: Optional[float] = None,
    x_max: Optional[float] = None,
    y_min: Optional[float] = None,
    y_max: Optional[float] = None,
) -> str:
    use_nr_style()
    dpi = 100
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)

    all_xs = [x for s in series_list for x in s.xs]
    all_ys = [y for s in series_list for y in s.ys]
    min_x = x_min if x_min is not None else min(all_xs)
    max_x = x_max if x_max is not None else max(all_xs)
    min_y = y_min if y_min is not None else min(all_ys)
    max_y = y_max if y_max is not None else max(all_ys)
    for s in series_list:
        line_style = "-"
        if s.line_type == "dashed":
            line_style = "--"
        elif s.line_type == "dotted":
            line_style = ":"

        marker = "o" if len(s.xs) == 1 else None
        markersize = 8 if len(s.xs) == 1 else None
        ax.plot(s.xs, s.ys, label=s.label, color=s.color, linestyle=line_style, linewidth=s.line_thickness, marker=marker, markersize=markersize)

    ax.grid(True)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=9)
    ax.set_ylabel(y_label, fontsize=9)

    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    # Centrowanie osi na (0,0) jeśli 0 mieści się w zakresie (dokładnie jak w pbPlots)
    if min_x < 0.0 < max_x:
        ax.spines["left"].set_position(("data", 0))
    else:
        ax.spines["left"].set_position(("axes", 0))

    if min_y < 0.0 < max_y:
        ax.spines["bottom"].set_position(("data", 0))
    else:
        ax.spines["bottom"].set_position(("axes", 0))

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if len(series_list) > 1 or any(s.label != "Series" for s in series_list):
        ax.legend(frameon=True, facecolor="white", edgecolor="#cccccc", fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi)

    if show:
        plt.show()

    plt.close(fig)
    return output_path
