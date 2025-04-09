from enum import Enum


class MeatType(Enum):
    BEEF = "Beef"
    PORK = "Pork"


class MeatCuts:
    _instances = {}

    @classmethod
    def get_instance(cls, name: str, meat_type: MeatType):
        if meat_type not in cls._instances:
            cls._instances[meat_type] = {}

        if name not in cls._instances[meat_type]:
            cls._instances[meat_type][name] = super().__new__(cls)

        return cls._instances[meat_type][name]

    def __new__(cls, name: str, meat_type: MeatType):
        return cls.get_instance(name, meat_type)


class Cut:
    def __init__(self, name: str, meat_type: MeatType, meat_cuts: MeatCuts):
        self.name = name
        self.meat_type = meat_type
        self.meat_cuts = meat_cuts

    def __str__(self):
        cut = self.meat_cuts.get_instance(self.name, self.meat_type)
        return f"Cut: {cut.name}, Type: {cut.meat_type.value}"


class ButcherShop:
    def __init__(self):
        self.cuts = []

    def add_cut(self, name: str, meat_type: MeatType):
        meat_cuts = MeatCuts.get_instance(name, meat_type)
        cut = Cut(name, meat_type, meat_cuts)
        self.cuts.append(cut)
        return self

    def __str__(self):
        return "\n".join(str(cut) for cut in self.cuts)
