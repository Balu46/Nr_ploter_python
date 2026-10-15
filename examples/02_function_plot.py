import math
import nrplotter as nr

def main():
    nr.plot_function(lambda x: math.sin(x), x_min=-2*math.pi, x_max=2*math.pi, num_points=64, title="sin(x)", output_path="example_sin.png", backend="pbplots", color=nr.NRColors.BLUE)
    print("Wykres funkcji zapisany w example_sin.png")

if __name__ == "__main__":
    main()
