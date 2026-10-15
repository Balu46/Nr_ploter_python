# Metody Numeryczne - nrplotter w Pythonie

Środowisko do generowania wykresów na laboratoria z Metod Numerycznych w stylu aplikacji `nrPlotter` (C++).

## Cechy biblioteki:
1. **Backend `pbplots`**: Czysty Python (zero zależności zewnętrznych), generujący pliki PNG piksel w piksel identyczne z programem `nrPlotter`.
2. **Backend `matplotlib`**: Odtworzony styl wizualny `nrPlotter` (osie wycentrowane w $(0,0)$, siatka `#e6e6e6`, czcionka monospace), obsługa tablic `numpy` i opcja natychmiastowego podglądu okienkowego (`show=True`).

---

## Szybki start

Zarządzanie środowiskiem opiera się na narzędziu `uv`:

```bash
uv sync
```

### Uruchamianie przykładów:
```bash
uv run python examples/01_pbplots_exact.py
uv run python examples/02_function_plot.py
uv run python examples/03_multi_series.py
uv run python examples/04_interactive_mpl.py
```

### Uruchamianie testów:
```bash
uv run pytest
```

---

## Przykłady użycia w kodzie

### 1. Wykres funkcji (czysty pbPlots, identyczny z nrPlotter)
```python
import math
import nrplotter as nr

nr.plot_function(
    func=lambda x: math.sin(x),
    x_min=-2 * math.pi,
    x_max=2 * math.pi,
    num_points=64,
    title="sin(x)",
    output_path="plot_sin.png",
    backend="pbplots",
    color=nr.NRColors.BLUE,
)
```

### 2. Wykres punktów / wielomianu
```python
import nrplotter as nr

nr.plot_points(
    xs=[-2, -1, 0, 1, 2],
    ys=[4, 1, 0, 1, 4],
    title="Parabola",
    output_path="parabola.png",
    backend="pbplots",
    line_type="dashed",
    color=nr.NRColors.RED,
)
```

### 3. Wiele serii na jednym wykresie z Matplotlib
```python
import nrplotter as nr

nr.plot_series([
    nr.Series(xs=[0, 1, 2], ys=[0, 1, 2], label="Metoda A", color=nr.NRColors.BLUE),
    nr.Series(xs=[0, 1, 2], ys=[0, 0.9, 2.1], label="Metoda B", color=nr.NRColors.RED, line_type="dashed"),
], title="Porownanie metod", output_path="porownanie.png", backend="matplotlib", show=False)
```

### 4. Aktywacja stylu nrPlotter w standardowym Matplotlib
```python
import matplotlib.pyplot as plt
import nrplotter as nr

nr.use_nr_style()
plt.plot([-5, 5], [-5, 5])
plt.show()
```
