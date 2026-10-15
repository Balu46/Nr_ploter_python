import math
import os
import pytest
import nrplotter as nr

def test_plot_function_pbplots(tmp_path):
    out = tmp_path / "sin_pb.png"
    res = nr.plot_function(lambda x: math.sin(x), x_min=-math.pi, x_max=math.pi, num_points=50, output_path=str(out), backend="pbplots")
    assert os.path.exists(res)

def test_plot_function_matplotlib(tmp_path):
    out = tmp_path / "sin_mpl.png"
    res = nr.plot_function(lambda x: math.sin(x), x_min=-math.pi, x_max=math.pi, num_points=50, output_path=str(out), backend="matplotlib")
    assert os.path.exists(res)

def test_plot_points_validation():
    with pytest.raises(ValueError, match="show=True is not supported for pbplots backend"):
        nr.plot_points([1, 2], [3, 4], backend="pbplots", show=True)
