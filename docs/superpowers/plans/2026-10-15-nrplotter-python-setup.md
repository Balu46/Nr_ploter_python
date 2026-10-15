# nrPlotter Python Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Utworzenie w katalogu `Metody numeryczne` środowiska Python zarządzanego przez `uv` z pakietem `nrplotter`, który umożliwia generowanie wykresów identycznych z aplikacją `nrPlotter` (C++) za pomocą czystego `pbPlots` oraz backendu `matplotlib` ze stylem nrPlotter.

**Architecture:** Modułowa architektura z pakietem `nrplotter` zawierającym: warstwę vendor (`pbPlots`), definicje stylów i struktur (`Series`), backend `pbplots`, backend `matplotlib` oraz zunifikowane API funkcyjne (`plot_function`, `plot_points`, `plot_series`).

**Tech Stack:** Python 3, `uv`, `pbPlots` (czysty Python, zero-dependency), `matplotlib`, `numpy`, `pytest`.

**Spec:** [docs/superpowers/specs/2026-10-15-nrplotter-python-setup-design.md](file:///home/jan/magazyn/Projekty/studia/Metody%20numeryczne/docs/superpowers/specs/2026-10-15-nrplotter-python-setup-design.md)

## Global Constraints

- Komendy terminala prezentowane użytkownikowi muszą być w dokładnie jednej linijce (single-line).
- Brak zbędnych plików konfiguracyjnych agenta w repozytorium.
- Czysty podział na zadania zgodny z TDD (failing test -> pass -> commit).

## Review Focus

1. Nierówne długości list `xs` i `ys` — rzucenie czytelnego `ValueError` zamiast cichego ucięcia lub indeksowania poza zakresem.
2. Przekazanie pustych danych (`xs=[]`, `ys=[]`) — rzucenie `ValueError` lub wygenerowanie czystego wykresu bez awarii procesu.
3. Zażądanie `show=True` przy backendzie `pbplots` — rzucenie `ValueError` z jasnym komunikatem, że podgląd okienkowy wymaga `backend="matplotlib"`.
4. Obsługa tablic `numpy.ndarray` oraz floatów — automatyczna konwersja do list floatów przed przekazaniem do `pbPlots`.
5. Prawidłowy zapis nagłówka PNG (`\x89PNG\r\n\x1a\n`) dla obu backendów na dysku.

---

### Task 1: Konfiguracja środowiska `uv` i modułu `nrplotter.vendor`

**Files:**
- Create: `pyproject.toml`
- Create: `nrplotter/__init__.py`
- Create: `nrplotter/vendor/__init__.py`
- Create: `nrplotter/vendor/pbPlots.py` (skopiowane z `../nr_protter/build/_deps/pbplots_fetch-src/Python/pbPlots.py`)
- Create: `nrplotter/vendor/supportLib.py` (skopiowane z `../nr_protter/build/_deps/pbplots_fetch-src/Python/supportLib.py`)
- Test: `tests/test_vendor_import.py`

**Interfaces:**
- Consumes: Pliki źródłowe `pbPlots.py` i `supportLib.py` z `../nr_protter`.
- Produces: Importowalny pakiet `nrplotter.vendor.pbPlots` i `nrplotter.vendor.supportLib`.

- [ ] **Step 1: Write the failing test**

Utwórz `tests/test_vendor_import.py`:
```python
def test_vendor_pbplots_importable():
    from nrplotter.vendor import pbPlots, supportLib
    image_ref = pbPlots.CreateRGBABitmapImageReference()
    assert image_ref is not None
```

- [ ] **Step 2: Run test to verify it fails**

Uruchom: `uv run pytest tests/test_vendor_import.py -v`
Oczekiwany rezultat: FAIL z komunikatem `ModuleNotFoundError: No module named 'nrplotter'`.

- [ ] **Step 3: Write minimal implementation**

Utwórz `pyproject.toml`:
```toml
[project]
name = "metody-numeryczne"
version = "0.1.0"
description = "Metody numeryczne - zestaw narzędzi i wykresów w stylu nrPlotter"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "matplotlib>=3.8.0",
    "numpy>=1.26.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
]
```

Skopiuj `pbPlots.py` i `supportLib.py` do `nrplotter/vendor/`, utwórz `nrplotter/__init__.py` i `nrplotter/vendor/__init__.py`.

- [ ] **Step 4: Run test to verify it passes**

Uruchom: `uv run pytest tests/test_vendor_import.py -v`
Oczekiwany rezultat: PASS.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml nrplotter tests/test_vendor_import.py && git commit -m "feat: scaffold uv project and vendor pbPlots"
```

---

### Task 2: Moduł stylów i struktury danych (`style.py`, `models.py`)

**Files:**
- Create: `nrplotter/models.py`
- Create: `nrplotter/style.py`
- Test: `tests/test_models_and_style.py`

**Interfaces:**
- Consumes: Standardowe typy Pythona, `numpy`.
- Produces: `Series(xs, ys, label, color, line_type, line_thickness)`, stałe wymiarów i kolorów w `style.py`.

- [ ] **Step 1: Write the failing test**

Utwórz `tests/test_models_and_style.py`:
```python
import pytest
from nrplotter.models import Series
from nrplotter.style import DEFAULT_WIDTH, DEFAULT_HEIGHT, NRColors

def test_series_validation():
    s = Series(xs=[1, 2, 3], ys=[4, 5, 6], label="test", color=NRColors.BLUE, line_type="solid")
    assert s.xs == [1.0, 2.0, 3.0]
    assert s.ys == [4.0, 5.0, 6.0]

def test_series_mismatched_lengths():
    with pytest.raises(ValueError, match="xs and ys must have the same length"):
        Series(xs=[1, 2], ys=[1])

def test_series_empty_data():
    with pytest.raises(ValueError, match="xs and ys cannot be empty"):
        Series(xs=[], ys=[])
```

- [ ] **Step 2: Run test to verify it fails**

Uruchom: `uv run pytest tests/test_models_and_style.py -v`
Oczekiwany rezultat: FAIL z błędem braku modułu `nrplotter.models`.

- [ ] **Step 3: Write minimal implementation**

Zaimplementuj `nrplotter/style.py`:
```python
from dataclasses import dataclass

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480

@dataclass(frozen=True)
class NRColors:
    WHITE: tuple[float, float, float] = (1.0, 1.0, 1.0)
    BLACK: tuple[float, float, float] = (0.0, 0.0, 0.0)
    GRID_GRAY: tuple[float, float, float] = (0.9, 0.9, 0.9)
    BLUE: tuple[float, float, float] = (0.0, 0.0, 1.0)
    GREEN: tuple[float, float, float] = (0.0, 1.0, 0.0)
    RED: tuple[float, float, float] = (1.0, 0.0, 0.0)
```

Zaimplementuj `nrplotter/models.py`:
```python
from dataclasses import dataclass, field
from typing import Sequence, Any
from nrplotter.style import NRColors

@dataclass
class Series:
    xs: list[float]
    ys: list[float]
    label: str = "Series"
    color: tuple[float, float, float] = NRColors.BLUE
    line_type: str = "solid"
    line_thickness: float = 2.0

    def __post_init__(self):
        self.xs = [float(x) for x in self.xs]
        self.ys = [float(y) for y in self.ys]
        if len(self.xs) == 0 or len(self.ys) == 0:
            raise ValueError("xs and ys cannot be empty")
        if len(self.xs) != len(self.ys):
            raise ValueError(f"xs and ys must have the same length ({len(self.xs)} != {len(self.ys)})")
```

- [ ] **Step 4: Run test to verify it passes**

Uruchom: `uv run pytest tests/test_models_and_style.py -v`
Oczekiwany rezultat: PASS.

- [ ] **Step 5: Commit**

```bash
git add nrplotter/style.py nrplotter/models.py tests/test_models_and_style.py && git commit -m "feat: add style constants and Series model"
```

---

### Task 3: Backend pbPlots (`engine_pbplots.py`)

**Files:**
- Create: `nrplotter/engine_pbplots.py`
- Test: `tests/test_pbplots_engine.py`

**Interfaces:**
- Consumes: `nrplotter.models.Series`, `nrplotter.vendor.pbPlots`, `nrplotter.vendor.supportLib`.
- Produces: `render_pbplots(series_list, title, x_label, y_label, output_path, width, height, auto_boundaries, x_min, x_max, y_min, y_max) -> str`.

- [ ] **Step 1: Write the failing test**

Utwórz `tests/test_pbplots_engine.py`:
```python
import os
from pathlib import Path
from nrplotter.models import Series
from nrplotter.engine_pbplots import render_pbplots
from nrplotter.style import NRColors

def test_render_pbplots_single_series(tmp_path):
    output_png = tmp_path / "test_pb.png"
    s = Series(xs=[-2, 0, 2], ys=[4, 0, 4], label="parabola", color=NRColors.RED, line_type="dashed")
    result_path = render_pbplots([s], title="Test", output_path=str(output_png))
    
    assert os.path.exists(result_path)
    with open(result_path, "rb") as f:
        header = f.read(8)
        assert header == b"\x89PNG\r\n\x1a\n"
```

- [ ] **Step 2: Run test to verify it fails**

Uruchom: `uv run pytest tests/test_pbplots_engine.py -v`
Oczekiwany rezultat: FAIL z błędem braku modułu `nrplotter.engine_pbplots`.

- [ ] **Step 3: Write minimal implementation**

Zaimplementuj `nrplotter/engine_pbplots.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Uruchom: `uv run pytest tests/test_pbplots_engine.py -v`
Oczekiwany rezultat: PASS.

- [ ] **Step 5: Commit**

```bash
git add nrplotter/engine_pbplots.py tests/test_pbplots_engine.py && git commit -m "feat: implement pbplots rendering engine"
```

---

### Task 4: Backend Matplotlib i Styl nrPlotter (`engine_matplotlib.py`)

**Files:**
- Create: `nrplotter/engine_matplotlib.py`
- Test: `tests/test_matplotlib_engine.py`

**Interfaces:**
- Consumes: `nrplotter.models.Series`, `matplotlib.pyplot`.
- Produces: `use_nr_style()`, `render_matplotlib(...)`.

- [ ] **Step 1: Write the failing test**

Utwórz `tests/test_matplotlib_engine.py`:
```python
import os
from nrplotter.models import Series
from nrplotter.engine_matplotlib import render_matplotlib, use_nr_style
from nrplotter.style import NRColors

def test_render_matplotlib_png(tmp_path):
    output_png = tmp_path / "test_mpl.png"
    s = Series(xs=[-5, 0, 5], ys=[-10, 0, 10], label="line", color=NRColors.BLUE)
    result_path = render_matplotlib([s], title="MPL Test", output_path=str(output_png), show=False)
    
    assert os.path.exists(result_path)
    with open(result_path, "rb") as f:
        header = f.read(8)
        assert header == b"\x89PNG\r\n\x1a\n"
```

- [ ] **Step 2: Run test to verify it fails**

Uruchom: `uv run pytest tests/test_matplotlib_engine.py -v`
Oczekiwany rezultat: FAIL z błędem braku modułu `nrplotter.engine_matplotlib`.

- [ ] **Step 3: Write minimal implementation**

Zaimplementuj `nrplotter/engine_matplotlib.py`:
```python
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

        ax.plot(s.xs, s.ys, label=s.label, color=s.color, linestyle=line_style, linewidth=s.line_thickness)

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
```

- [ ] **Step 4: Run test to verify it passes**

Uruchom: `uv run pytest tests/test_matplotlib_engine.py -v`
Oczekiwany rezultat: PASS.

- [ ] **Step 5: Commit**

```bash
git add nrplotter/engine_matplotlib.py tests/test_matplotlib_engine.py && git commit -m "feat: implement matplotlib engine with nrPlotter styling"
```

---

### Task 5: Zunifikowane Publiczne API (`nrplotter/__init__.py`)

**Files:**
- Modify: `nrplotter/__init__.py`
- Test: `tests/test_public_api.py`

**Interfaces:**
- Produces: `plot_function`, `plot_points`, `plot_series`, `use_nr_style`, `Series`, `NRColors`.

- [ ] **Step 1: Write the failing test**

Utwórz `tests/test_public_api.py`:
```python
import math
import os
import pytest
import nrplotter as nr

def test_plot_function_pbplots(tmp_path):
    out = tmp_path / "sin_pb.png"
    res = nr.plot_function(lambda x: math.sin(x), x_min=-math.pi, x_max=math.pi, num_points=50, output_path=str(out), backend="pbplots")
    assert os.path.exists(res)

def test_plot_function_matplotlib(tmp_path):
    out = tmp_path / "sin_mpl.png"
    res = nr.plot_function(lambda x: math.sin(x), x_min=-math.pi, x_max=math.pi, num_points=50, output_path=str(out), backend="matplotlib")
    assert os.path.exists(res)

def test_plot_points_validation():
    with pytest.raises(ValueError, match="show=True is not supported for pbplots backend"):
        nr.plot_points([1, 2], [3, 4], backend="pbplots", show=True)
```

- [ ] **Step 2: Run test to verify it fails**

Uruchom: `uv run pytest tests/test_public_api.py -v`
Oczekiwany rezultat: FAIL z błędem braku funkcji w `nrplotter`.

- [ ] **Step 3: Write minimal implementation**

Zaktualizuj `nrplotter/__init__.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Uruchom: `uv run pytest tests/test_public_api.py -v`
Oczekiwany rezultat: PASS.

- [ ] **Step 5: Commit**

```bash
git add nrplotter/__init__.py tests/test_public_api.py && git commit -m "feat: export unified public API for nrplotter"
```

---

### Task 6: Przykłady laboratoryjne, dokumentacja i weryfikacja końcowa

**Files:**
- Create: `examples/01_pbplots_exact.py`
- Create: `examples/02_function_plot.py`
- Create: `examples/03_multi_series.py`
- Create: `examples/04_interactive_mpl.py`
- Create: `README.md`

- [ ] **Step 1: Write example scripts**

Utwórz `examples/01_pbplots_exact.py`:
```python
import nrplotter as nr

def main():
    xs = [-2, -1, 0, 1, 2]
    ys = [2, -1, -2, -1, 2]
    nr.plot_points(xs, ys, title="x^2-2 (Exact pbPlots)", output_path="example_pbplots.png", backend="pbplots", line_type="dotted", color=nr.NRColors.GREEN)
    print("Wykres zapisany w example_pbplots.png")

if __name__ == "__main__":
    main()
```

Utwórz `examples/02_function_plot.py`:
```python
import math
import nrplotter as nr

def main():
    nr.plot_function(lambda x: math.sin(x), x_min=-2*math.pi, x_max=2*math.pi, num_points=64, title="sin(x)", output_path="example_sin.png", backend="pbplots", color=nr.NRColors.BLUE)
    print("Wykres funkcji zapisany w example_sin.png")

if __name__ == "__main__":
    main()
```

Utwórz `examples/03_multi_series.py`:
```python
import math
import nrplotter as nr

def main():
    xs = [i * 0.1 for i in range(-50, 51)]
    ys_sin = [math.sin(x) for x in xs]
    ys_cos = [math.cos(x) for x in xs]

    nr.plot_series([
        nr.Series(xs, ys_sin, label="sin(x)", color=nr.NRColors.BLUE, line_type="solid"),
        nr.Series(xs, ys_cos, label="cos(x)", color=nr.NRColors.RED, line_type="dashed"),
    ], title="sin(x) vs cos(x)", output_path="example_multi.png", backend="matplotlib")
    print("Wykres wielu serii zapisany w example_multi.png")

if __name__ == "__main__":
    main()
```

Utwórz `examples/04_interactive_mpl.py`:
```python
import nrplotter as nr

def main():
    xs = [-3, -2, -1, 0, 1, 2, 3]
    ys = [9, 4, 1, 0, 1, 4, 9]
    nr.plot_points(xs, ys, title="Interaktywny podgląd", output_path="example_interactive.png", backend="matplotlib", show=False)
    print("Wygenerowano example_interactive.png (użyj show=True, aby otworzyć okno)")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create README.md**

Utwórz `README.md` z opisem uruchamiania przez `uv run python examples/...`.

- [ ] **Step 3: Run full test suite and verify examples**

Uruchom:
```bash
uv run pytest && uv run python examples/01_pbplots_exact.py && uv run python examples/02_function_plot.py && uv run python examples/03_multi_series.py
```
Oczekiwany rezultat: Wszystkie testy zdane (PASS), pliki PNG wygenerowane bez błędów.

- [ ] **Step 4: Commit**

```bash
git add examples README.md && git commit -m "docs: add examples and README for nrplotter setup"
```
