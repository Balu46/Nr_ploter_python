from typing import Callable, Sequence, Optional, Union
from nrplotter.models import Series
from nrplotter.style import NRColors, DEFAULT_WIDTH, DEFAULT_HEIGHT
from nrplotter.engine_pbplots import render_pbplots
from nrplotter.engine_matplotlib import render_matplotlib, use_nr_style

def plot_series(
    series_list: Sequence[Series],
    title: str = "Plot",
    output_path: str = "plot.png",
    backend: str = "pbplots",
    show: bool = False,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    x_min: Optional[float] = None,
    x_max: Optional[float] = None,
    y_min: Optional[float] = None,
    y_max: Optional[float] = None,
) -> str:
    if backend == "pbplots":
        if show:
            raise ValueError("show=True is not supported for pbplots backend. Use backend='matplotlib' for interactive window display.")
        return render_pbplots(
            series_list=series_list,
            title=title,
            output_path=output_path,
            width=width,
            height=height,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
    elif backend == "matplotlib":
        return render_matplotlib(
            series_list=series_list,
            title=title,
            output_path=output_path,
            width=width,
            height=height,
            show=show,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
    else:
        raise ValueError(f"Unknown backend '{backend}'. Supported backends: 'pbplots', 'matplotlib'")

def plot_function(
    func: Callable[[float], float],
    x_min: float = -10.0,
    x_max: float = 10.0,
    num_points: int = 100,
    title: str = "Function",
    output_path: str = "plot.png",
    backend: str = "pbplots",
    line_type: str = "solid",
    color: tuple[float, float, float] = NRColors.BLUE,
    line_thickness: float = 2.0,
    show: bool = False,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
) -> str:
    step = (x_max - x_min) / max(num_points, 1)
    xs = [x_min + i * step for i in range(num_points + 1)]
    ys = [func(x) for x in xs]
    series = Series(xs=xs, ys=ys, label=title, color=color, line_type=line_type, line_thickness=line_thickness)
    return plot_series([series], title=title, output_path=output_path, backend=backend, show=show, width=width, height=height)

def plot_points(
    xs: Sequence[Union[int, float]],
    ys: Sequence[Union[int, float]],
    title: str = "Points",
    output_path: str = "plot.png",
    backend: str = "pbplots",
    line_type: str = "solid",
    color: tuple[float, float, float] = NRColors.RED,
    line_thickness: float = 2.0,
    show: bool = False,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
) -> str:
    series = Series(xs=list(xs), ys=list(ys), label=title, color=color, line_type=line_type, line_thickness=line_thickness)
    return plot_series([series], title=title, output_path=output_path, backend=backend, show=show, width=width, height=height)

__all__ = [
    "Series",
    "NRColors",
    "plot_function",
    "plot_points",
    "plot_series",
    "use_nr_style",
]
