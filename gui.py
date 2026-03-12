







def __init__(self):
        self.best_times = self.load_best_times()
        self.timer_running = False
        self.start_time = 0
        self.elapsed_time = 0

def start_game(self, rows, cols, mines):
        self.board = Board(rows, cols, mines)
        self.difficulty_key=f"{rows}x{cols}
        self.timer_running=False
        self.elapsed_time=0

def load_best_times(self):
        if os.path.exists("best_times.json"):
            with open("best_times.json", "r") as f:
                return json.load(f)
        return {"10x10": float('inf'), "16x16": float('inf'), "20x20": float('inf')}
def save_best_times(self):
        with open("best_times.json", "w") as f:
            json.dump(self.best_times, f)
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