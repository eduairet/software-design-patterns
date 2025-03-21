from software_design_patterns.creational.prototype_pattern import *
import pytest


def test_prototype_hex_color():
    color_factory_no_alpha = ColorFactory()
    color = color_factory_no_alpha.new_hex_color(
        HexValue("ff"), HexValue("00"), HexValue("00")
    )
    assert str(color) == "#ff0000"

    color_factory_alpha = ColorFactory()
    color = color_factory_alpha.new_hex_color(
        HexValue("ff"), HexValue("00"), HexValue("00"), Alpha(0.5)
    )
    assert str(color) == "#ff00007f"


def test_prototype_hex_color_error():
    color_factory = ColorFactory()

    with pytest.raises(ValueError, match="Invalid hex value"):
        color_factory.new_hex_color(HexValue("zz"), HexValue("00"), HexValue("00"))


def test_prototype_hex_alpha_error():
    color_factory = ColorFactory()

    with pytest.raises(ValueError, match="Invalid alpha value"):
        color_factory.new_hex_color(
            HexValue("ff"), HexValue("00"), HexValue("00"), Alpha(1.5)
        )


def test_prototype_hex_deep_copy():
    red, green, blue, alpha = HexValue("ff"), HexValue("00"), HexValue("00"), Alpha(0.5)

    color_factory = ColorFactory()
    color = color_factory.new_hex_color(red, green, blue, alpha)

    red.value = "00"
    color.alpha.value = 0.6

    assert str(red) != str(color.red)
    assert str(green) == str(color.green)
    assert str(blue) == str(color.blue)
    assert str(alpha) != str(color.alpha)


def test_prototype_rgb_color():
    color_factory_no_alpha = ColorFactory()
    color = color_factory_no_alpha.new_rgb_color(
        RgbValue(255), RgbValue(0), RgbValue(0)
    )
    assert str(color) == "rgb(255, 0, 0)"

    color_factory_alpha = ColorFactory()
    color = color_factory_alpha.new_rgb_color(
        RgbValue(255), RgbValue(0), RgbValue(0), Alpha(0.5)
    )
    assert str(color) == "rgba(255, 0, 0, 0.5)"


def test_prototype_rgb_color_error():
    color_factory = ColorFactory()

    with pytest.raises(ValueError, match="Invalid RGB value"):
        color_factory.new_rgb_color(RgbValue(256), RgbValue(0), RgbValue(0))


def test_prototype_rgb_alpha_error():
    color_factory = ColorFactory()

    with pytest.raises(ValueError, match="Invalid alpha value"):
        color_factory.new_rgb_color(RgbValue(255), RgbValue(0), RgbValue(0), Alpha(1.5))


def test_prototype_rgb_deep_copy():
    red, green, blue, alpha = RgbValue(255), RgbValue(0), RgbValue(0), Alpha(0.5)

    color_factory = ColorFactory()
    color = color_factory.new_rgb_color(red, green, blue, alpha)

    red.value = 0
    color.alpha.value = 0.6

    assert str(red) != str(color.red)
    assert str(green) == str(color.green)
    assert str(blue) == str(color.blue)
    assert str(alpha) != str(color.alpha)
