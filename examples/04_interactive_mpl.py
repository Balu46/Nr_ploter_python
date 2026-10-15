import nrplotter as nr

def main():
    xs = [-3, -2, -1, 0, 1, 2, 3]
    ys = [9, 4, 1, 0, 1, 4, 9]
    nr.plot_points(xs, ys, title="Interaktywny podgląd", output_path="example_interactive.png", backend="matplotlib", show=False)
    print("Wygenerowano example_interactive.png (użyj show=True, aby otworzyć okno)")

if __name__ == "__main__":
    main()
