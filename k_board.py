from vk_api.keyboard import VkKeyboard
import json


def _greet(params) -> tuple:
    """Генерирует кнопки клавиатуры в ответ на неизвестное сообщение
    :return: ответ на сообщение и экземпляр клавиатуры"""
    keyboard = VkKeyboard()
    keyboard.add_button('Начать')
    keyboard.add_line()
    keyboard.add_button('Завершить')
    msg = f'Привет, {params["name"]}' 
    return msg, keyboard.get_keyboard()

def _start(message:str) -> tuple:
    """Генерирует кнопки клавиатуры в ответ на 'Начать'
    :return: ответ на сообщение и экземпляр клавиатуры"""
    keyboard = VkKeyboard()
    keyboard.add_button('Продолжить')
    keyboard.add_button('Избранное')
    keyboard.add_line()
    keyboard.add_button('Завершить')
    return ANSWERS.get(message), keyboard.get_keyboard()

def _confirm(message:str, params: dict) -> tuple:
    """Генерирует кнопки клавиатуры в ответ на 'Продолжить'
    :return: ответ на сообщение и экземпляр клавиатуры"""
    keyboard = VkKeyboard()
    keyboard.add_button('Да')
    keyboard.add_button('Нет')
    keyboard.add_line()
    keyboard.add_button('Завершить')
    msg = f'{ANSWERS.get(message)}\nВозраст: {params["age"]}, Город: {params["city"]}'
    return msg, keyboard.get_keyboard()

def _next_step() -> tuple:
    """Генерирует кнопки клавиатуры в ответ на 'Нет'
    :return: экземпляр клавиатуры"""
    keyboard = VkKeyboard()
    keyboard.add_button('Город')
    keyboard.add_button('Возраст')
    keyboard.add_line()
    keyboard.add_button('Завершить')
    return keyboard.get_keyboard()


def _correct_params(message:str) -> tuple:
    """Подтверждение данных
    :return: ответ на сообщение и экземпляр клавиатуры"""
    keyboard = VkKeyboard()
    keyboard.add_button('Продолжить')
    keyboard.add_line()
    keyboard.add_button('Завершить')
    return f'{ANSWERS.get(message)}', keyboard.get_keyboard()

def _listen_anket(message:str) -> tuple:
    """Генерирует кнопки клавиатуры в ответ на 'Да'
    :return: экземпляр клавиатуры"""
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Далее')
    keyboard.add_button('В избранное')
    keyboard.add_line() 
    keyboard.add_button('Завершить')
    return ANSWERS.get(message), keyboard.get_keyboard()

def _listen_favorites() -> tuple:
    """Генерирует кнопки клавиатуры в ответ на 'Изрбранное'
    :return: экземпляр клавиатуры"""
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Далее')
    keyboard.add_button('Удалить')
    keyboard.add_line() 
    keyboard.add_button('Завершить')
    return keyboard.get_keyboard()

def _finish(message:str) -> tuple:
    """Генерирует кнопки клавиатуры в ответ на Завершить'
    :return: ответ на сообщение и экземпляр калвиатуры, закрывает диалог"""
    keyboard = VkKeyboard()
    keyboard.add_button('Начать')
    keyboard.add_line()
    keyboard.add_button('Завершить')
    return ANSWERS.get(message), keyboard.get_keyboard()

with open('messages.json', encoding='UTF-8') as file:
    ANSWERS = json.load(file)

if __name__ == '__main__':
    ...