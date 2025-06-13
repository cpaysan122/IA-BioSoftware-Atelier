import os
from datetime import datetime
from pathlib import Path

# Dictionnaire des prix des ingrédients autorisés
INGREDIENT_PRICES = {
    "bun": 2.0,
    "beef": 5.0,
    "chicken": 4.0,
    "cheese": 1.0,
    "tomato": 0.5,
    "lettuce": 0.5,
    "sauce": 0.3,
}

# Listes blanches des options pour chaque ingrédient
ALLOWED_BUNS = ["classic", "sesame", "wholewheat"]
ALLOWED_MEATS = ["beef", "chicken"]
ALLOWED_SAUCES = ["ketchup", "mayo", "bbq", "mustard", "sauce"]
ALLOWED_CHEESES = ["cheddar", "swiss", "emmental", "cheese"]

# Chemin sécurisé pour sauvegarder les fichiers
TMP_DIR = Path("/tmp/burger_safe")
TMP_DIR.mkdir(parents=True, exist_ok=True)
BURGER_FILE = TMP_DIR / "burger.txt"
COUNT_FILE = TMP_DIR / "burger_count.txt"


def get_order_timestamp():
    """Retourne la date et l'heure actuelles sous forme de chaîne."""
    return datetime.now().isoformat(sep=" ", timespec="seconds")


def ask_choice(prompt, allowed, max_attempts=3):
    """
    Demande à l'utilisateur de choisir parmi une liste autorisée,
    avec un nombre limité de tentatives.
    """
    attempts = 0
    while attempts < max_attempts:
        choice = input(f"{prompt} ({'/'.join(allowed)}): ").strip().lower()
        if choice in allowed:
            print(f"Selected: {choice}")
            return choice
        print(f"Invalid choice. Please select from: {', '.join(allowed)}.")
        attempts += 1
    raise ValueError("Too many invalid attempts. Aborting.")


def calculate_burger_price(ingredients_list):
    """Calcule le prix total du burger à partir d'une liste d'ingrédients."""
    total = 0
    for ingredient in ingredients_list:
        total += INGREDIENT_PRICES.get(ingredient, 0)
    return round(total * 1.2, 2)  # Taxe de 20%, arrondi à 2 décimales


def assemble_burger():
    """
    Assemble le burger à partir des choix utilisateur
    et retourne sa description et son prix.
    """
    bun = ask_choice("What kind of bun would you like?", ALLOWED_BUNS)
    meat = ask_choice("Enter the meat type", ALLOWED_MEATS)
    sauce = ask_choice("What sauce would you like?", ALLOWED_SAUCES)
    cheese = ask_choice("What kind of cheese?", ALLOWED_CHEESES)

    # Construction de la liste d'ingrédients pour le calcul du prix
    ingredients = ["bun", meat, "cheese", "sauce"]
    price = calculate_burger_price(ingredients)
    timestamp = get_order_timestamp()

    burger_description = (
        f"{bun} bun + {meat} + {sauce} + {cheese} cheese"
    )

    return burger_description, price, timestamp


def load_burger_count():
    """Charge le nombre de burgers fabriqués depuis le fichier sécurisé."""
    try:
        if COUNT_FILE.exists():
            with open(COUNT_FILE, "r", encoding="utf-8") as f:
                count = int(f.read())
                return count
    except Exception:
        pass
    return 0


def save_burger(burger, price, timestamp, count):
    """
    Sauvegarde la description du burger, son prix et la date dans un fichier sécurisé.
    """
    try:
        with open(BURGER_FILE, "w", encoding="utf-8") as f:
            f.write(
                f"Burger: {burger}\nPrice: {price:.2f} €\nTimestamp: {timestamp}\n"
            )
        with open(COUNT_FILE, "w", encoding="utf-8") as f:
            f.write(str(count))
        os.chmod(BURGER_FILE, 0o600)  # Lecture/écriture propriétaire seulement
        os.chmod(COUNT_FILE, 0o600)
        print(f"Burger saved to {BURGER_FILE}")
    except Exception as e:
        print(f"Failed to save burger: {e}")


def main():
    """Point d'entrée principal du script."""
    print("Welcome to the secure burger maker!")
    burger_count = load_burger_count()
    try:
        burger, price, timestamp = assemble_burger()
        burger_count += 1
        print(f"\nYour burger: {burger}")
        print(f"Total price (tax included): {price:.2f} €")
        save_burger(burger, price, timestamp, burger_count)
    except ValueError as ve:
        print(f"Order cancelled: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()



