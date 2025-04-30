from software_design_patterns.behavioral.strategy_pattern import *


def test_strategy_red_wine():
    wine_server = WineServer(WineType.RED)
    assert wine_server.execute_strategy() == (
        "Serve at 16-18°C\n"
        "Let it breathe for 30 minutes\n"
        "Serve Red wine in a Standard Red cup"
    )


def test_strategy_white_wine():
    wine_server = WineServer(WineType.WHITE)
    assert wine_server.execute_strategy() == (
        "Serve at 8-10°C\n" "Serve White wine in a Blanc cup"
    )


def test_strategy_sparkling_wine():
    wine_server = WineServer(WineType.SPARKLING)
    assert wine_server.execute_strategy() == (
        "Serve at 6-8°C\n" "Serve Sparkling wine in a Flute cup"
    )


def test_strategy_invalid_wine_type():
    try:
        WineServer("INVALID")
    except ValueError as e:
        assert str(e) == "Unknown wine type"
