"""Золотая лихорадка v0.1: сундуки."""
import random

ROUNDS = 10
CHESTS = 5
ATTEMPTS = 2
POINTS_FIRST = 10
POINTS_SECOND = 4
STREAK_LENGTH = 3
STREAK_BONUS = 3


def show_chests(opened=None):
    """Показывает номера ещё закрытых сундуков."""
    line = ""
    for number in range(1, CHESTS + 1):
        if number == opened:
            line += " [ ] "
        else:
            line += f" [{number}] "
    print(line)


def ask_chest(attempt, forbidden=None):
    """Спрашивает номер сундука и проверяет ввод."""
    while True:
        answer = input(f"Попытка {attempt}. Номер сундука: ").strip()
        if not answer.isdigit():
            print("Введите число.")
            continue
        number = int(answer)
        if number < 1 or number > CHESTS:
            print(f"Введите число от 1 до {CHESTS}.")
        elif number == forbidden:
            print("Этот сундук уже открыт.")
        else:
            return number


def grade(points):
    """Возвращает звание по количеству очков."""
    if points >= 100:
        return "Золотой магнат"
    elif points >= 70:
        return "Опытный старатель"
    elif points >= 40:
        return "Удачливый искатель"
    elif points >= 20:
        return "Начинающий старатель"
    return "Сегодня не ваш день"


def main():
    """Проводит десять раундов и печатает итог."""
    score = 0
    found = 0
    first = 0
    streak = 0
    best_streak = 0
    bonus_total = 0

    for round_number in range(1, ROUNDS + 1):
        print(f"\nРаунд {round_number} из {ROUNDS}")
        coin = random.randint(1, CHESTS)
        forbidden = None
        success = False
        for attempt in range(1, ATTEMPTS + 1):
            show_chests(forbidden)
            choice = ask_chest(attempt, forbidden)
            if choice == coin:
                points = POINTS_FIRST if attempt == 1 else POINTS_SECOND
                score += points
                found += 1
                if attempt == 1:
                    first += 1
                print(f"Монета найдена! +{points} очков.")
                success = True
                break
            print("Пусто!")
            forbidden = choice

        if success:
            streak += 1
            if streak > best_streak:
                best_streak = streak
            if streak >= STREAK_LENGTH:
                score += STREAK_BONUS
                bonus_total += STREAK_BONUS
                print(f"Бонус за серию: +{STREAK_BONUS}.")
        else:
            streak = 0
            print(f"Монета была в сундуке {coin}.")

    accuracy = found / ROUNDS * 100
    print(f"\nОчки: {score}")
    print(f"Найдено монет: {found} из {ROUNDS}")
    print(f"Точность: {accuracy:.0f}%")
    print(f"Лучшая серия: {best_streak}")
    print(f"С первой попытки: {first}")
    print(f"Бонус за серии: {bonus_total}")
    print(f"Звание: {grade(score)}")


if __name__ == "__main__":
    main()
