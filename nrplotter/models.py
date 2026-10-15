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
