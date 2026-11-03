from bakery import assert_equal
from dataclasses import dataclass
from drafter import *



@dataclass
class Note:
    pitch: str
    length: int
    position: int

@dataclass
class Measure:
    size: int
    beats: list[Note]
