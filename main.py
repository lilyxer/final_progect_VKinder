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
  
    def __init__(self) -> None:
        self._do_authorize()
        self.api = BotBack(token=env('ACCES_TOKEN'))
        self.data = VKengine()
        self.params = None
        if self.authorize and self.api:
            create_db()

    def _do_authorize(self) -> None:
        """Проходим авторизацию для работы бота с чатом
        """
        try:
            self.authorize = vk_api.VkApi(token=env('GROUP_TOKEN'))
        except ApiError as e:
            print(e.error['error_msg'])
   
    def write_msg(self, user_id: int, message: str, 
                  keyboard=None, attachment=None) -> None:
        """Отвечает на сообщения чата
        :user_id: - id начавшего диалог
        :message: сообщение которое будет отправлено в чат
        :attachment: не текстовое сообщение, в нашем случае фото анкеты
        :keyboard: кнопки клавиатуры для упрощения общения
        """
        param = {'user_id': user_id, 'message': message, 'attachment': attachment, 
                 'random_id': get_random_id(), 'keyboard': keyboard,}
        self.authorize.method('messages.send', param)

    def _get_profiles(self):
        search_list = self.api.search_users(params=self.params)
        if search_list:
            for user in search_list:
                if not self.data.request_id(profile_id=self.params['id'], anket_id=user['id']):
                    self.data.add_user(profile_id=self.params['id'], anket_id=user['id'])
                    yield user
        else:
            return self._get_profiles()

    def tracking(self):
        """Эхо чата, создаем сеанс отслеживания событий чата"""
        longpoll = VkLongPoll(self.authorize)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text
                if not self.dialog and msg:
                    self.params = self.api._get_info(sender_id=event.user_id)
                    _msg, _board, _att = k_board._greet(self.params)
                    self.write_msg(user_id=event.user_id, message=_msg, 
                                   keyboard=_board, attachment=_att)
                    self.dialog = '_greet'

                elif msg == 'Начать':
                    _msg, _board, _att = k_board._start(msg)
                    self.write_msg(user_id=event.user_id, message=_msg, 
                                   keyboard=_board, attachment=_att)
                    self.dialog = '_start'

                elif msg == 'Завершить':
                    _msg, _board, _att = k_board._finish(msg)
                    self.write_msg(user_id=event.user_id, message=_msg, 
                                   keyboard=_board, attachment=_att)
                    self.params = None
                    self.dialog = False

                elif msg == 'Продолжить':
                    _msg, _board, _att = k_board._confirm(msg, self.params)
                    self.write_msg(user_id=event.user_id, message=_msg, 
                                   keyboard=_board, attachment=_att)
                    self.dialog = '_confirm'
                
                elif self.dialog == '_confirm':
                    if msg == 'Нет':
                        _msg, _board, _att = k_board._next_step(msg)
                        self.write_msg(user_id=event.user_id, 
                                       message='Выберите что будете менять',
                                       keyboard=_board, attachment=_att)

                    elif msg == 'Город':
                        _msg, _board, _att = k_board._correct_params(msg)
                        self.write_msg(user_id=event.user_id, message=_msg, 
                                       keyboard=_board, attachment=_att)
                        self.dialog = '_confirm_city'
                    
                    elif msg == 'Возраст':
                        _msg, _board, _att = k_board._correct_params(msg)
                        self.write_msg(user_id=event.user_id, message=_msg, 
                                       keyboard=_board, attachment=_att)
                        self.dialog = '_confirm_age'
                    
                    elif msg == 'Да':
                        """получаем анкеты"""
                        _msg, _board, _att = k_board._listen_anket(msg)
                        self.write_msg(user_id=event.user_id, message=_msg, 
                                       keyboard=_board, attachment=_att)
                        self.dialog = '_in_search'
                        
                elif msg and self.dialog == '_confirm_city':
                    self.params['city'] = msg
                    self.dialog == '_confirm'

                elif msg and self.dialog == '_confirm_age':
                    try:
                        self.params['age'] = int(msg)
                        self.dialog == '_confirm'
                    except ValueError:
                        err = f'{msg} не является числом'
                        self.write_msg(user_id=event.user_id, message=err)

                elif self.dialog == '_in_search':
                    if msg == 'Далее':
                        _msg = next(self._get_profiles())
                        _att = self.api.get_photos(id=_msg['id'])
                        self.write_msg(user_id=event.user_id, message=f'{_msg["f"]} -> vk.com/id{_msg["id"]}', 
                                       keyboard=_board, attachment=_att)


                elif msg == 'Избранное':
                    """подключаемся к базе, получаем список анкет, генерируем"""
                    self.dialog = '_favorite'

                else:
                    _msg, _board, _att = k_board._greet(self.params)
                    self.write_msg(user_id=event.user_id, 
                                   message='Я вас не понимаю, воспользуйтесь кнопками',
                                   keyboard=_board, attachment=_att)
                print(self.dialog)


if __name__ == '__main__':
    bot = BotFront()
    bot.tracking()
