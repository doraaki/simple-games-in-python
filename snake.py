import pygame
from dataclasses import dataclass
from __future__ import annotations
from typing import List
from enum import Enum
import time
pygame.init()

@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

class Orientation(Enum):
    NORTH = 1
    WEST  = 2
    SOUTH = 3
    EAST  = 4

    def left(self) -> Orientation:
        return Orientation((self.value + 1) % 4)
    
    def right(self) -> Orientation:
        return Orientation((self.value + 1) % 4)




class Snake:
    def __init__(self,
                 body_parts: List[Point],
                 orientation: Orientation):
        self.body_parts = body_parts
        self.orientation = orientation