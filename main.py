import vk_api
import json
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id
from vk_api.exceptions import ApiError
from environs import Env
from data_base import create_db, VKengine
from engine import BotBack
import k_board

env = Env()
env.read_env()

class BotFront:
    """Класс отвечающий за логику общения между клиентом и ботом.
    """
    authorize = False
    api = False
    dialog = False
    # ANSWERS = None
  
    def __init__(self) -> None:
        self._do_authorize()
        self.api = BotBack(token=env('ACCES_TOKEN'))
        self.params = None
        # self.ANSWERS = self._get_answers()
        if self.authorize and self.api:
            print('[+] Авторизация ВК успешна')
            create_db()
            

    def _do_authorize(self) -> None:
        """Проходим авторизацию для работы бота с чатом
        """
        try:
            self.authorize = vk_api.VkApi(token=env('GROUP_TOKEN'))
        except ApiError as e:
            print(e.error['error_msg'])

    def _get_answers(self) -> dict:
        with open('messages.json', encoding='UTF-8') as file:
            return json.load(file)
    
    def write_msg(self, user_id: int, message: str, attachment=None) -> None:
        """Отвечает на сообщения чата
        :user_id: - id начавшего диалог
        :message: сообщение которое будет отправлено в чат
        :attachment: не текстовое сообщение, в нашем случае фото анкеты
        :keyboard: кнопки клавиатуры для упрощения общения
        """
        # keyboard = VkKeyboard()
        actions = {'Начать': k_board._start(message),
                   'Продолжить': k_board._confirm(message),
                   'Далее': k_board._next_step(message),
                   # 'Избранное': favorites,
                    # 'Следующая': next_anket(),
                    # 'В избранное': next_anket(like=True),
                    'Завершить': k_board._finish(message),
                }

        msg, buttons, attachment = actions.get(message) if actions.get(message) else k_board._greet(self.params)
        param = {'user_id': user_id, 'message': msg,
                'attachment': attachment, 'random_id': get_random_id(),
                'keyboard': buttons,}
        self.authorize.method('messages.send', param)

    def tracking(self):
        """Эхо чата, создаем сеанс отслеживания событий чата"""
        longpoll = VkLongPoll(self.authorize)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text
                if not self.dialog:
                    vk_engine = VKengine()
                    self.dialog = True
                    self.params = self.api._get_info(sender_id=event.user_id)
                    self.write_msg(user_id=event.user_id, message=msg)
                else:
                    self.write_msg(user_id=event.user_id, message=msg)
                    if msg == 'Завершить':
                        self.dialog = False
                        vk_engine.closed()


# def correct(msg, user_info):
#     keyboard = VkKeyboard()
#     keyboard.add_button('Всё верно')
#     keyboard.add_button('Закончить')
#     keyboard.add_line()
#     keyboard.add_button('Хочу изменить возраст')
#     keyboard.add_button('Хочу изменить город')
#     msg = ANSWERS.get(msg)
#     text = f'Ваш возарст: {user_info.get("age", "нет информации")} город: {user_info.get("city")}'
#     write_msg(user_id=sender_id, message=f'{text}\n{msg}', keyboard=keyboard)
    


if __name__ == '__main__':
    bot = BotFront()
    bot.tracking()