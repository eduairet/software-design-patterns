from enum import Enum


class KnifeSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Knife:
    def __init__(self, size: KnifeSize):
        self.size = size


class SwissKnife:
    def __init__(
        self,
        size: KnifeSize,
        knife: bool,
        can_opener: bool,
        screw_driver: bool,
        scissors: bool,
        nail_file: bool,
    ):
        self.size = size
        self.knife = knife
        self.can_opener = can_opener
        self.screw_driver = screw_driver
        self.scissors = scissors
        self.nail_file = nail_file


class KnifeToSwissKnifeAdapter:
    def __init__(
        self,
        knife: Knife,
        can_opener: bool = False,
        screw_driver: bool = False,
        scissors: bool = False,
        nail_file: bool = False,
    ):
        self._knife = knife
        self.knife = True
        self.can_opener = can_opener
        self.screw_driver = screw_driver
        self.scissors = scissors
        self.nail_file = nail_file

    @property
    def size(self):
        return self._knife.size

    def __str__(self):
        return f"Knife: {self._knife.size.name.lower()}, can_opener: {self.can_opener}, screw_driver: {self.screw_driver}, scissors: {self.scissors}, nail_file: {self.nail_file}"
