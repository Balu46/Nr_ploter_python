def test_vendor_pbplots_importable():
    from nrplotter.vendor import pbPlots, supportLib
    image_ref = pbPlots.CreateRGBABitmapImageReference()
    assert image_ref is not None
