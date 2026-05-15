import pytest
from board import Board


@pytest.fixture
def empty_board():
    """
    Фікстура, яка створює невелику дошку (3x3) без мін.
    Це дозволяє нам вручну розставляти міни там, де нам потрібно для тестів.
    """
    return Board(rows=3, cols=3, mines=0)


# --- ТЕСТИ ---

# Тест 1: Перевірка ініціалізації дошки (генерація мін)
def test_board_initialization():
    """Перевіряє, чи створюється поле правильного розміру і з правильною кількістю мін."""
    board = Board(rows=5, cols=5, mines=5)

    assert board.rows == 5
    assert board.cols == 5
    assert board.mines == 5

    # Рахуємо фактичну кількість мін на полі
    actual_mines = sum(1 for r in range(5) for c in range(5)
                       if board.grid[r][c].is_mine)
    assert actual_mines == 5


# Тест 2: Перевірка логіки прапорців
def test_toggle_flag(empty_board):
    """Перевіряє, чи правильно ставиться/знімається прапорець та оновлюється лічильник."""
    board = empty_board
    assert board.flags_placed == 0

    # Ставимо прапорець на клітинку (1, 1)
    board.toggle_flag(1, 1)
    assert board.grid[1][1].is_flagged is True
    assert board.flags_placed == 1

    # Знімаємо прапорець з тієї ж клітинки
    board.toggle_flag(1, 1)
    assert board.grid[1][1].is_flagged is False
    assert board.flags_placed == 0


# Тест 3: Підрахунок сусідніх мін (ПАРАМЕТРИЗАЦІЯ)
@pytest.mark.parametrize("mine_coords, check_r, check_c, expected_count", [
    ([(0, 0)], 0, 1, 1),                          # Одна міна зліва від клітинки (0,1)
    ([(0, 0), (0, 2)], 0, 1, 2),                  # Дві міни: зліва і справа від (0,1)
    ([(0, 0), (0, 1), (0, 2)], 1, 1, 3),          # Три міни зверху від центру (1,1)
    ([(0, 0), (0, 1), (0, 2), (1, 0),
      (1, 2), (2, 0), (2, 1), (2, 2)], 1, 1, 8)  # Міни навколо центру
])
def test_calculate_adjacency(empty_board, mine_coords, check_r, check_c, expected_count):
    """
    Параметризований тест для перевірки методу _calculate_adjacency.
    Перевіряє різні комбінації розташування мін навколо певної клітинки.
    """
    board = empty_board

    # Вручну розставляємо міни за координатами з параметрів
    for r, c in mine_coords:
        board.grid[r][c].is_mine = True

    # Примусово викликаємо перерахунок сусідів
    board._calculate_adjacency()

    # Перевіряємо, чи правильна цифра записалася в тестовану клітинку
    assert board.grid[check_r][check_c].adjacent_mines == expected_count
