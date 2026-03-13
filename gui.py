import tkinter as tk
from tkinter import messagebox
import time
import json
import os
import pygame
from board import Board

class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Сапер")
        
        # Панель для статистики (Счетчик мин, Таймер, Рекорд)
        self.stats_frame = tk.Frame(self.root)
        self.stats_frame.pack(padx=10, pady=5, fill=tk.X)
        
        self.mines_label = tk.Label(self.stats_frame, text="Мин: 0", font=("Arial", 12, "bold"))
        self.mines_label.pack(side=tk.LEFT)
        
        self.timer_label = tk.Label(self.stats_frame, text="Время: 0", font=("Arial", 12, "bold"))
        self.timer_label.pack(side=tk.RIGHT)
        
        self.best_time_label = tk.Label(self.stats_frame, text="Рекорд: -", font=("Arial", 10))
        self.best_time_label.pack(side=tk.TOP)

        # Контейнер для кнопок
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)
        
        self.board = None
        self.buttons = {}
        
        # Переменные таймера и рекордов
        self.timer_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.difficulty_key = "10x10"
        self.best_times = self.load_best_times()
        
        self.create_menu()
        self.start_game(10, 10, 10) 

    def load_best_times(self):
        if os.path.exists("best_times.json"):
            with open("best_times.json", "r") as f:
                return json.load(f)
        return {"10x10": float('inf'), "16x16": float('inf'), "20x20": float('inf')}

    def save_best_times(self):
        with open("best_times.json", "w") as f:
            json.dump(self.best_times, f)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        
        game_menu.add_command(label="Легко (10x10, 10 мин)", command=lambda: self.start_game(10, 10, 10))
        game_menu.add_command(label="Помірно (16x16, 40 мин)", command=lambda: self.start_game(16, 16, 40))
        game_menu.add_command(label="Складно (20x20, 80 мин)", command=lambda: self.start_game(20, 20, 80))
        
        menubar.add_cascade(label="Нова гра", menu=game_menu)
        self.root.config(menu=menubar)
    
    def start_game(self, rows, cols, mines):
        self.timer_running = False
        self.elapsed_time = 0
        self.difficulty_key = f"{rows}x{cols}"
        self.update_timer_label()
        self.update_best_time_label()

        for widget in self.frame.winfo_children():
            widget.destroy()
            
        self.buttons = {}
        self.board = Board(rows=rows, cols=cols, mines=mines)
        self.update_mines_label()
        self.create_widgets()
    def draw_panel(self):
        pygame.draw.rect(self.screen, COLORS["panel"], (0, 0, self.screen.get_width(), PANEL_HEIGHT))
        
        # Малюємо кнопки складності
        for text, (bx, by, bw, bh, _, _, _) in self.diff_buttons.items():
            pygame.draw.rect(self.screen, COLORS["btn"], (bx, by, bw, bh))
            pygame.draw.rect(self.screen, COLORS["text"], (bx, by, bw, bh), 2)
            lbl = self.font.render(text, True, COLORS["text"])
            self.screen.blit(lbl, (bx + 5, by + 5))

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
    def draw_board(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                # Додаємо offset_x для центрування поля
                x = self.offset_x + c * CELL_SIZE
                y = r * CELL_SIZE + PANEL_HEIGHT
                cell = self.board.grid[r][c]
                
                rect = (x, y, CELL_SIZE, CELL_SIZE)
                if not cell.is_revealed:
                    pygame.draw.rect(self.screen, COLORS["cell_closed"], rect)
                    pygame.draw.rect(self.screen, COLORS["line"], rect, 2)
                    if cell.is_flagged:
                        pygame.draw.polygon(self.screen, COLORS["flag"], [(x+10, y+20), (x+10, y+10), (x+20, y+15)])
                        pygame.draw.line(self.screen, COLORS["text"], (x+10, y+25), (x+10, y+10), 2)
                else:
                    pygame.draw.rect(self.screen, COLORS["cell_open"], rect)
                    pygame.draw.rect(self.screen, COLORS["line"], rect, 1)
                    if cell.is_mine:
                        pygame.draw.circle(self.screen, COLORS["mine"], (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//3)
                    elif cell.adjacent_mines > 0:
                        txt = self.font.render(str(cell.adjacent_mines), True, NUM_COLORS.get(cell.adjacent_mines, COLORS["text"]))
                        self.screen.blit(txt, (x + 10, y + 5))
    

    def handle_click(self,pos, button):
        x, y = pos
        
        if y < PANEL_HEIGHT:
            if button == 1: 
                for text, (bx, by, bw, bh, r, c, m) in self.diff_buttons.items():
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
    def show_all_mines(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.grid[r][c].is_mine:
                    self.board.grid[r][c].is_revealed = True
    
    def update_mines_label(self):
        remaining = self.board.mines - self.board.flags_placed
        self.mines_label.config(text=f"Мін: {remaining}")

    def update_best_time_label(self):
        bt = self.best_times.get(self.difficulty_key, float('inf'))
        if bt != float('inf'):
            self.best_time_label.config(text=f"Рекорд: {bt} сек")
        else:
            self.best_time_label.config(text="Рекорд: -")

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time = int(time.time() - self.start_time)
            self.update_timer_label()
            self.root.after(1000, self.update_timer) # Вызываем эту же функцию через 1 секунду

    def update_timer_label(self):
        self.timer_label.config(text=f"Час: {self.elapsed_time}")

    def create_widgets(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                btn = tk.Button(self.frame, width=3, height=1, font=("Arial", 10, "bold"))
                btn.bind("<Button-1>", lambda e, row=r, col=c: self.on_left_click(row, col))
                btn.bind("<Button-3>", lambda e, row=r, col=c: self.on_right_click(row, col))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    def on_left_click(self, r, c):
        if self.board.game_over or self.board.grid[r][c].is_flagged: return
        
        # Запускаем таймер при первом клике
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.update_timer()
        
        self.board.reveal_cell(r, c)
        self.update_board()
        
        if self.board.game_over:
            self.timer_running = False # Останавливаем таймер
            if self.board.win:
                self.check_best_time()
                messagebox.showinfo("Перемога!", f"Ви розмінували поле за {self.elapsed_time} секунд!")
            else:
                self.show_all_mines()
                messagebox.showerror("Поразка", "Ви натрапили на міну!")

    def on_right_click(self, r, c):
        if self.board.game_over: return
        self.board.toggle_flag(r, c)
        self.update_mines_label() # Обновляем счетчик мин
        self.update_board()

    def check_best_time(self):
        current_best = self.best_times.get(self.difficulty_key, float('inf'))
        if self.elapsed_time < current_best:
            self.best_times[self.difficulty_key] = self.elapsed_time
            self.save_best_times()
            self.update_best_time_label()
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.screen.fill(COLORS["bg"])
            
            if self.timer_running:
                self.elapsed_time = int(time.time() - self.start_time)

    def update_board(self):
        colors = {1: "blue", 2: "green", 3: "red", 4: "purple", 5: "maroon", 6: "turquoise", 7: "black", 8: "gray"}
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                btn = self.buttons[(r, c)]
                
                if cell.is_revealed:
                    btn.config(state="disabled", relief=tk.SUNKEN)
                    if cell.is_mine:
                        btn.config(text="💣", disabledforeground="red")
                    elif cell.adjacent_mines > 0:
                        btn.config(text=str(cell.adjacent_mines), disabledforeground=colors.get(cell.adjacent_mines, "black"))
                    else:
                        btn.config(text="")
                elif cell.is_flagged:
                    btn.config(text="🚩", fg="red")
                else:
                    btn.config(text="")

    def show_all_mines(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.grid[r][c].is_mine:
                    self.board.grid[r][c].is_revealed = True
        self.update_board()