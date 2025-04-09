from enum import Enum
from typing import Dict, Any


class MeatType(Enum):
    BEEF = "Beef"
    PORK = "Pork"


class MeatCuts:
    _instances: Dict[MeatType, Dict[str, Any]] = {}

    @classmethod
    def get_instance(cls, name: str, meat_type: MeatType):
        meat_dict = cls._instances.setdefault(meat_type, {})

        if name not in meat_dict:
            meat_dict[name] = super().__new__(cls)

        return meat_dict[name]

    def __new__(cls, name: str, meat_type: MeatType):
        return cls.get_instance(name, meat_type)


class Cut:
    def __init__(self, name: str, meat_type: MeatType):
        self.name = name
        self.meat_type = meat_type
        self.meat_cut = MeatCuts(name, meat_type)

    def __str__(self):
        return f"Cut: {self.name}, Type: {self.meat_type.value}"


class ButcherShop:
    def __init__(self):
        self.cuts = []

    def add_cut(self, name: str, meat_type: MeatType):
        self.cuts.append(Cut(name, meat_type))
        return self

    def __str__(self):
        return "\n".join(str(cut) for cut in self.cuts)
