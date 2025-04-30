import pytest
from software_design_patterns.behavioral.template_method_pattern import *


def test_template_method_drip_coffee():
    EXPECTED_PREPARATION = (
        "Grinding coffee beans to medium size\n"
        "Add filter to the coffee maker\n"
        "Add coffee grounds to the filter\n"
        "Fill the water reservoir\n"
        "Turn on the coffee maker\n"
        "Wait for the coffee to brew\n"
        "Coffee prepared using Drip method"
    )
    coffee = DripCoffee()
    assert coffee.prepare() == EXPECTED_PREPARATION
    assert coffee.ready is True

    assert coffee.cups == 8
    assert coffee.served_cups == 0
    assert coffee.can_refill is True

    coffee.pour()
    assert coffee.served_cups == 1

    with pytest.raises(
        ValueError,
        match="You can only prepare a new batch when the coffee maker is empty",
    ):
        coffee.prepare_new_batch()

    for _ in range(7):
        coffee.pour()
    assert coffee.served_cups == 8
    assert coffee.can_refill is False

    coffee.prepare_new_batch()
    coffee.pour()
    assert coffee.served_cups == 9


def test_template_method_french_press():
    EXPECTED_PREPARATION = (
        "Grinding coffee beans to coarse size\n"
        "Add coffee grounds to the French press\n"
        "Add hot water to the French press\n"
        "Stir the mixture\n"
        "Let it steep for 4 minutes\n"
        "Press the plunger down\n"
        "Coffee prepared using French Press method"
    )
    coffee = FrenchPressCoffee()
    assert coffee.prepare() == EXPECTED_PREPARATION
    assert coffee.ready is True

    assert coffee.cups == 4
    assert coffee.served_cups == 0
    assert coffee.can_refill is True

    coffee.pour()
    assert coffee.served_cups == 1
    with pytest.raises(
        ValueError,
        match="The French press is not empty, please pour all the coffee before preparing a new batch",
    ):
        coffee.prepare_new_batch()

    for _ in range(3):
        coffee.pour()
    assert coffee.served_cups == 4
    assert coffee.can_refill is False

    coffee.prepare_new_batch()
    coffee.pour()
    assert coffee.served_cups == 5


def test_template_method_espresso_coffee():
    EXPECTED_PREPARATION = (
        "Fine grinding the coffee beans for a great espresso\n"
        "Add 18g of coffee grounds to the espresso machine portafilter\n"
        "Fill the water reservoir\n"
        "Turn on the espresso machine\n"
        "Place your cup under the portafilter\n"
        "Coffee prepared using Espresso method"
    )
    coffee = EspressoCoffee()
    assert coffee.prepare() == EXPECTED_PREPARATION
    assert coffee.ready is True
    assert coffee.poured is False

    with pytest.raises(
        ValueError,
        match="You can only prepare a new batch after pouring the espresso",
    ):
        coffee.prepare_new_batch()

    coffee.pour()
    assert coffee.poured is True

    coffee.prepare_new_batch()
    assert coffee.poured is False
    coffee.pour()
    assert coffee.poured is True
