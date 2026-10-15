import math
import nrplotter as nr


def bsect(func, a: float, b: float, tol: float = 0.001, max_iter: int = 100) -> float:
    """Metoda bisekcji (równego podziału) znajdująca pierwiastek f(x) = 0 w [a, b]."""
    fa = func(a)
    fb = func(b)

    if fa * fb > 0:
        raise ValueError(
            f"Funkcja musi mieć przeciwne znaki na krańcach: f({a})={fa}, f({b})={fb}"
        )

    for i in range(max_iter):
        mid = (a + b) / 2.0
        fmid = func(mid)

        # Sprawdzenie warunku stopu
        if abs(fmid) < tol or (b - a) / 2.0 < tol:
            print(f"Znaleziono pierwiastek px = {mid:.6f} po {i + 1} iteracjach.")
            return mid

        if fa * fmid < 0:
            b = mid
            fb = fmid
        else:
            a = mid
            fa = fmid

    print(f"Osiągnięto limit iteracji. Przybliżony pierwiastek: {mid:.6f}")
    return (a + b) / 2.0


def main():
    # 1. Zdefiniuj funkcję badaną w zadaniu (np. x^2 - 2, x^3 - x - 2 itp.)
    # Zmień poniższe wyrażenie na wzór podany w treści zadania na Moodle:
    f = lambda x: x**2 - 2.0

    a, b = 1.0, 3.0
    tol = 0.001

    # 2. Obliczenie pierwiastka metodą bisekcji (odpowiednik bsect w C++)
    px = bsect(f, a, b, tol)
    print(f"Wyznaczony punkt: Vertex({px:.4f}, 0.0)")

    # 3. Przygotowanie serii do wykresu:
    # a) Wykres ciągły badanej funkcji f(x)
    xs_func = [0.5 + i * 0.02 for i in range(150)]  # zakres wokół pierwiastka
    ys_func = [f(x) for x in xs_func]

    # b) Wyznaczony punkt (px, 0.0) - odpowiada v w C++ dodawanemu do points_
    # Wokół px dodajemy mały znacznik/punkt
    series_func = nr.Series(
        xs_func,
        ys_func,
        label="f(x)",
        color=nr.NRColors.BLUE,
        line_type="solid",
        line_thickness=2.0,
    )

    series_root = nr.Series(
        [px],
        [0.0],
        label=f"Pierwiastek px={px:.3f}",
        color=nr.NRColors.RED,
        line_type="dotted",
        line_thickness=5.0,
    )

    # 4. Generowanie wykresu w stylu nrPlotter
    # backend="matplotlib" z show=True pozwala na natychmiastowy podgląd w oknie
    nr.plot_series(
        [series_func, series_root],
        title=f"Bisekcja: px = {px:.3f}",
        output_path="wykres_bisekcja.png",
        backend="matplotlib",
        show=False,
    )
    print("Wykres został zapisany do pliku: wykres_bisekcja.png")


if __name__ == "__main__":
    main()
