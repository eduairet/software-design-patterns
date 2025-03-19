from software_design_patterns.creational.factory_pattern import *
from unittest.mock import patch

SIZE = PizzaSize.MEDIUM
TOPPINGS = ["cheese", "pepperoni"]
THIN_EXPECTED = f"Prepare {SIZE.name} thin crust pizza with {', '.join(TOPPINGS)}"
THICK_EXPECTED = f"Prepare {SIZE.name} thick crust pizza with {', '.join(TOPPINGS)}"


@patch("builtins.input")
def test_factory_thin_crust_pizza(mock_input):
    mock_input.side_effect = ["1", "MEDIUM", "cheese, pepperoni"]

    pizzeria = Pizzeria()
    thin_crust_pizza = pizzeria.make_pizza()

    assert thin_crust_pizza.dough == Dough.THIN
    assert thin_crust_pizza.size == SIZE
    assert thin_crust_pizza.toppings == TOPPINGS
    assert thin_crust_pizza.consume() == THIN_EXPECTED


@patch("builtins.input")
def test_factory_thick_crust_pizza(mock_input):
    mock_input.side_effect = ["2", "MEDIUM", "cheese, pepperoni"]

    pizzeria = Pizzeria()
    thick_crust_pizza = pizzeria.make_pizza()

    assert thick_crust_pizza.dough == Dough.THICK
    assert thick_crust_pizza.size == SIZE
    assert thick_crust_pizza.toppings == TOPPINGS
    assert thick_crust_pizza.consume() == THICK_EXPECTED
