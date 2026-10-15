import nrplotter as nr

def main():
    xs = [-2, -1, 0, 1, 2]
    ys = [2, -1, -2, -1, 2]
    nr.plot_points(xs, ys, title="x^2-2 (Exact pbPlots)", output_path="example_pbplots.png", backend="pbplots", line_type="dotted", color=nr.NRColors.GREEN)
    print("Wykres zapisany w example_pbplots.png")

if __name__ == "__main__":
    main()
