class FontInfo:
    def __init__(self):
        self.family_name = None
        self.style_name = None
        self.weight = None
        self.version = None

    def __str__(self):
        return (
            f"FontInfo:\n"
            f"\tFamily name: {self.family_name}\n"
            f"\tStyle name: {self.style_name}\n"
            f"\tWeight: {self.weight}\n"
            f"\tVersion: {self.version}"
        )


class Metrics:
    def __init__(self):
        self.units_per_em = None
        self.x_height = None
        self.cap_height = None
        self.ascender = None
        self.descender = None
        self.italic_angle = None

    def __str__(self):
        return (
            f"Metrics:\n"
            f"\tUPM: {self.units_per_em}\n"
            f"\tX height: {self.x_height}\n"
            f"\tCap height: {self.cap_height}\n"
            f"\tAscender: {self.ascender}\n"
            f"\tDescender: {self.descender}\n"
            f"\tItalic angle: {self.italic_angle}"
        )


class Glyph:
    def __init__(self, name=None, unicode=None):
        self.name = name
        self.unicode = unicode

    def __str__(self):
        return f"Glyph: {self.name} | Unicode: {self.unicode}"


class Font:
    def __init__(self):
        self.font_info = None or FontInfo()
        self.metrics = None or Metrics()
        self.glyphs = []

    def __str__(self):
        return (
            f"Font:\n"
            f"{self.font_info}\n"
            f"{self.metrics}\n"
            f"Glyphs:\n"
            f"\t{', '.join([str(g) for g in self.glyphs])}"
        )

    @staticmethod
    def new():
        return FontBuilder()


class FontBuilder:
    def __init__(self):
        self.font = Font()

    def build(self):
        return self.font


class FontInfoBuilder(FontBuilder):
    def named(self, family_name):
        self.font.font_info.family_name = family_name
        return self

    def styled(self, style_name):
        self.font.font_info.style_name = style_name
        return self

    def with_weight(self, weight):
        self.font.font_info.weight = weight
        return self

    def with_version(self, version):
        self.font.font_info.version = version
        return self


class MetricsBuilder(FontBuilder):
    def with_units_per_em(self, units_per_em):
        self.font.metrics.units_per_em = units_per_em
        return self

    def with_x_height(self, x_height):
        self.font.metrics.x_height = x_height
        return self

    def with_cap_height(self, cap_height):
        self.font.metrics.cap_height = cap_height
        return self

    def with_ascender(self, ascender):
        self.font.metrics.ascender = ascender
        return self

    def with_descender(self, descender):
        self.font.metrics.descender = descender
        return self

    def with_italic_angle(self, italic_angle):
        self.font.metrics.italic_angle = italic_angle
        return self


class GlyphBuilder(FontBuilder):
    def add_glyph(self, name, unicode):
        glyph = Glyph(name, unicode)
        self.font.glyphs.append(glyph)
        return self


class CompleteFontBuilder(FontInfoBuilder, MetricsBuilder, GlyphBuilder):
    pass
