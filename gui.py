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
                # Розрахунок координат з урахуванням зміщення та висоти панелі
                x = self.offset_x + c * CELL_SIZE
                y = PANEL_HEIGHT + r * CELL_SIZE
                cell = self.board.grid[r][c]

                rect = (x, y, CELL_SIZE, CELL_SIZE)

                if not cell.is_revealed:
                    # Малюємо закриту клітинку
                    pygame.draw.rect(self.screen, COLORS["cell_closed"],
                                     (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, COLORS["line"],
                                     (x, y, CELL_SIZE, CELL_SIZE), 1)
                    if cell.is_flagged:
                        pygame.draw.polygon(self.screen, COLORS["flag"],
                                            [(x+10, y+20), (x+10, y+10), (x+20, y+15)])
                        pygame.draw.line(self.screen, COLORS["text"],
                                         (x+10, y+25), (x+10, y+10), 2)
                else:
                    pygame.draw.rect(self.screen, COLORS["cell_open"], rect)
                    pygame.draw.rect(self.screen, COLORS["line"], rect, 1)
                    if cell.is_mine:
                        pygame.draw.circle(self.screen, COLORS["mine"],
                                           (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//3)
                    elif cell.adjacent_mines > 0:
                        txt = self.font.render(str(cell.adjacent_mines), True,
                                               NUM_COLORS.get(cell.adjacent_mines, COLORS["text"]))
                        self.screen.blit(txt, (x + 10, y + 5))

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            # 1. Заливка фону (на самому початку циклу)
            self.screen.fill(COLORS["bg"])

            if self.timer_running:
                self.elapsed_time = int(time.time() - self.start_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, event.button)

            self.draw_panel()
            self.draw_board()

            if self.board.game_over:
                msg = "ПЕРЕМОГА!" if self.board.win else "ПОРАЗКА!"
                color = (0, 255, 0) if self.board.win else (255, 0, 0)
                txt = self.big_font.render(msg, True, color)
                # Розміщуємо по центру
                self.screen.blit(txt, (self.screen.get_width()//2 - txt.get_width()//2,
                                       self.screen.get_height()//2 - txt.get_height()//2))

            # 2. Оновлення екрану (в самому кінці циклу)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

    def handle_click(self, pos, button):
        x, y = pos

        # Натискання на панель кнопок
        if y < PANEL_HEIGHT:
            if button == 1:
                for name, (bx, by, bw, bh, r, c, m) in self.diff_buttons.items():
                    if bx <= x <= bx + bw and by <= y <= by + bh:
                        self.start_game(r, c, m)
            return

        if self.board.game_over:
            return

        # Перевіряємо, чи клік був не по порожній зоні збоку від поля
        if x < self.offset_x or x >= self.offset_x + self.board.cols * CELL_SIZE:
            return

        # Вираховуємо колонку з урахуванням відступу
        col = (x - self.offset_x) // CELL_SIZE
        row = (y - PANEL_HEIGHT) // CELL_SIZE

        if 0 <= row < self.board.rows and 0 <= col < self.board.cols:
            if button == 1:
                if not self.board.grid[row][col].is_flagged:
                    if not self.timer_running:
                        self.timer_running = True
                        self.start_time = time.time()

                    self.board.reveal_cell(row, col)

                    if self.board.game_over:
                        self.timer_running = False
                        if self.board.win:
                            self.check_best_time()
                        else:
                            self.show_all_mines()

            elif button == 3:
                self.board.toggle_flag(row, col)

    def load_best_times(self):
        if os.path.exists("best_times.json"):
            with open("best_times.json", "r") as f:
                return json.load(f)
        return {"10x10": float('inf'), "16x16": float('inf'), "20x20": float('inf')}

    def save_best_times(self):
        with open("best_times.json", "w") as f:
            json.dump(self.best_times, f)

    def draw_panel(self):
        # Малюємо панель
        pygame.draw.rect(self.screen, COLORS["panel"],
                         (0, 0, self.screen.get_width(), PANEL_HEIGHT))

        # Малюємо кнопки складності
        for name, (bx, by, bw, bh, r, c, m) in self.diff_buttons.items():
            pygame.draw.rect(self.screen, COLORS["btn"], (bx, by, bw, bh))
            pygame.draw.rect(self.screen, COLORS["text"], (bx, by, bw, bh), 2)
            text = self.font.render(name, True, COLORS["text"])
            self.screen.blit(text, (bx + 5, by + 5))

        # Статистика
        mines_left = self.board.mines - self.board.flags_placed
        time_display = self.elapsed_time if self.timer_running or self.board.game_over else 0
        bt = self.best_times.get(self.difficulty_key, float('inf'))
        best_str = f"Рекорд: {bt}с" if bt != float('inf') else "Рекорд: -"

        mines_lbl = self.font.render(f"Мін: {mines_left}", True, (255, 255, 255))
        time_lbl = self.font.render(f"Час: {time_display}с", True, (255, 255, 255))
        best_lbl = self.font.render(best_str, True, (255, 255, 255))

        # Рівномірно розподіляємо текст по ширині панелі
        self.screen.blit(mines_lbl, (15, 50))
        self.screen.blit(time_lbl, (self.screen.get_width() // 2 - time_lbl.get_width() // 2, 50))
        self.screen.blit(best_lbl, (self.screen.get_width() - best_lbl.get_width() - 15, 50))

    def show_all_mines(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.grid[r][c].is_mine:
                    self.board.grid[r][c].is_revealed = True

    def check_best_time(self):
        current_best = self.best_times.get(self.difficulty_key, float('inf'))
        if self.elapsed_time < current_best:
            self.best_times[self.difficulty_key] = self.elapsed_time
            self.save_best_times()
