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
