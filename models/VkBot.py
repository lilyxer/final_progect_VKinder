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
            self.session = self.authorize.get_api()
            print('[+] Авторизация успешна')
            print('[+] Создана сессия')
            self.run_bot()

    def do_authauthorize(self) -> None:
        """Проходим авторизацию
        создаём сессию, для работы с ботом
        """
        try:
            self.authorize = vk_api.VkApi(token=env('GROUP_TOKEN'))
        except Exception as err:
            print(err, 'Авторизация завершилась неудачно', sep='\n')

    def write_msg(self, user_id: int, message: str):
        """Автоответчик
        """
        self.authorize.method('messages.send', {'user_id': user_id, 
                                                'message': message,
                                                'random_id': get_random_id()})

    def run_bot(self):
        print('[+] Бот запущен')
        self.longpoll = VkLongPoll(self.authorize)
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    msg = event.text.lower()
                    sender = event.user_id
                    self.write_msg(user_id=sender, message=msg)