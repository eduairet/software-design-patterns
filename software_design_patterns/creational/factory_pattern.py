from enum import Enum, auto
from abc import ABC


class Dough(Enum):
    THIN = auto()
    THICK = auto()


class PizzaSize(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    EXTRA_LARGE = auto()


class Pizza(ABC):
    def __init__(self, dough: Dough, size: PizzaSize, toppings: list[str]):
        self.dough = dough
        self.size = size
        self.toppings = toppings

    def prepare(self):
        pass

    def consume(self):
        pass


class ThinCrustPizza(Pizza):
    def consume(self):
        return (
            f"Prepare {self.size.name} thin crust pizza with {', '.join(self.toppings)}"
        )


class ThickCrustPizza(Pizza):
    def consume(self):
        return f"Prepare {self.size.name} thick crust pizza with {', '.join(self.toppings)}"


class ThinCrustPizzaFactory:
    def prepare(self, size: PizzaSize, toppings: list[str]):
        print(f"Prepare {size.name} thin crust pizza")
        return ThinCrustPizza(Dough.THIN, size, toppings)


class ThickCrustPizzaFactory:
    def prepare(self, size: PizzaSize, toppings: list[str]):
        print(f"Prepare {size.name} thick crust pizza")
        return ThickCrustPizza(Dough.THICK, size, toppings)


class Pizzeria:
    factories = []
    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialized = True
            self.factories = [
                eval(f"{dough.name[0]}{dough.name[1:].lower()}CrustPizzaFactory")()
                for dough in Dough
            ]

    def make_pizza(self):
        factory_index = input(
            f"Select the pizza factory: {', '.join([factory.__class__.__name__ for factory in self.factories])}\n"
        )
        factory_index = int(factory_index) - 1

        size = input(
            f"Select pizza size: ({', '.join([size.name for size in PizzaSize])})\n"
        )
        size = eval(f"PizzaSize.{size}")

        toppings = input("Enter toppings separated by comma:\n")
        toppings = toppings.split(", ")

        return self.factories[factory_index].prepare(size, toppings)
