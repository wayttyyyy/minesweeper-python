import pytest
from unittest.mock import patch, mock_open
from gui import MinesweeperGUI


# --- ФІКСТУРИ ---
@pytest.fixture
@patch('gui.pygame.display.set_mode')
@patch('gui.pygame.font.SysFont')
@patch('gui.pygame.init')
def app(mock_init, mock_font, mock_set_mode):
    """
    Фікстура для безпечної ініціалізації GUI.
    Мокує (імітує) функції Pygame, щоб вікно гри не відкривалося під час тестів.
    """
    return MinesweeperGUI()

# --- ТЕСТИ ---


# Тест 1: Завантаження рекордів, якщо файл ІСНУЄ
@pytest.mark.gui
@patch('gui.os.path.exists')
@patch('builtins.open', new_callable=mock_open,
       read_data='{"10x10": 42, "16x16": 100, "20x20": 200}')
def test_load_best_times_file_exists(mock_file, mock_exists, app):
    """Перевіряє, чи правильно читається існуючий JSON файл з рекордами."""
    # Вказуємо моку, що файл нібито існує
    mock_exists.return_value = True

    # Викликаємо метод
    times = app.load_best_times()

    # Перевіряємо результати та чи викликались системні функції
    assert times["10x10"] == 42
    assert times["16x16"] == 100
    mock_exists.assert_called_with("best_times.json")
    mock_file.assert_called_with("best_times.json", "r")


# Тест 2: Завантаження рекордів, якщо файлу НЕМАЄ
@pytest.mark.gui
@patch('gui.os.path.exists')
def test_load_best_times_no_file(mock_exists, app):
    """Перевіряє, що метод повертає словник за замовчуванням (float('inf')), якщо файлу немає."""
    # Вказуємо моку, що файлу не існує
    mock_exists.return_value = False

    times = app.load_best_times()

    # Перевіряємо, чи отримали ми нескінченність (відсутність рекорду)
    assert times["10x10"] == float('inf')
    mock_exists.assert_called_with("best_times.json")


# Тест 3: Збереження рекордів
@pytest.mark.gui
@patch('builtins.open', new_callable=mock_open)
@patch('gui.json.dump')
def test_save_best_times(mock_json_dump, mock_file, app):
    """Перевіряє, чи правильно викликається функція запису у файл."""
    # Змінюємо рекорди в об'єкті
    app.best_times = {"10x10": 15, "16x16": 50, "20x20": 120}

    # Викликаємо збереження
    app.save_best_times()

    # Перевіряємо, чи файл відкрився на запис ("w") і чи передались туди правильні дані
    mock_file.assert_called_once_with("best_times.json", "w")
    mock_json_dump.assert_called_once_with(app.best_times, mock_file())
