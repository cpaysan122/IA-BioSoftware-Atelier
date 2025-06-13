import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import os

# On suppose que le script principal s'appelle burger.py
import burger

class TestBurgerMaker(unittest.TestCase):

    def test_calculate_burger_price(self):
        # Test prix avec ingrédients connus
        ingredients = ["bun", "beef", "cheese", "sauce"]
        price = burger.calculate_burger_price(ingredients)
        expected = round((2.0 + 5.0 + 1.0 + 0.3) * 1.2, 2)
        self.assertEqual(price, expected)

        # Test ingrédient inconnu (doit être ignoré)
        ingredients = ["bun", "unknown"]
        price = burger.calculate_burger_price(ingredients)
        expected = round(2.0 * 1.2, 2)
        self.assertEqual(price, expected)

    @patch('builtins.input', side_effect=['sesame'])
    def test_ask_choice_valid(self, mock_input):
        result = burger.ask_choice("What kind of bun would you like?", burger.ALLOWED_BUNS)
        self.assertEqual(result, 'sesame')

    @patch('builtins.input', side_effect=['invalid', 'classic'])
    def test_ask_choice_invalid_then_valid(self, mock_input):
        result = burger.ask_choice("What kind of bun would you like?", burger.ALLOWED_BUNS)
        self.assertEqual(result, 'classic')

    def test_load_and_save_burger_count(self):
        # Utiliser un répertoire temporaire
        tmp_dir = Path('/tmp/burger_test')
        tmp_dir.mkdir(exist_ok=True)
        count_file = tmp_dir / "burger_count.txt"
        # Sauver un nombre
        with open(count_file, "w") as f:
            f.write("7")
        # Patch le chemin dans le module principal
        with patch.object(burger, 'COUNT_FILE', count_file):
            count = burger.load_burger_count()
            self.assertEqual(count, 7)
            burger.save_burger("desc", 12.5, "2025-06-13 15:00:00", 8)
            with open(count_file, "r") as f:
                self.assertEqual(f.read(), "8")
        # Nettoyage
        try:
            count_file.unlink()
            tmp_dir.rmdir()
        except Exception:
            pass

    def test_get_order_timestamp_format(self):
        ts = burger.get_order_timestamp()
        # Format attendu: 'YYYY-MM-DD HH:MM:SS'
        self.assertRegex(ts, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

if __name__ == '__main__':
    unittest.main()
