from __future__ import annotations
import pygame
from dataclasses import dataclass
from typing import List
from enum import Enum
from collections import deque
import time
pygame.init()

WHITE_RGB = (255,255,255)
BLACK_RGB = (0,0,0)

@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other) -> Coordinate:
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> Coordinate:
        return Coordinate(self.x - other.x, self.y - other.y)

class Orientation(Enum):
    NORTH = 1
    WEST  = 2
    SOUTH = 3
    EAST  = 4

    def left(self) -> Orientation:
        return Orientation((self.value + 1) % 4)
    
    def right(self) -> Orientation:
        return Orientation((self.value + 3) % 4)

class Snake:
    def __init__(self,
                 body_parts: List[Coordinate],
                 orientation: Orientation,
                 board: Board):
        self.body_parts = deque(body_parts) # Use deque to efficiently move body forward
        self.orientation = orientation
        self.board = board
    
    def turn_left(self):
        self.orientation = self.orientation.left()
    
    def turn_right(self):
        self.orientation = self.orientation.right()

    def move(self, food_in_front=False):
        if not food_in_front:
            self.body_parts.popleft()
        
        old_head_position = self.body_parts[-1]

        new_head_position = self.board.move(old_head_position, self.orientation)
        self.body_parts.append(new_head_position)

class Board:
    orientation_to_move_map = {
        Orientation.NORTH : Coordinate(0 , 1),
        Orientation.WEST  : Coordinate(-1, 0),
        Orientation.SOUTH : Coordinate(0 ,-1),
        Orientation.EAST  : Coordinate(1 , 0)
    }
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def onBoard(self, coord: Coordinate):
        return coord.x >= 0 and coord.x < self.width and coord.y >= 0 and coord.y < self.height

    def move(self, position: Coordinate, orientation: Orientation) -> Coordinate:
        new_position = position + Board.orientation_to_move_map[orientation]
        # make sure new position is inside board
        new_position.x = (new_position.x + self.width) % self.width
        new_position.y = (new_position.y + self.height) % self.height

        return new_position

class Game:
    def __init__(self, width=500, height=500):
        self.width = width
        self.height = height
        self.board = Board(self.width, self.height)
        
        initial_orientation = Orientation.EAST
        initial_body_parts = [Coordinate(self.width // 2, self.height // 2)]
        INITIAL_BODY_PART_COUNT = 5
        for body_part in range(1, INITIAL_BODY_PART_COUNT):
            initial_body_parts.append(initial_body_parts[-1] + Coordinate(20,0))
        print(initial_body_parts)
        self.snake = Snake(initial_body_parts, initial_orientation, self.board)

        self.screen = pygame.display.set_mode([self.width, self.height])
        self.screen.fill(WHITE_RGB)
    
    def draw(self):
        for body_part in self.snake.body_parts:
            pygame.draw.rect(self.screen, BLACK_RGB, [body_part.x,body_part.y,20,20])
    
    def run(self):
        running = True
        while running:
            time.sleep(0.1)
            self.draw()
            had_event = False
            # Did the user click the window close button?
            for event in pygame.event.get():
                had_event = True
                if event.type == pygame.QUIT:
                    running = False
            
            pygame.display.flip()



# Done! Time to quit.
pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()