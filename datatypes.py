import enum
import logging
from dataclasses import dataclass
import settings


@dataclass
class Coordinates:
    """Just coordinates"""
    latitude: float
    longitude: float


class PollutionTypeDangerLevel(enum.Enum):
    PM10 = 50
    PM25 = 25
    PM1 = 15


class PollutionType:
    def __init__(self, name: str, value: float):
        self.name = name
        self.value = value

    def is_acceptable(self) -> bool:
        acceptable = self.value < PollutionTypeDangerLevel[self.name].value
        if not acceptable or settings.DEBUG:
            logging.info("%s acceptable level: %s: %s", 'Passed' if acceptable else 'Not', self.name, self.value)
        return acceptable

