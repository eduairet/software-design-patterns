from abc import ABC, abstractmethod
from enum import Enum


class WineType(Enum):
    RED = "Red"
    WHITE = "White"
    SPARKLING = "Sparkling"


class WineCupType(Enum):
    STANDARD_RED = "Standard Red"
    BLANC = "Blanc"
    FLUTE = "Flute"


class WineStrategy(ABC):
    @abstractmethod
    def temp(self) -> str:
        pass

    def oxygen(self) -> str:
        return ""

    def serve(self, wine_type: WineType) -> str:
        cup_mapping = {
            WineType.RED: WineCupType.STANDARD_RED,
            WineType.WHITE: WineCupType.BLANC,
            WineType.SPARKLING: WineCupType.FLUTE,
        }
        cup = cup_mapping[wine_type]
        return f"Serve {wine_type.value} wine in a {cup.value} cup"


class RedWineStrategy(WineStrategy):
    def temp(self) -> str:
        return "Serve at 16-18°C"

    def oxygen(self) -> str:
        return "Let it breathe for 30 minutes"


class WhiteWineStrategy(WineStrategy):
    def temp(self) -> str:
        return "Serve at 8-10°C"


class SparklingWineStrategy(WineStrategy):
    def temp(self) -> str:
        return "Serve at 6-8°C"


class WineServer:
    def __init__(self, wine_type: WineType):
        self.wine_type = wine_type
        self.strategy = self.get_strategy(wine_type)

    def get_strategy(self, wine_type: WineType) -> WineStrategy:
        strategy_mapping = {
            WineType.RED: RedWineStrategy(),
            WineType.WHITE: WhiteWineStrategy(),
            WineType.SPARKLING: SparklingWineStrategy(),
        }
        return strategy_mapping.get(wine_type, ValueError("Unknown wine type"))

    def execute_strategy(self) -> str:
        temp = self.strategy.temp()
        oxygen = self.strategy.oxygen()
        serve = self.strategy.serve(self.wine_type)
        instructions = [i for i in [temp, oxygen, serve] if i]
        return "\n".join(instructions)
