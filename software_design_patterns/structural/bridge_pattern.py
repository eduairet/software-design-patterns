from abc import ABC, abstractmethod
from typing import List


class Cooker(ABC):
    @abstractmethod
    def cook(self, taco: "Taco") -> str:
        pass


class FriedCooker(Cooker):
    def cook(self, taco: "Taco") -> str:
        toppings = f" then add {taco.toppings_str}" if taco.toppings else ""
        return f"Frying {taco.name} taco{toppings}."


class GrilledCooker(Cooker):
    def cook(self, taco: "Taco") -> str:
        toppings = f" then add {taco.toppings_str}" if taco.toppings else ""
        return f"Grilling {taco.name} taco{toppings}."


class Taco(ABC):
    def __init__(self, name: str, cooker: Cooker):
        self.name = name
        self.cooker = cooker
        self.toppings: List[str] = []

    def add_toppings(self, *toppings: str) -> "Taco":
        self.toppings.extend(toppings)
        return self

    @property
    def toppings_str(self) -> str:
        return ", ".join(self.toppings)

    def __str__(self) -> str:
        return self.cooker.cook(self)


class CarnitasTaco(Taco):
    def __init__(self):
        super().__init__("carnitas", FriedCooker())


class AsadaTaco(Taco):
    def __init__(self):
        super().__init__("asada", GrilledCooker())
