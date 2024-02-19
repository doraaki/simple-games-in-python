from __future__ import annotations
import pygame
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum
from collections import deque
import time
import random
pygame.init()

WHITE_RGB = (255,255,255)
BLACK_RGB = (0,0,0)
RED_RGB = (255,0,0)

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
        return Orientation(self.value % 4 + 1)
    
    def right(self) -> Orientation:
        return Orientation((self.value + 2) % 4 + 1)
    
    def opposite(self) -> Orientation:
        return Orientation((self.value + 1) % 4 + 1)

class Snake:
    def __init__(self,
                 body_parts: List[Coordinate],
                 orientation: Orientation,
                 board: Board):
        self.body_parts = deque(body_parts) # Use deque to efficiently move body forward
        self.head_position = self.body_parts[-1]
        self.orientation = orientation
        self.board = board
    
    def turn_left(self):
        self.orientation = self.orientation.left()
    
    def turn_right(self):
        self.orientation = self.orientation.right()

    def move(self, new_head_position: Coordinate, food_in_front=False):
        if not food_in_front:
            self.body_parts.popleft()
        
        self.body_parts.append(new_head_position)
        self.head_position = new_head_position

class Board:
    orientation_to_move_map = {
        Orientation.NORTH : Coordinate(0 , -1),
        Orientation.WEST  : Coordinate(-1, 0),
        Orientation.SOUTH : Coordinate(0 , 1),
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
    pygame_key_to_orientation_map = {
        pygame.K_UP: Orientation.NORTH,
        pygame.K_LEFT: Orientation.WEST,
        pygame.K_DOWN: Orientation.SOUTH,
        pygame.K_RIGHT: Orientation.EAST
    }

    orientation_to_pygame_key_map = {orientation:key for key, orientation in pygame_key_to_orientation_map.items()}

    def __init__(self,
                 width=500,
                 height=500,
                 block_size_in_pixels=10,
                 initial_body_part_count=5,
                 default_seconds_between_iterations=0.2):
        self.screen_width = width
        self.screen_height = height
        self.block_size_in_pixels = block_size_in_pixels

        self.default_seconds_between_iterations = default_seconds_between_iterations
        self.seconds_between_iterations = self.default_seconds_between_iterations

        self.board_width = self.screen_width // block_size_in_pixels
        self.board_height = self.screen_height // block_size_in_pixels
        self.board = Board(self.board_width, self.board_height)
        
        initial_orientation = Orientation.EAST
        initial_body_parts = [Coordinate(self.board_width // 2, self.board_height // 2)]
        for body_part in range(1, initial_body_part_count):
            initial_body_parts.append(initial_body_parts[-1] + Coordinate(1,0))

        self.snake = Snake(initial_body_parts, initial_orientation, self.board)

        self.food_position = self.generate_food()

        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.running = True

    def generate_food(self):
        while True:
            food_x = random.randint(1, self.board_width) - 1
            food_y = random.randint(1, self.board_height) - 1
            if Coordinate(food_x, food_y) not in self.snake.body_parts:
                return Coordinate(food_x, food_y)
    
    def draw_rect(self, coord: Coordinate, color: Tuple):
        x = coord.x * self.block_size_in_pixels
        y = coord.y * self.block_size_in_pixels
        pygame.draw.rect(self.screen, color, [x,y,self.block_size_in_pixels,self.block_size_in_pixels])
    
    def draw(self):
        self.screen.fill(WHITE_RGB)
        for body_part in self.snake.body_parts:
            self.draw_rect(body_part, BLACK_RGB)

        self.draw_rect(self.food_position, RED_RGB)
    
    def run_game_iteration(self):
        new_head_position = self.board.move(self.snake.head_position, self.snake.orientation)
        if new_head_position in self.snake.body_parts:
            self.running = False
            return
        food_in_front_of_snake = (self.food_position == new_head_position)

        self.snake.move(new_head_position, food_in_front=food_in_front_of_snake)
        
        if food_in_front_of_snake:
            self.food_position = self.generate_food()
    
    def run(self):
        while self.running:
            time.sleep(self.seconds_between_iterations)
            had_event = False
            # Did the user click the window close button?
            self.seconds_between_iterations = self.default_seconds_between_iterations

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key not in Game.pygame_key_to_orientation_map:
                        continue

                    new_orientation = Game.pygame_key_to_orientation_map[event.key]
                    # Can't reverse direction
                    if new_orientation == self.snake.orientation.opposite():
                        continue
                    self.snake.orientation = new_orientation
                    break

            keys = pygame.key.get_pressed()
            if keys[Game.orientation_to_pygame_key_map[self.snake.orientation]]:
                self.seconds_between_iterations = self.default_seconds_between_iterations / 5
    
            self.run_game_iteration()
            self.draw()
            pygame.display.flip()



# Done! Time to quit.
pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()