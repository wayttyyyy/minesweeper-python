import random
from cell import Cell

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.flags_placed = 0 # Добавили счетчик флагов
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.game_over = False
        self.win = False

        self._place_mines()

    def _place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if not self.grid[r][c].is_mine:
                self.grid[r][c].is_mine = True
                mines_placed += 1