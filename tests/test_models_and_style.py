import pytest
from nrplotter.models import Series
from nrplotter.style import DEFAULT_WIDTH, DEFAULT_HEIGHT, NRColors

def test_series_validation():
    s = Series(xs=[1, 2, 3], ys=[4, 5, 6], label="test", color=NRColors.BLUE, line_type="solid")
    assert s.xs == [1.0, 2.0, 3.0]
    assert s.ys == [4.0, 5.0, 6.0]

def test_series_mismatched_lengths():
    with pytest.raises(ValueError, match="xs and ys must have the same length"):
        Series(xs=[1, 2], ys=[1])

def test_series_empty_data():
    with pytest.raises(ValueError, match="xs and ys cannot be empty"):
        Series(xs=[], ys=[])
