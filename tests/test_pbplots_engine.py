import os
from pathlib import Path
from nrplotter.models import Series
from nrplotter.engine_pbplots import render_pbplots
from nrplotter.style import NRColors

def test_render_pbplots_single_series(tmp_path):
    output_png = tmp_path / "test_pb.png"
    s = Series(xs=[-2, 0, 2], ys=[4, 0, 4], label="parabola", color=NRColors.RED, line_type="dashed")
    result_path = render_pbplots([s], title="Test", output_path=str(output_png))
    
    assert os.path.exists(result_path)
    with open(result_path, "rb") as f:
        header = f.read(8)
        assert header == b"\x89PNG\r\n\x1a\n"
