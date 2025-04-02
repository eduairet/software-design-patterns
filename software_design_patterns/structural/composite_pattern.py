from abc import ABC, abstractmethod
from enum import Enum


class Subconscious(ABC):
    @abstractmethod
    def operation(self):
        pass


class DreamType(Enum):
    NIGHTMARE = "Nightmare"
    DAYDREAM = "Daydream"
    LUCID = "Lucid Dream"


class Dream(Subconscious):
    def __init__(self, type: DreamType):
        self.name = "Dream"
        self.type = type

    def operation(self):
        return f"Dreaming in {self.type.value.lower()} mode"


class HallucinationType(Enum):
    VISUAL = "Visual"
    AUDITORY = "Auditory"
    TACTILE = "Tactile"


class Hallucination(Subconscious):
    def __init__(self, type: HallucinationType):
        self.name = "Hallucination"
        self.type = type

    def operation(self):
        return f"Experiencing {self.type.value.lower()} hallucination"


class SubconsciousComposite(Subconscious):
    def __init__(self):
        self.subconscious_elements = []
        self.name = "Composite Subconscious"

    def add(self, subconscious: Subconscious):
        self.subconscious_elements.append(subconscious)

    def remove(self, subconscious: Subconscious):
        self.subconscious_elements.remove(subconscious)

    def operation(self):
        results = [
            subconscious.operation() for subconscious in self.subconscious_elements
        ]
        return f"{self.name}: " + ", ".join(results)
