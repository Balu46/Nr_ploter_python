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
