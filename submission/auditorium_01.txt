import random

MAX_HP = 30
HEALS_LIMIT = 2

MIN_URON = 3
MAX_URON = 7
MIN_SILNIY_URON = 10
MAX_SILNIY_URON = 15
SHANS_POPADANIYA = 0.5
LECHENIE = 5


def hp_bar(hp: int) -> str:
    """Рисует полоску здоровья: каждый блок = 2 HP."""
    hp = max(0, min(MAX_HP, hp))
    bloki = hp // 2
    vsego_blokov = (MAX_HP + 1) // 2

    return "[" + "#" * bloki + "." * (vsego_blokov - bloki) + "]"


def ask_action() -> int:
    """Спрашивает действие, пока пользователь не введёт 1, 2 или 3."""
    while True:
        answer = input(
            "Ваш ход (1 - удар, 2 - сильный удар, 3 - лечение): "
        )

        if answer in ("1", "2", "3"):
            return int(answer)

        print("Некорректный ввод. Введите число от 1 до 3.")


def main():
    player_hp = MAX_HP
    bot_hp = MAX_HP

    player_heals = HEALS_LIMIT
    bot_heals = HEALS_LIMIT

    turn = 1

    print("=== АРЕНА v0.1: ДУЭЛЬ ===")

    while player_hp > 0 and bot_hp > 0:
        print(f"\n--- Ход {turn} ---")

        print(
            f"Вы:  {hp_bar(player_hp)} "
            f"{player_hp:>3} HP (лечений: {player_heals})"
        )

        print(
            f"Бот: {hp_bar(bot_hp)} "
            f"{bot_hp:>3} HP (лечений: {bot_heals})"
        )

        print()

        deystvie_igroka = ask_action()

        if deystvie_igroka == 1:
            damage = random.randint(MIN_URON, MAX_URON)

            bot_hp -= damage

            print(f"Вы нанесли обычный удар: {damage} урона.")

        elif deystvie_igroka == 2:
            if random.random() < SHANS_POPADANIYA:
                damage = random.randint(
                    MIN_SILNIY_URON,
                    MAX_SILNIY_URON
                )

                bot_hp -= damage

                print(f"Мощный удар! {damage} урона.")
            else:
                print("Мощный удар не попал в цель!")

        else:
            if player_heals > 0:
                staroe_zdorovye = player_hp

                player_hp = min(MAX_HP, player_hp + LECHENIE)
                player_heals -= 1

                vosstanovleno = player_hp - staroe_zdorovye

                print(
                    f"Вы восстановили {vosstanovleno} HP. "
                    f"Осталось лечений: {player_heals}."
                )
            else:
                print("Лечения закончились! Ход потрачен.")

        if bot_hp <= 0:
            break

        print("\nХод компьютера.")

        bot_action = random.choice([1, 1, 2, 3])

        if bot_action == 3 and bot_heals == 0:
            bot_action = 1

        if bot_action == 1:
            damage = random.randint(MIN_URON, MAX_URON)

            player_hp -= damage

            print(f"Бот нанёс обычный удар: {damage} урона.")

        elif bot_action == 2:
            if random.random() < SHANS_POPADANIYA:
                damage = random.randint(
                    MIN_SILNIY_URON,
                    MAX_SILNIY_URON
                )

                player_hp -= damage

                print(f"Бот нанёс мощный удар: {damage} урона.")
            else:
                print("Бот промахнулся мощным ударом!")

        else:
            staroe_zdorovye = bot_hp

            bot_hp = min(MAX_HP, bot_hp + LECHENIE)
            bot_heals -= 1

            vosstanovleno = bot_hp - staroe_zdorovye

            print(
                f"Бот восстановил {vosstanovleno} HP. "
                f"Осталось лечений: {bot_heals}."
            )

        turn += 1

    print("\n" + "=" * 30)

    if player_hp <= 0 and bot_hp <= 0:
        print("Ничья: оба бойца пали.")

    elif bot_hp <= 0:
        print(
            f"ПОБЕДА! У вас осталось "
            f"{max(0, player_hp)} HP за {turn} ходов."
        )

    else:
        print(
            f"ПОРАЖЕНИЕ! У бота осталось "
            f"{max(0, bot_hp)} HP за {turn} ходов."
        )



if __name__ == "__main__":
    main()
