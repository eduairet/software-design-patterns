from abc import abstractmethod
from enum import Enum
from collections import namedtuple


class Location(Enum):
    OUTDOOR = "Outdoor"
    INDOOR = "Indoor"


class Sport:
    def __init__(self, name: str, location: Location):
        self._name = name
        self._location = location

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def location(self) -> Location:
        return self._location

    @location.setter
    def location(self, location: Location) -> None:
        self._location = location

    @abstractmethod
    def __str__(self) -> str:
        pass


class IndividualSport(Sport):
    def __init__(self, name: str, location: Location):
        super().__init__(name, location)


class IndividualDistanceSport(IndividualSport):
    def __init__(self, name: str, location: Location, distance: int):
        super().__init__(name, location)
        self._distance = distance

    @property
    def distance(self) -> int:
        return self._distance

    @distance.setter
    def distance(self, distance: int) -> None:
        self._distance = distance


class TeamSport(Sport):
    def __init__(self, name: str, number_of_players: int, location: Location):
        super().__init__(name, location)
        self._number_of_players = number_of_players

    @property
    def number_of_players(self) -> int:
        return self._number_of_players

    @number_of_players.setter
    def number_of_players(self, number_of_players: int) -> None:
        self._number_of_players = number_of_players


class SwimmingStyle(Enum):
    FREESTYLE = "Freestyle"
    BACKSTROKE = "Backstroke"
    BREASTSTROKE = "Breaststroke"
    BUTTERFLY = "Butterfly"


class Swimming(IndividualDistanceSport):
    def __init__(
        self,
        location: Location,
        distance: int,
        swimming_style: SwimmingStyle,
    ):
        name = f"Swimming {swimming_style.value}"
        super().__init__(name, location, distance)
        self._swimming_style = swimming_style

    @property
    def swimming_style(self) -> SwimmingStyle:
        return self._swimming_style

    @swimming_style.setter
    def swimming_style(self, swimming_style: SwimmingStyle) -> None:
        self._swimming_style = swimming_style

    def __str__(self) -> str:
        return f"Swimming {self.swimming_style.value} {self.distance} meters"


class RunningType(Enum):
    SPRINT = "Sprint"
    MIDDLE_DISTANCE = "Middle distance"
    LONG_DISTANCE = "Long distance"


class Running(IndividualDistanceSport):
    def __init__(self, location: Location, distance: int):
        running_type = (
            distance < 1000
            and RunningType.SPRINT
            or distance < 5000
            and RunningType.MIDDLE_DISTANCE
            or RunningType.LONG_DISTANCE
        )

        name = f"Running {running_type.value}"
        super().__init__(name, location, distance)

    def __str__(self) -> str:
        return f"Running {self.distance} meters"


class BicycleType(Enum):
    ROAD = "Road"
    MOUNTAIN = "Mountain"
    TRACK = "Track"
    BMX = "BMX"


class Cycling(IndividualDistanceSport):
    def __init__(
        self,
        location: Location,
        distance: int,
        bicycle_type: BicycleType,
    ):
        name = f"Cycling {bicycle_type.value}"
        super().__init__(name, location, distance)
        self._bicycle_type = bicycle_type

    @property
    def bicycle_type(self) -> BicycleType:
        return self._bicycle_type

    @bicycle_type.setter
    def bicycle_type(self, bicycle_type: BicycleType) -> None:
        self._bicycle_type = bicycle_type

    def __str__(self) -> str:
        return f"Cycling {self.bicycle_type.value} {self.distance} meters"


TriathlonDistances = namedtuple(
    "TriathlonDistances", ["swimming", "running", "cycling"]
)
TriathlonDistances.__new__.__defaults__ = (0, 0, 0)


class Triathlon(IndividualDistanceSport):
    def __init__(
        self,
        name: str,
        distances: TriathlonDistances,
        bicycle_type: BicycleType,
    ):
        super().__init__(name, Location.OUTDOOR, sum(distances))
        self.swimming = Swimming(
            self.location, distances.swimming, SwimmingStyle.FREESTYLE
        )
        self.running = Running(self.location, distances.running)
        self.cycling = Cycling(self.location, distances.cycling, bicycle_type)

    def __str__(self) -> str:
        return f"{self.name} with swimming {self.swimming.distance} meters, running {self.running.distance} meters, and cycling {self.cycling.distance} meters"


class RugbyType(Enum):
    SEVENS = {"name": "Sevens", "number_of_players": 7}
    TENS = {"name": "Tens", "number_of_players": 10}
    FIFTEENS = {"name": "Fifteens", "number_of_players": 15}


class Rugby(TeamSport):
    def __init__(
        self,
        type: RugbyType,
    ):
        super().__init__(
            f"Rugby {type.value["name"]}",
            type.value["number_of_players"],
            Location.OUTDOOR,
        )
        self._type = type

    def __str__(self) -> str:
        return f"Rugby with {self.number_of_players} players"
