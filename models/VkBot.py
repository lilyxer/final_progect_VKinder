import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardButton
from environs import Env
import requests
from datetime import date


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
        self.url = 'https://api.vk.com/method/'
        self.do_authauthorize()
        if self.authorize:
            self.session = self.authorize.get_api()
            print('[+] Авторизация ВК успешна')
            print('[+] Создана ВК сессия')

    def do_authauthorize(self) -> None:
        """Проходим авторизацию
        создаём сессию, для работы с ботом
        """
        try:
            self.authorize = vk_api.VkApi(token=env('GROUP_TOKEN'))
        except Exception as err:
            print(err, 'Авторизация завершилась неудачно', sep='\n')

    def write_msg(self, user_id: int, message: str) -> None:
        """Автоответчик
        """
        self.authorize.method('messages.send', {'user_id': user_id, 
                                                'message': message,
                                                'random_id': get_random_id()})

    def run_bot(self) -> None:
        """Запускаем бота и создание отслеживания событий
        """
        self.longpoll = VkLongPoll(self.authorize)
        print('[+] Чат-бот запущен')
    
    def get_info(self, sender_id:int) -> None:
        """Получаем информацию об отправителе:
        имя, фамилия, возараст, пол, город
        """
        params = {'access_token': env('CLIENT_TOKEN'),
                  'user_ids': sender_id,
                  'fields': ('bdate, city, sex'),
                  'v': '5.131'}
        response = requests.get(url=f'{self.url}users.get', params=params)
        response = response.json()
        if response.get('error'):
            print(response['error']['error_msg'])
        else:
            info = response['response'][0]
            first_name = info.get('first_name')
            last_name = info.get('last_name')
            if city := info.get('city'):
                city = city.get('title')
            age = info.get('bdate')
            if age and len(age.split('.')) == 3:
                age = date.today().year - int(age.split('.')[-1])
            sex = info.get('sex')
            print(first_name, last_name, city, age, sex)

    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}\n{self.authorize=}\n{self.session=}\n{self.longpoll=}'