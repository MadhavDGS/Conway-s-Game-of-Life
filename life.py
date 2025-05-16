import argparse
import pygame
import random
import sys
import time
from typing import Set, Tuple, List

def parse_args():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("--width", type=int, default=60, help="Width of the game board")
    parser.add_argument("--height", type=int, default=30, help="Height of the game board")
    parser.add_argument("--fps", type=int, default=10, help="Frames per second")
    return parser.parse_args()

class GameOfLife:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.live_cells: Set[Tuple[int, int]] = set()
        self.generation = 0
    
    def clear(self):
        self.live_cells.clear()
        self.generation = 0
    
    def random_fill(self, probability=0.3):
        self.clear()
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < probability:
                    self.live_cells.add((x, y))
    
    def count_neighbors(self, x: int, y: int) -> int:
        neighbors = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if (x + dx, y + dy) in self.live_cells:
                    neighbors += 1
        return neighbors
    
    def next_generation(self):
        new_live_cells = set()
        
        cells_to_check = set()
        for x, y in self.live_cells:
            cells_to_check.add((x, y))
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    cells_to_check.add((x + dx, y + dy))
        
        for x, y in cells_to_check:
            if not (0 <= x < self.width and 0 <= y < self.height):
                continue
                
            neighbors = self.count_neighbors(x, y)
            is_alive = (x, y) in self.live_cells
            
            if is_alive and (neighbors == 2 or neighbors == 3):
                new_live_cells.add((x, y))
            elif not is_alive and neighbors == 3:
                new_live_cells.add((x, y))
        
        self.live_cells = new_live_cells
        self.generation += 1
    
    def save_pattern(self, filename="patterns.txt"):
        with open(filename, "w") as f:
            f.write(f"# Pattern saved at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for x, y in sorted(self.live_cells):
                f.write(f"{x},{y}\n")
    
    def load_pattern(self, filename="patterns.txt"):
        self.clear()
        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        x, y = map(int, line.split(","))
                        self.live_cells.add((x, y))
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"Error loading pattern: {e}")

class GameVisualizer:
    def __init__(self, game: GameOfLife, cell_size=15, fps=10):
        self.game = game
        self.cell_size = cell_size
        self.fps = fps
        self.running = False
        self.paused = True
        
        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")
        
        self.width = game.width * cell_size
        self.height = game.height * cell_size + 40
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        
        self.bg_color = (255, 255, 255)  # White background
        self.grid_color = (220, 220, 220)  # Light gray grid
        self.cell_color = (0, 0, 0)  # Black live cells
        self.text_color = (50, 50, 50)  # Dark gray text
        
        self.font = pygame.font.SysFont("Arial", 14)
    
    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height - 40))
        for y in range(0, self.height - 40, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))
    
    def draw_cells(self):
        for x, y in self.game.live_cells:
            rect = pygame.Rect(
                x * self.cell_size + 1,
                y * self.cell_size + 1,
                self.cell_size - 1,
                self.cell_size - 1
            )
            pygame.draw.rect(self.screen, self.cell_color, rect)
    
    def draw_ui(self):
        pygame.draw.rect(self.screen, (240, 240, 240), (0, self.height - 40, self.width, 40))
        
        controls = "Space:▶/⏸  N:Step  C:Clear  R:Random  S:Save  L:Load"
        text_surface = self.font.render(controls, True, self.text_color)
        self.screen.blit(text_surface, (10, self.height - 35))
        
        stats = f"Generation: {self.game.generation}    Live cells: {len(self.game.live_cells)}    FPS: {self.fps}"
        stats_surface = self.font.render(stats, True, self.text_color)
        self.screen.blit(stats_surface, (10, self.height - 20))
    
    def handle_mouse(self, pos, button):
        if pos[1] >= self.height - 40:
            return
            
        x = pos[0] // self.cell_size
        y = pos[1] // self.cell_size
        
        if 0 <= x < self.game.width and 0 <= y < self.game.height:
            if button == 1:
                self.game.live_cells.add((x, y))
            elif button == 3:
                self.game.live_cells.discard((x, y))
    
    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_n:
                        self.game.next_generation()
                    elif event.key == pygame.K_c:
                        self.game.clear()
                    elif event.key == pygame.K_r:
                        self.game.random_fill()
                    elif event.key == pygame.K_s:
                        self.game.save_pattern()
                    elif event.key == pygame.K_l:
                        self.game.load_pattern()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse(pygame.mouse.get_pos(), event.button)
            
            if not self.paused:
                self.game.next_generation()
            
            self.screen.fill(self.bg_color)
            self.draw_grid()
            self.draw_cells()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()

def main():
    args = parse_args()
    game = GameOfLife(args.width, args.height)
    visualizer = GameVisualizer(game, cell_size=15, fps=args.fps)
    visualizer.run()

if __name__ == "__main__":
    main() 