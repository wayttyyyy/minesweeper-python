from cell import Cell


def test_cell_initialization():
    """Перевіряє правильність початкового стану клітинки."""
    cell = Cell(row=2, col=3)

    assert cell.row == 2
    assert cell.col == 3
    assert cell.is_mine is False
    assert cell.is_revealed is False
    assert cell.is_flagged is False
    assert cell.adjacent_mines == 0
