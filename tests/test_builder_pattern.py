from software_design_patterns.creational.builder_pattern import *

FONT_FAMILY = "Helvetica"
FONT_STYLE = "sans-serif"
FONT_WEIGHT = 400
FONT_VERSION = "1.0"
UNITS_PER_EM = 1000
X_HEIGHT = 500
CAP_HEIGHT = 700
ASCENDER = 800
DESCENDER = 200
ITALIC_ANGLE = 0
GLYPH_A_NAME, GLYPH_A_UNICODE = "A", "U+0041"
GLYPH_B_NAME, GLYPH_B_UNICODE = "B", "U+0042"
FONT_INFO_EXPECTED = f"FontInfo:\n\tFamily name: {FONT_FAMILY}\n\tStyle name: {FONT_STYLE}\n\tWeight: {FONT_WEIGHT}\n\tVersion: {FONT_VERSION}"
METRICS_EXPECTED = f"Metrics:\n\tUPM: {UNITS_PER_EM}\n\tX height: {X_HEIGHT}\n\tCap height: {CAP_HEIGHT}\n\tAscender: {ASCENDER}\n\tDescender: {DESCENDER}\n\tItalic angle: {ITALIC_ANGLE}"
GLYPHS_EXPECTED_LENGTH = 2
GLYPHS_EXPECTED = f"Glyph: {GLYPH_A_NAME} | Unicode: {GLYPH_A_UNICODE}, Glyph: {GLYPH_B_NAME} | Unicode: {GLYPH_B_UNICODE}"
FONT_EXPECTED = (
    f"Font:\n{FONT_INFO_EXPECTED}\n{METRICS_EXPECTED}\nGlyphs:\n\t{GLYPHS_EXPECTED}"
)


def test_builder_font_info():
    font_builder = FontInfoBuilder()

    test = (
        font_builder.named(FONT_FAMILY)
        .styled(FONT_STYLE)
        .with_weight(FONT_WEIGHT)
        .with_version(FONT_VERSION)
        .build()
    )

    assert test.font_info.family_name == FONT_FAMILY
    assert test.font_info.style_name == FONT_STYLE
    assert test.font_info.weight == FONT_WEIGHT
    assert test.font_info.version == FONT_VERSION

    assert str(test.font_info) == FONT_INFO_EXPECTED


def test_builder_font_metrics():
    font_builder = MetricsBuilder()

    test = (
        font_builder.with_units_per_em(UNITS_PER_EM)
        .with_x_height(X_HEIGHT)
        .with_cap_height(CAP_HEIGHT)
        .with_ascender(ASCENDER)
        .with_descender(DESCENDER)
        .with_italic_angle(ITALIC_ANGLE)
        .build()
    )

    assert test.metrics.units_per_em == UNITS_PER_EM
    assert test.metrics.x_height == X_HEIGHT
    assert test.metrics.cap_height == CAP_HEIGHT
    assert test.metrics.ascender == ASCENDER
    assert test.metrics.descender == DESCENDER
    assert test.metrics.italic_angle == ITALIC_ANGLE

    assert str(test.metrics) == METRICS_EXPECTED


def test_builder_font_glyphs():
    font_builder = GlyphBuilder()

    test = (
        font_builder.add_glyph(GLYPH_A_NAME, GLYPH_A_UNICODE)
        .add_glyph(GLYPH_B_NAME, GLYPH_B_UNICODE)
        .build()
    )

    assert len(test.glyphs) == GLYPHS_EXPECTED_LENGTH
    assert test.glyphs[0].name == GLYPH_A_NAME
    assert test.glyphs[0].unicode == GLYPH_A_UNICODE
    assert test.glyphs[1].name == GLYPH_B_NAME
    assert test.glyphs[1].unicode == GLYPH_B_UNICODE

    assert str(", ".join([str(g) for g in test.glyphs])) == GLYPHS_EXPECTED


def test_builder_font_complete():
    font_builder = CompleteFontBuilder()

    test = (
        font_builder.named(FONT_FAMILY)
        .styled(FONT_STYLE)
        .with_weight(FONT_WEIGHT)
        .with_version(FONT_VERSION)
        .with_units_per_em(UNITS_PER_EM)
        .with_x_height(X_HEIGHT)
        .with_cap_height(CAP_HEIGHT)
        .with_ascender(ASCENDER)
        .with_descender(DESCENDER)
        .with_italic_angle(ITALIC_ANGLE)
        .add_glyph(GLYPH_A_NAME, GLYPH_A_UNICODE)
        .add_glyph(GLYPH_B_NAME, GLYPH_B_UNICODE)
        .build()
    )

    assert test.font_info.family_name == FONT_FAMILY
    assert test.font_info.style_name == FONT_STYLE
    assert test.font_info.weight == FONT_WEIGHT
    assert test.font_info.version == FONT_VERSION
    assert test.metrics.units_per_em == UNITS_PER_EM
    assert test.metrics.x_height == X_HEIGHT
    assert test.metrics.cap_height == CAP_HEIGHT
    assert test.metrics.ascender == ASCENDER
    assert test.metrics.descender == DESCENDER
    assert test.metrics.italic_angle == ITALIC_ANGLE
    assert len(test.glyphs) == GLYPHS_EXPECTED_LENGTH
    assert test.glyphs[0].name == GLYPH_A_NAME
    assert test.glyphs[0].unicode == GLYPH_A_UNICODE
    assert test.glyphs[1].name == GLYPH_B_NAME
    assert test.glyphs[1].unicode == GLYPH_B_UNICODE

    assert str(test) == FONT_EXPECTED
