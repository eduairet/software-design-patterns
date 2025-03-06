class Pet:
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    def make_sound(self) -> str:
        pass

    def __str__(self):
        return f"{self.__class__.__name__} {self.name} says {self.make_sound()}"


class Dog(Pet):
    def make_sound(self) -> str:
        return "Woof"


class Cat(Pet):
    def make_sound(self) -> str:
        return "Meow"


class Spider(Pet):
    def make_sound(self) -> str:
        raise Exception("Spiders don't make sounds")


def make_pets_sound(pets: list[Pet]) -> None:
    for pet in pets:
        print(pet)
