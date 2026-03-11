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
