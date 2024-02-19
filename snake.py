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
    def __init__(self, width=500, height=500, block_size_in_pixels=10, initial_body_part_count=5):
        self.screen_width = width
        self.screen_height = height
        self.block_size_in_pixels = block_size_in_pixels
        self.board_width = self.screen_width // block_size_in_pixels
        self.board_height = self.screen_height // block_size_in_pixels
        self.board = Board(self.board_width, self.board_height)
        
        initial_orientation = Orientation.EAST
        initial_body_parts = [Coordinate(self.board_width // 2, self.board_height // 2)]
        for body_part in range(1, initial_body_part_count):
            initial_body_parts.append(initial_body_parts[-1] + Coordinate(1,0))
        print(initial_body_parts)
        self.snake = Snake(initial_body_parts, initial_orientation, self.board)

        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.screen.fill(WHITE_RGB)
    
    def draw(self):
        self.screen.fill(WHITE_RGB)
        for body_part in self.snake.body_parts:
            screen_position_x = body_part.x * self.block_size_in_pixels
            screen_position_y = body_part.y * self.block_size_in_pixels
            pygame.draw.rect(self.screen,
                             BLACK_RGB,
                             [screen_position_x,screen_position_y,self.block_size_in_pixels,self.block_size_in_pixels])
    
    def run_game_iteration(self):
        self.snake.move()
    
    def run(self):
        running = True
        while running:
            time.sleep(0.1)
            had_event = False
            # Did the user click the window close button?
            for event in pygame.event.get():
                had_event = True
                if event.type == pygame.QUIT:
                    running = False
            
            self.run_game_iteration()
            self.draw()
            pygame.display.flip()



# Done! Time to quit.
pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()