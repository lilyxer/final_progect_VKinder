import vk_api
from vk_api.exceptions import ApiError
from environs import Env
from datetime import date


env = Env()
env.read_env()

class BotBack:
    """Класс отвечающий за логику общения между ботом и БД."""

    def __init__(self, token: str) -> None:
        self.api = vk_api.VkApi(token=token)
        self.offset = 0

    def get_info(self, sender_id:int) -> dict:
        """Получаем информацию об отправителе:
        :sender_id: id начавшего диалог
        :return: {'id': ..., 'name' : ..., 'city': ..., 'age': ..., 'sex': ...}"""
        data =  {'id': sender_id, 'name' : "Иван", 'city': 'Ростов', 
                 'age': 25, 'sex': 2}
        try:
            info, = self.api.method('users.get', {'user_ids': sender_id,
                                'fields': ('bdate, city, sex'),})
            data['name'] = f"{info.get('first_name')} {info.get('last_name')}"
            city = info.get('city')
            data['city'] = city.get('title') if city else None
            age = info.get('bdate')
            if age and len(age.split('.')) == 3:
                data['age'] = date.today().year - int(age.split('.')[-1])
            data['sex'] = info.get('sex')
        except ApiError as e:
            print(e.error['error_msg'])
        finally:
            return data
    
    def search_users(self, params: dict) -> None|list:
        """Наинаем поиск подходящих анкет
        :params: словарь содержайщий: 
            :city: Москва
            :age: 35
            :sex: 1- Жен, 2-Муж
        :return: [(id,), (id,)] список анкет"""
        values = {'count': 5, 'offset': self.offset,
                  'age_from': params['age'] - 3,
                  'age_to': params['age'] + 3,
                  'sex': 1 if params['sex'] == 2 else 2,
                  'hometown': params['city'], 'has_photo': 1,
                  'status': 6, 'is_closed': False,}
        self.offset += 5
        users = self.api.method('users.search', values=values)
        if users.get('items'):
            users = [{'id': user['id'], 
                      'f': f"{user.get('first_name', '')} {user.get('last_name', '')}"} 
                     for user in users['items'] if not user['is_closed']]
            return users
    
    def get_photos(self, id: int) -> list:
        """Принимает id профиля из найденной анкеты
        :return: список со ссылками на топ 3 фото анкеты"""
        photos = self.api.method('photos.get', {'owner_id': id,
                                                'album_id': 'profile',
                                                'extended': 1}) 
        if photos.get('items'):
            all_owners = [(item['id'], 
                           item['likes']['count'] + item['comments']['count']) 
                          for item in photos['items']]
            owners_top_3 = [k[0] for k in sorted(all_owners, 
                                                 key=lambda d: d[1], reverse=True)][:3]
            return ','.join(f'photo{id}_{owner}' for owner in owners_top_3)
    
if __name__ == '__main__':
    bot = BotBack(token=env('ACCES_TOKEN'))
    print(bot.get_info(2674056))
    for anket in bot.search_users({'city': 'Москва',
                                'age': 35,
                                'sex': 2}):
        print(anket['id'])
    for x in range(1, 10):
        print(bot.search_users(params={'city': 'Можайск',
                                'age': 35,
                                'sex': 2}))
