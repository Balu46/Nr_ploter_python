from typing import Sequence, Optional
from nrplotter.models import Series
from nrplotter.vendor import pbPlots, supportLib
from nrplotter.style import DEFAULT_WIDTH, DEFAULT_HEIGHT

def render_pbplots(
    series_list: Sequence[Series],
    title: str = "Plot",
    x_label: str = "X axis",
    y_label: str = "Y axis",
    output_path: str = "plot.png",
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    auto_boundaries: bool = True,
    x_min: Optional[float] = None,
    x_max: Optional[float] = None,
    y_min: Optional[float] = None,
    y_max: Optional[float] = None,
) -> str:
    if not series_list:
        raise ValueError("series_list cannot be empty")

    plot_series_objs = []
    for s in series_list:
        sp_series = pbPlots.GetDefaultScatterPlotSeriesSettings()
        sp_series.xs = list(s.xs)
        sp_series.ys = list(s.ys)
        sp_series.linearInterpolation = True
        sp_series.lineType = s.line_type
        sp_series.lineThickness = float(s.line_thickness)
        sp_series.color = pbPlots.CreateRGBColor(s.color[0], s.color[1], s.color[2])
        plot_series_objs.append(sp_series)

    settings = pbPlots.GetDefaultScatterPlotSettings()
    settings.width = float(width)
    settings.height = float(height)
    settings.title = title
    settings.xLabel = x_label
    settings.yLabel = y_label
    settings.scatterPlotSeries = plot_series_objs

    if auto_boundaries and (x_min is None or x_max is None or y_min is None or y_max is None):
        settings.autoBoundaries = True
    else:
        settings.autoBoundaries = False
        settings.xMin = float(x_min) if x_min is not None else -10.0
        settings.xMax = float(x_max) if x_max is not None else 10.0
        settings.yMin = float(y_min) if y_min is not None else -10.0
        settings.yMax = float(y_max) if y_max is not None else 10.0

    settings.autoPadding = False
    settings.xPadding = float(width // 20)
    settings.yPadding = float(height // 20)

    image_ref = pbPlots.CreateRGBABitmapImageReference()
    error_message = pbPlots.StringReference()
    success = pbPlots.DrawScatterPlotFromSettings(image_ref, settings, error_message)

    if not success:
        err = "".join(error_message.string) if error_message.string else "Unknown pbPlots error"
        raise RuntimeError(f"pbPlots failed to generate plot: {err}")

    png_data = pbPlots.ConvertToPNG(image_ref.image)
    supportLib.WriteToFile(png_data, output_path)
    pbPlots.DeleteImage(image_ref.image)
    return output_path
