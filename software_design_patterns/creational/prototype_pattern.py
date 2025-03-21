import copy
from abc import ABC, abstractmethod
import re


class HexValue:
    def __init__(self, value: str):
        if not re.match(r"^[0-9A-Fa-f]+$", value):
            raise ValueError("Invalid hex value")
        self.value = value

    def __str__(self):
        return self.value


class RgbValue:
    def __init__(self, value: int):
        if value < 0 or value > 255:
            raise ValueError("Invalid RGB value")
        self.value = value

    def __str__(self):
        return str(self.value)


class Alpha:
    def __init__(self, value: float):
        if value < 0 or value > 1:
            raise ValueError("Invalid alpha value")
        self.value = value

    def __str__(self):
        return str(self.value)


class Color(ABC):
    def __init__(self):
        self.red = None
        self.green = None
        self.blue = None
        self.alpha = None

    @abstractmethod
    def set_red(self, value):
        pass

    @abstractmethod
    def set_green(self, value):
        pass

    @abstractmethod
    def set_blue(self, value):
        pass

    @abstractmethod
    def set_alpha(self, value):
        pass


class HexColor(Color):
    def __init__(self):
        super().__init__()

    def set_red(self, red: HexValue):
        self.red = red
        return self

    def set_green(self, green: HexValue):
        self.green = green
        return self

    def set_blue(self, blue: HexValue):
        self.blue = blue
        return self

    def set_alpha(self, alpha: Alpha):
        self.alpha = alpha
        return self

    def __str__(self):
        red = self.red or HexValue("00")
        green = self.green or HexValue("00")
        blue = self.blue or HexValue("00")
        alpha = self.alpha or Alpha(1)
        alpha_hex = (
            format(int(255 * float(alpha.value)), "02x") if alpha.value < 1 else ""
        )
        return f"#{red}{green}{blue}{alpha_hex}"


class RgbColor(Color):
    def __init__(self):
        super().__init__()

    def set_red(self, red: RgbValue):
        self.red = red
        return self

    def set_green(self, green: RgbValue):
        self.green = green
        return self

    def set_blue(self, blue: RgbValue):
        self.blue = blue
        return self

    def set_alpha(self, alpha: Alpha):
        self.alpha = alpha
        return self

    def __str__(self):
        red = self.red or RgbValue(0)
        green = self.green or RgbValue(0)
        blue = self.blue or RgbValue(0)
        alpha = self.alpha or Alpha(1)
        alpha_rgb = (
            f"{self.alpha.value:.1f}" if self.alpha and self.alpha.value < 1 else None
        )
        return (
            f"rgba({red}, {green}, {blue}, {alpha_rgb})"
            if self.alpha
            else f"rgb({red}, {green}, {blue})"
        )


class ColorFactory:
    hex_color_prototype = (
        HexColor()
        .set_red(HexValue("00"))
        .set_green(HexValue("00"))
        .set_blue(HexValue("00"))
        .set_alpha(Alpha(1))
    )
    rgb_color_prototype = (
        RgbColor()
        .set_red(RgbValue(0))
        .set_green(RgbValue(0))
        .set_blue(RgbValue(0))
        .set_alpha(Alpha(1))
    )

    @staticmethod
    def __new_color(proto, red, green, blue, alpha: Alpha = None):
        return (
            copy.deepcopy(proto)
            .set_red(copy.deepcopy(red))
            .set_green(copy.deepcopy(green))
            .set_blue(copy.deepcopy(blue))
            .set_alpha(copy.deepcopy(alpha))
        )

    @staticmethod
    def new_hex_color(
        red: HexValue, green: HexValue, blue: HexValue, alpha: Alpha = None
    ):
        return ColorFactory.__new_color(
            ColorFactory.hex_color_prototype, red, green, blue, alpha
        )

    @staticmethod
    def new_rgb_color(
        red: RgbValue, green: RgbValue, blue: RgbValue, alpha: Alpha = None
    ):
        return ColorFactory.__new_color(
            ColorFactory.rgb_color_prototype, red, green, blue, alpha
        )
