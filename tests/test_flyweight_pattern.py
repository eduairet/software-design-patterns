from software_design_patterns.structural.flyweight_pattern import *


def test_flyweight_meat_cuts():
    butcher_shop = ButcherShop()

    butcher_shop.add_cut("Ribeye", MeatType.BEEF).add_cut(
        "Tenderloin", MeatType.BEEF
    ).add_cut("Pork Chop", MeatType.PORK).add_cut("Pork Belly", MeatType.PORK)

    EXPECTED_OUTPUT = (
        "Cut: Ribeye, Type: Beef\n"
        "Cut: Tenderloin, Type: Beef\n"
        "Cut: Pork Chop, Type: Pork\n"
        "Cut: Pork Belly, Type: Pork"
    )

    assert str(butcher_shop) == EXPECTED_OUTPUT
