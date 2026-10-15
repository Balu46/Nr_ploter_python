import math
import nrplotter as nr


def f(x: float) -> float:
    """Równanie: x^3 + x^2 - 3x - 3 = 0

    Analitycznie: (x^2 - 3)(x + 1) = 0, więc pierwiastek w [1.0, 3.0] to
    sqrt(3) ~= 1.73205...
    """
    return x**3 + x**2 - 3.0 * x - 3.0


def bsect(
    func, a: float, b: float, tol: float = 0.001, max_iter: int = 100
) -> tuple[float, list[dict]]:
    """Metoda bisekcji poszukująca pierwiastka w przedziale [a, b].

    Zwraca wyznaczony pierwiastek oraz pełną historię kolejnych iteracji.
    """
    fa = func(a)
    fb = func(b)

    if fa * fb > 0:
        raise ValueError(
            f"Funkcja musi mieć przeciwne znaki na krańcach: f({a})={fa}, f({b})={fb}"
        )

    history = []
    print(
        f"{'Iter':<5} | {'a':<10} | {'b':<10} | {'środek (r)':<20} | {'f(r)':<15} | {'szerokość (b-a)':<15}"
    )
    print("-" * 85)

    r = (a + b) / 2.0
    for i in range(1, max_iter + 1):
        r = (a + b) / 2.0
        fr = func(r)
        width = b - a

        history.append(
            {"iter": i, "a": a, "b": b, "r": r, "fr": fr, "width": width}
        )
        print(
            f"{i:<5} | {a:<10.6f} | {b:<10.6f} | {r:<20.16f} | {fr:<15.6e} | {width:<15.6f}"
        )

        # Warunek zbieżności
        if abs(fr) < tol or (b - a) / 2.0 < tol:
            print("-" * 85)
            print(
                f"Zbieżność osiągnięta w iteracji {i}: r = {r:.16f} (dokładne sqrt(3) = {math.sqrt(3):.16f})"
            )
            return r, history

        if fa * fr < 0:
            b = r
            fb = fr
        else:
            a = r
            fa = fr

    print("-" * 85)
    return r, history


def main():
    a, b = 1.0, 3.0
    tol = 0.001

    print("=== METODA BISEKCJI DLA RÓWNANIA: x^3 + x^2 - 3x - 3 = 0 ===")
    print(f"Przedział początkowy: [{a}, {b}], tolerancja: {tol}\n")

    root, history = bsect(f, a, b, tol=tol)

    # Przygotowanie wykresu w stylu nrPlotter
    # Punkty funkcji f(x)
    xs_curve = [0.8 + i * 0.02 for i in range(120)]
    ys_curve = [f(x) for x in xs_curve]

    series_func = nr.Series(
        xs=xs_curve,
        ys=ys_curve,
        label="f(x) = x^3 + x^2 - 3x - 3",
        color=nr.NRColors.BLUE,
        line_type="solid",
        line_thickness=2.0,
    )

    # Punkt pierwiastka r zaznaczony czerwoną kropką na osi
    series_root = nr.Series(
        xs=[root],
        ys=[0.0],
        label=f"Pierwiastek r ≈ {root:.4f}",
        color=nr.NRColors.RED,
        line_thickness=6.0,
    )

    output_file = "bisekcja_rownanie.png"
    nr.plot_series(
        [series_func, series_root],
        title=f"Bisekcja: x^3 + x^2 - 3x - 3 = 0 (r ≈ {root:.4f})",
        output_path=output_file,
        backend="matplotlib",
        show=False,
    )
    print(f"\nWykres w stylu nrPlotter zapisano do: {output_file}")


if __name__ == "__main__":
    main()
