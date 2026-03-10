import random
from cell import Cell

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.flags_placed = 0 # Лічильник прапорців
        # Ініціалізація сітки
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.game_over = False
        self.win = False

        self._place_mines()
        self._calculate_adjacency()

    def _place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if not self.grid[r][c].is_mine:
                self.grid[r][c].is_mine = True
                mines_placed += 1

    def _calculate_adjacency(self):
        # Напрями для перевірки 8 сусідніх клітин
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].is_mine:
                    continue
                count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    # Перевірка меж масиву
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.grid[nr][nc].is_mine:
                            count += 1
                self.grid[r][c].adjacent_mines = count
    
    def reveal_cell(self, r, c):
        if self.game_over or self.grid[r][c].is_revealed or self.grid[r][c].is_flagged:
            return

        self.grid[r][c].is_revealed = True

        if self.grid[r][c].is_mine:
            self.game_over = True
            return
        
        # Рекурсивне відкриття порожніх областей
        if self.grid[r][c].adjacent_mines == 0:
            directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                # Перевірка, що сусідня клітина знаходиться всередині ігрового поля
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    self.reveal_cell(nr, nc)