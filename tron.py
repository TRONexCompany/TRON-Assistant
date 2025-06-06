import protokols.brauzer
import protokols.protokol1
import spisok
import random
import function
from golos import Сказ
import frazi
from listen import listen_command
import time
import random
import pickle
import os
import protokols
import importlib
import re
from Slovo import slovo

# Файл для сохранения последних ключей
LAST_KEYS_FILE = 'last_keys.pkl'

# Словарь доступных протоколов
протоколы = {
    "один": None,
    "браузер": None
}

активный_протокол = None

# Инициализация протоколов
протоколы["один"] = protokols.protokol1.Протокол1()
протоколы["браузер"] = protokols.brauzer.браузер()


def execute_command(query):
    global активный_протокол

    separators = spisok.разделение
    last_keys = load_last_keys()  # Загрузка последних использованных ключей

    # Разделяем запрос на команды
    commands = split_query(query, separators)

    # Нормализуем каждое слово в командах
    normalized_commands = []
    for command in commands:
        normalized_words = [slovo(word) for word in command.split()]
        normalized_commands.append(' '.join(normalized_words))

    # Объединяем нормализованные команды обратно в запрос для дальнейшей обработки
    normalized_query = ' '.join(normalized_commands)

    # Проверка на активацию протокола
    activation_keywords = ["протокол"]

    if "протокол" in normalized_query.lower():
        query_parts = normalized_query.lower().split()
        название_протокола = ' '.join([part for part in query_parts if part != 'протокол']).strip()

        if название_протокола in протоколы:
            активный_протокол = протоколы[название_протокола]
            активный_протокол.активировать_протокол()  # Вызов метода активации протокола
            print(f"[Активирован протокол: {название_протокола}]")

    elif any(keyword in normalized_query.lower() for keyword in activation_keywords):
        query_parts = normalized_query.split()
        название_протокола = ' '.join([part for part in query_parts if part.lower() not in activation_keywords]).strip()

        if название_протокола in протоколы:
            активный_протокол = протоколы[название_протокола]
            активный_протокол.активировать_протокол()  # Вызов метода активации протокола
            print(f"[Активирован протокол: {название_протокола}]")


    if активный_протокол:
        valid_words = set()
        for v in активный_протокол.словарь_команд.values():
            valid_words.update(set(v))
        for v in активный_протокол.словарь_действий.values():
            valid_words.update(set(v))

        all_used_keys = set()

        for command in normalized_commands:
            query_words = set(command.split())
            filtered_query_words = query_words.intersection(valid_words)

            # Если команда пустая, используем последние ключи
            if not filtered_query_words:
                filtered_query_words = last_keys
            # Если команда состоит из одного ключа, добавляем последние ключи
            elif len(filtered_query_words) == 1:
                filtered_query_words.update(last_keys)

            found_commands = set()
            for key, value in активный_протокол.словарь_команд.items():
                if filtered_query_words & set(value):
                    found_commands.add(key)

            # Выполняем действия и сохраняем ключи, если они привели к выполнению действий
            if execute_actions(found_commands, активный_протокол.словарь_действий, активный_протокол.функции):
                all_used_keys.update(found_commands)

        save_last_keys(all_used_keys)  # Сохранение последних использованных ключей
        return

    if not активный_протокол:
        # Создание словаря функций из модуля function.py
        functions_dict = {name: getattr(function, name) for name in dir(function) if callable(getattr(function, name))}

        valid_words = set()
        for v in spisok.список_команд["команды"].values():
            valid_words.update(set(v))
        for v in spisok.список["действия"].values():
            valid_words.update(set(v))

        all_used_keys = set()

        for command in normalized_commands:
            query_words = set(command.split())
            filtered_query_words = query_words.intersection(valid_words)

            # Если команда пустая, используем последние ключи
            if not filtered_query_words:
                filtered_query_words = last_keys
            # Если команда состоит из одного ключа, добавляем последние ключи
            elif len(filtered_query_words) == 1:
                filtered_query_words.update(last_keys)

            found_commands = set(k for k, v in spisok.список_команд["команды"].items() if filtered_query_words & set(v))

            # Выполняем действия и сохраняем ключи, если они привели к выполнению действий
            if execute_actions(found_commands, spisok.список["действия"], functions_dict):
                all_used_keys.update(found_commands)

        save_last_keys(all_used_keys)  # Сохранение последних использованных ключей
        return

    # Если протокол не активен, используем spisok.py и function.py
    valid_words = set()
    for v in spisok.список_команд["команды"].values():
        valid_words.update(set(v))
    for v in spisok.список["действия"].values():
        valid_words.update(set(v))

    all_used_keys = set()

    for command in normalized_commands:
        query_words = set(command.split())
        filtered_query_words = query_words.intersection(valid_words)

        # Если команда пустая, используем последние ключи
        if not filtered_query_words:
            filtered_query_words = last_keys
        # Если команда состоит из одного ключа, добавляем последние ключи
        elif len(filtered_query_words) == 1:
            filtered_query_words.update(last_keys)

        found_commands = set(k for k, v in spisok.список_команд["команды"].items() if filtered_query_words & set(v))

        # Выполняем действия и сохраняем ключи, если они привели к выполнению действий
        if execute_actions(found_commands, spisok.список["действия"], function):
            all_used_keys.update(found_commands)

    save_last_keys(all_used_keys)  # Сохранение последних использованных ключей


def load_last_keys():
    """Загрузка последних использованных ключей."""
    try:
        with open(LAST_KEYS_FILE, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return set()


def save_last_keys(keys):
    """Сохранение последних использованных ключей."""
    with open(LAST_KEYS_FILE, 'wb') as f:
        pickle.dump(keys, f)


def split_query(query, separators):
    """Разделение запроса на отдельные команды."""
    commands = [query]
    for separator in separators:
        new_commands = []
        for command in commands:
            if separator in command:
                new_commands.extend(command.split(separator))
            else:
                new_commands.append(command)
        commands = new_commands
    return commands


def execute_actions(found_commands, actions_dict, functions):
    """Выполняем действия, если найденные команды совпадают с ключами действий."""
    for action_key, action_value in actions_dict.items():
        if found_commands == set(action_value):
            if action_key in functions and callable(functions[action_key]):
                functions[action_key]()
                return True  # Действие выполнено
            break
    return False  # Действие не выполнено




last_wake_time = 0
WAKE_TIMEOUT = 10  # Время в секундах, в течение которого не нужно повторять wake_word

def main():
    global last_wake_time
    while True:
        # Проверяем, прошло ли достаточно времени с последнего вызова wake_word
        current_time = time.time()
        if current_time - last_wake_time > WAKE_TIMEOUT:
            query = listen_command()
            if any(wake_word in query for wake_word in spisok.Трон["имя"]):
                text = random.choice(frazi.пробуждение)
                print(text)
                Сказ(text)
                last_wake_time = current_time  # Обновляем время последнего вызова wake_word
            else:
                continue
        else:
            # Слушаем команду без повторного вызова wake_word
            command = listen_command()
            if command:
                execute_command(command)
                last_wake_time = current_time  # Обновляем время после выполнения команды


if __name__ == "__main__":
    main()
