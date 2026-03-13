import pygame
import time
import json
import os
from board import Board

# Налаштування кольорів
COLORS = {
    "bg": (192, 192, 192),
    "cell_closed": (150, 150, 150),
    "cell_open": (220, 220, 220),
    "line": (128, 128, 128),
    "text": (0, 0, 0),
    "mine": (255, 0, 0),
    "flag": (255, 0, 0),
    "panel": (100, 100, 100),
    "btn": (200, 200, 200)
}

# Кольори для цифр
NUM_COLORS = {
    1: (0, 0, 255), 2: (0, 128, 0), 3: (255, 0, 0),
    4: (0, 0, 128), 5: (128, 0, 0), 6: (0, 128, 128),
    7: (0, 0, 0), 8: (128, 128, 128)
}

CELL_SIZE = 30
PANEL_HEIGHT = 80

class MinesweeperGUI:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 24, bold=True)
        
        self.best_times = self.load_best_times()
        self.timer_running = False
        self.start_time = 0
        self.elapsed_time = 0
        
        # Кнопки складності (x, y, width, height, rows, cols, mines)
        self.diff_buttons = {
            "Легко": (10, 10, 80, 30, 10, 10, 10),
            "Середньо": (100, 10, 100, 30, 16, 16, 40),
            "Складно": (210, 10, 100, 30, 20, 20, 80)
        }
        
        self.start_game(10, 10, 10)

    def start_game(self, rows, cols, mines):
        self.board = Board(rows, cols, mines)
        self.difficulty_key = f"{rows}x{cols}"
        self.timer_running = False
        self.elapsed_time = 0
    
        # Налаштування розміру вікна
        width = cols * CELL_SIZE
        height = rows * CELL_SIZE + PANEL_HEIGHT
    
        # Робимо вікно трохи ширшим, щоб вліз весь текст
        if width < 340: 
            width = 340 
        
        # Вираховуємо відступ зліва, щоб поле завжди було по центру
        self.offset_x = (width - (cols * CELL_SIZE)) // 2
    
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Minesweeper")

    def draw_board(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                # Розрахунок координат з урахуванням зміщення та висоти панелі
                x = self.offset_x + c * CELL_SIZE
                y = PANEL_HEIGHT + r * CELL_SIZE
                
                if not cell.is_revealed:
                    # Малюємо закриту клітинку
                    pygame.draw.rect(self.screen, COLORS["cell_closed"], (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, COLORS["line"], (x, y, CELL_SIZE, CELL_SIZE), 1)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill(COLORS["bg"])
            self.draw_panel()
            self.draw_board()
            
            pygame.display.flip()
            clock.tick(30)
            
        pygame.quit()