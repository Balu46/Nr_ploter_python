# Specyfikacja Projektu: Setup Python do generowania wykresów w stylu nrPlotter

## 1. Wprowadzenie i Cel
Celem projektu jest utworzenie środowiska w języku Python w katalogu `Metody numeryczne`, umożliwiającego generowanie wykresów o wyglądzie i funkcjonalności identycznej jak aplikacja C++ `nrPlotter` (używana w ramach laboratoriów z metod numerycznych na UKSW, opartej o silnik `pbPlots`).

Projekt oferuje podejście hybrydowe:
1. **Silnik `pbPlots` (czysty Python, zero-dependency)** – wierna implementacja biblioteki `pbPlots` w Pythonie, generująca pliki graficzne PNG piksel w piksel identyczne z wersją C++.
2. **Silnik `matplotlib` (zintegrowany ze stylem `nrPlotter`)** – nakładka stylizująca popularną bibliotekę `matplotlib`, która centruje osie na punkcie $(0,0)$, ustawia jasnoszarą siatkę, czcionkę o stałej szerokości (monospace) oraz pozwala na interaktywny podgląd wykresów w oknie (`show=True`) oraz bezpośrednią współpracę z tablicami `numpy`.

---

## 2. Architektura i Struktura Katalogów

Projekt jest zarządzany za pomocą narzędzia `uv` z plikiem konfiguracyjnym `pyproject.toml`.

```text
Metody numeryczne/
├── pyproject.toml                     # Konfiguracja środowiska uv i zależności (numpy, matplotlib, pytest)
├── README.md                          # Zwięzła instrukcja instalacji i przykłady użycia
├── docs/
│   └── superpowers/specs/
│       └── 2026-10-15-nrplotter-python-setup-design.md
├── nrplotter/                         # Główny pakiet biblioteki
│   ├── __init__.py                    # Publiczne API: plot_function, plot_points, plot_series, use_nr_style, Series
│   ├── engine_pbplots.py              # Implementacja backendu opartego o pbPlots
│   ├── engine_matplotlib.py           # Implementacja backendu opartego o Matplotlib
│   ├── style.py                       # Stałe wizualne (paleta barw, domyślne wymiary 640x480, typy linii)
│   └── vendor/                        # Oficjalne moduły pbPlots w czystym Pythonie
│       ├── __init__.py
│       ├── pbPlots.py
│       └── supportLib.py
├── examples/                          # Gotowe szablony zadań laboratoryjnych
│   ├── 01_pbplots_exact.py            # Porównanie 1:1 z nrPlotter (C++)
│   ├── 02_function_plot.py            # Wykres funkcji analitycznej f(x)
│   ├── 03_multi_series.py             # Wiele serii danych na jednym wykresie
│   └── 04_interactive_mpl.py          # Interaktywne okno z Matplotlib
└── tests/
    └── test_nrplotter.py              # Testy automatyczne weryfikujące oba silniki i zapis PNG
```

---

## 3. Szczegóły Komponentów

### 3.1. Moduł `nrplotter.vendor`
- Zawiera oryginalne pliki `pbPlots.py` oraz `supportLib.py` pochodzące ze sprawdzonych źródeł biblioteki `pbPlots`.
- Działa w 100% w czystym standardowym Pythonie 3 (bez bibliotek C i bez dodatkowych pakietów z PyPI).

### 3.2. Moduł `nrplotter.style`
- Definiuje domyślne wartości zgodne z `nrPlotter` C++:
  - Wymiary: szerokość `640` px, wysokość `480` px (lub `800`x`600`).
  - Marginesy (`padding`): `xPadding = width / 20`, `yPadding = height / 20`.
  - Kolory:
    - Tło: białe `#ffffff` (`CreateRGBColor(1.0, 1.0, 1.0)`).
    - Siatka: `#e6e6e6` (`GetGray(0.1)`).
    - Domyślny kolor linii: niebieski `(0.0, 0.0, 1.0)`, zielony `(0.0, 1.0, 0.0)`, czerwony `(1.0, 0.0, 0.0)`.
  - Style linii: `solid`, `dashed`, `dotted`.

### 3.3. Moduł `nrplotter.engine_pbplots`
- Odpowiada za konfigurację `ScatterPlotSettings` i `ScatterPlotSeries`.
- Funkcja `render_pbplots(series_list, title, x_label, y_label, output_path, width, height, auto_boundaries, x_min, x_max, y_min, y_max)`.
- Zapisuje wygenerowane bajty PNG do wskazanego pliku za pośrednictwem `supportLib.WriteToFile`.

### 3.4. Moduł `nrplotter.engine_matplotlib`
- Udostępnia funkcję `use_nr_style()` konfigurującą parametry `plt.rcParams`:
  - Czcionka: `font.family: monospace` (np. DejaVu Sans Mono / Courier).
  - Tło osi i figury: białe `#ffffff`.
  - Siatka: włączona, kolor `#e6e6e6`, styl ciągły lub przerywany, cienka linia (`linewidth=0.75`).
  - Osie: centrowane w punkcie `0` (`ax.spines['left'].set_position(('data', 0))` i `ax.spines['bottom'].set_position(('data', 0))` gdy $0$ mieści się w granicach, w przeciwnym razie przy krawędziach; ramki górna i prawa są ukryte `ax.spines['top'].set_visible(False)`).
- Obsługuje opcjonalny parametr `show=True`, otwierając okno `plt.show()`.

### 3.5. Publiczne API (`nrplotter/__init__.py`)
- Klasa `Series(xs, ys, label="Series", color=(0.0, 0.0, 1.0), line_type="solid")`.
- `plot_function(func, x_min=-10.0, x_max=10.0, num_points=100, title="Function", output_path="plot.png", backend="pbplots", line_type="solid", color=(0.0, 0.0, 1.0), show=False, width=640, height=480)`
- `plot_points(xs, ys, title="Points", output_path="plot.png", backend="pbplots", line_type="solid", color=(1.0, 0.0, 0.0), show=False, width=640, height=480)`
- `plot_series(series_list, title="Plot", output_path="plot.png", backend="pbplots", show=False, width=640, height=480)`
- `use_nr_style()`

---

## 4. Obsługa Błędów i Walidacja
- Zapewnienie równej długości wektorów `xs` i `ys` (rzucenie czytelnego `ValueError` w przypadku niezgodności).
- Rzucenie ostrzeżenia/błędu, jeśli użytkownik zażąda `show=True` przy wybranym backendzie `pbplots` (ponieważ pbPlots jest silnikiem czysto plikowym generującym raster).
- Prawidłowa konwersja typów (obsługa list, krotek, tablic `numpy.ndarray`).

---

## 5. Strategia Weryfikacji i Testy
1. **Testy jednostkowe (`pytest tests/`)**:
   - Sprawdzenie generowania pliku PNG przez backend `pbplots` dla pojedynczej funkcji, punktów i wielu serii.
   - Sprawdzenie generowania pliku PNG przez backend `matplotlib` ze stylem nrPlotter.
   - Sprawdzenie poprawności nagłówka pliku PNG (bajty sygnatury `\x89PNG\r\n\x1a\n`).
2. **Weryfikacja wizualna**:
   - Uruchomienie skryptu `examples/01_pbplots_exact.py` i porównanie wygenerowanego obrazu z referencyjnym `plot.png` z projektu `nr_protter`.
