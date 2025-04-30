from abc import ABC
from enum import Enum


class GrindSize(Enum):
    FINE = "fine"
    MEDIUM = "medium"
    COARSE = "coarse"


class ExtractMethod(Enum):
    DRIP = "Drip"
    FRENCH_PRESS = "French Press"
    ESPRESSO = "Espresso"


GRIND_SIZE = {
    ExtractMethod.DRIP: GrindSize.MEDIUM,
    ExtractMethod.FRENCH_PRESS: GrindSize.COARSE,
    ExtractMethod.ESPRESSO: GrindSize.FINE,
}


class Coffee(ABC):
    def __init__(self, extract_method: ExtractMethod):
        self.extract_method = extract_method
        self._ready = False

    def prepare(self) -> str:
        message = f"{self.grind()}\n"
        message += f"{self.brew()}\n"
        self._ready = True
        message += f"{str(self)}"
        return message

    def grind(self) -> str:
        pass

    def brew(self) -> str:
        pass

    def pour(self) -> str:
        pass

    def prepare_new_batch(self) -> None:
        pass

    @property
    def can_refill(self) -> bool:
        pass

    @property
    def ready(self) -> bool:
        return self._ready

    @ready.setter
    def ready(self, value: bool) -> None:
        self._ready = value

    def __str__(self) -> str:
        return f"Coffee prepared using {self.extract_method.value} method"


class DripCoffee(Coffee):
    def __init__(self):
        super().__init__(ExtractMethod.DRIP)
        self.cups = 8
        self.served_cups = 0

    def grind(self) -> str:
        return f"Grinding coffee beans to {GRIND_SIZE[self.extract_method].value} size"

    def brew(self) -> str:
        return "\n".join(
            [
                "Add filter to the coffee maker",
                "Add coffee grounds to the filter",
                "Fill the water reservoir",
                "Turn on the coffee maker",
                "Wait for the coffee to brew",
            ]
        )

    def pour(self) -> str:
        if not self.ready:
            return "Coffee is not ready yet, wait until the water from the reservoir has dripped through the coffee grounds"
        if self.can_refill:
            self.served_cups += 1
            return f"Pouring cup {self.served_cups} of coffee in a large mug"
        else:
            return "No more cups to pour, clean the coffee maker, replace the filter, and refill it with coffee grounds and water"

    def prepare_new_batch(self) -> None:
        if self.can_refill:
            raise ValueError(
                "You can only prepare a new batch when the coffee maker is empty"
            )
        self.cups *= 2
        self._ready = False
        return self.prepare()

    @property
    def can_refill(self) -> bool:
        return self.served_cups < self.cups


class FrenchPressCoffee(Coffee):
    def __init__(self):
        super().__init__(ExtractMethod.FRENCH_PRESS)
        self.cups = 4
        self.served_cups = 0

    def grind(self) -> str:
        return f"Grinding coffee beans to {GRIND_SIZE[self.extract_method].value} size"

    def brew(self) -> str:
        return "\n".join(
            [
                "Add coffee grounds to the French press",
                "Add hot water to the French press",
                "Stir the mixture",
                "Let it steep for 4 minutes",
                "Press the plunger down",
            ]
        )

    def pour(self) -> str:
        if not self.ready:
            return "Coffee is still brewing, wait until the coffee looks pretty dark"
        if self.can_refill:
            self.served_cups += 1
            return f"Pouring cup {self.served_cups} of coffee in a medium mug"
        else:
            return "The press ran out of coffee, please refill it with water and coffee grounds"

    def prepare_new_batch(self) -> None:
        if self.can_refill:
            raise ValueError(
                "The French press is not empty, please pour all the coffee before preparing a new batch"
            )
        self.cups *= 2
        self._ready = False
        return self.prepare()

    @property
    def can_refill(self) -> bool:
        return self.served_cups < self.cups


class EspressoCoffee(Coffee):
    def __init__(self):
        super().__init__(ExtractMethod.ESPRESSO)
        self.poured = False

    def grind(self) -> str:
        return f"{GRIND_SIZE[self.extract_method].value.capitalize()} grinding the coffee beans for a great espresso"

    def brew(self) -> str:
        return "\n".join(
            [
                "Add 18g of coffee grounds to the espresso machine portafilter",
                "Fill the water reservoir",
                "Turn on the espresso machine",
                "Place your cup under the portafilter",
            ]
        )

    def pour(self) -> str:
        if not self.ready:
            return "Your espresso machine is not correctly set up, please check the water reservoir and the coffee grounds"
        if self.poured:
            return "You already poured your espresso, please clean the portafilter and refill it with coffee grounds and water"
        self.poured = True
        return "Pouring a single shot of espresso in a small cup"

    def prepare_new_batch(self) -> None:
        if not self.poured:
            raise ValueError(
                "You can only prepare a new batch after pouring the espresso"
            )
        self.poured = False
        self._ready = False
        return self.prepare()

    @property
    def can_refill(self) -> bool:
        return False
