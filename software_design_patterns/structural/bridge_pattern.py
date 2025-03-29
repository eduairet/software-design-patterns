from abc import ABC, abstractmethod
from typing import List


class Cooker(ABC):
    @abstractmethod
    def cook(self, taco: "Taco") -> str:
        pass


class CookerFried(Cooker):
    def cook(self, taco: "Taco") -> str:
        return f"Frying {taco.name} taco{f' then add {taco.toppings_str}' if taco.toppings else ''}."


class CookerGrilled(Cooker):
    def cook(self, taco: "Taco") -> str:
        return f"Grilling {taco.name} taco{f' then add {taco.toppings_str}' if taco.toppings else ''}."


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


class TacoCarnitas(Taco):
    def __init__(self):
        super().__init__("carnitas", CookerFried())


class TacoAsada(Taco):
    def __init__(self):
        super().__init__("asada", CookerGrilled())
