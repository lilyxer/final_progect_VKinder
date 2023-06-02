from vk_api.keyboard import VkKeyboard
import json


def _greet(params) -> tuple:
    """Генерирует кнопки клавиатуры в ответ на неизвестное сообщение'
    :return: ответ на сообщение и экземпляр калвиатуры
    """
    keyboard = VkKeyboard()
    keyboard.add_button('Начать')
    keyboard.add_button('Завершить')
    msg = f'Привет, {params["name"]}' 
    return msg, keyboard.get_keyboard(), None

def _start(message:str) -> tuple:
    """Генерирует кнопки клавиатуры в ответ на Начать'
    :return: ответ на сообщение и экземпляр калвиатуры
    """
    keyboard = VkKeyboard()
    keyboard.add_button('Продолжить')
    keyboard.add_button('Избранное')
    keyboard.add_button('Завершить')
    return ANSWERS.get(message), keyboard.get_keyboard(), None

def _confirm(message:str, params: dict) -> tuple:
    """Генерирует кнопки клавиатуры в ответ на Продолжить'
    :return: ответ на сообщение и экземпляр калвиатуры
    """
    keyboard = VkKeyboard()
    keyboard.add_button('Да')
    keyboard.add_button('Завершить')
    msg = f'{ANSWERS.get(message)}\nВозраст: {params["age"]}, Город: {params["city"]}'
    return msg, keyboard.get_keyboard(), None

def _next_step(message:str) -> tuple:
    """Генерирует кнопки клавиатуры '
    :return: ответ на сообщение и экземпляр калвиатуры, закрывает диалог
    """
    keyboard = VkKeyboard()
    'search_users'
    keyboard.add_button('Далее')
    keyboard.add_button('В избранное')
    keyboard.add_line()
    keyboard.add_button('Завершить')
    return

def _finish(message:str) -> tuple:
    """Генерирует кнопки клавиатуры в ответ на Завершить'
    :return: ответ на сообщение и экземпляр калвиатуры, закрывает диалог
    """
    keyboard = VkKeyboard()
    keyboard.add_button('Начать')
    keyboard.add_button('Завершить')
    return ANSWERS.get(message), keyboard.get_keyboard(), None


with open('messages.json', encoding='UTF-8') as file:
    ANSWERS = json.load(file)

if __name__ == '__main__':
    ...