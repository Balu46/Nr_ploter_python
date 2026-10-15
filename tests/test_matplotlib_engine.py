import os
from nrplotter.models import Series
from nrplotter.engine_matplotlib import render_matplotlib, use_nr_style
from nrplotter.style import NRColors

def test_render_matplotlib_png(tmp_path):
    output_png = tmp_path / "test_mpl.png"
    s = Series(xs=[-5, 0, 5], ys=[-10, 0, 10], label="line", color=NRColors.BLUE)
    result_path = render_matplotlib([s], title="MPL Test", output_path=str(output_png), show=False)
    
    assert os.path.exists(result_path)
    with open(result_path, "rb") as f:
        header = f.read(8)
        assert header == b"\x89PNG\r\n\x1a\n"
