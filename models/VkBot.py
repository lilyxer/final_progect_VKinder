import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from environs import Env


env = Env()
env.read_env()

class VkBot:
    """Базовый класс бота
    Проходит авторизацию"""

    authorize = False
    session = False
    longpoll = False

    def __init__(self) -> None:
        """Инициализируем базовый класс"""
        print('запустли')
        self.do_authauthorize()
        if self.authorize:
            self.longpoll = VkLongPoll(self.authorize)
            print('прошли')


    def do_authauthorize(self):
        """Проходим авторизацию
        создаём сессию, для работы с ботом
        """
        try:
            self.authorize = vk_api.VkApi(token=env('GROUP_TOKEN'))
            self.session = self.authorize.get_api()
        except Exception as err:
            print(err, 'Авторизация завершилась неудачно', sep='\n')
    
    def write_msg(self, user_id: int, message: str):
        """Автоответчик
        """
        self.authorize.method('messages.send', {'user_id': user_id, 
                                                'message': message,
                                                'random_id': get_random_id()})