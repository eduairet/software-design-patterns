from software_design_patterns.structural.bridge_pattern import *


def test_bridge_taco():
    TACO_CARNITAS_EXPECTED = "Frying carnitas taco then add cilantro, guacamole."
    TACO_ASADA_EXPECTED = (
        "Grilling asada taco then add chiles toreados, cebolla rostizada."
    )

    taco = CarnitasTaco().add_toppings("cilantro", "guacamole")
    assert str(taco) == TACO_CARNITAS_EXPECTED

    taco = AsadaTaco().add_toppings("chiles toreados", "cebolla rostizada")
    assert str(taco) == TACO_ASADA_EXPECTED
