import vk_api
from vk_api.exceptions import ApiError
from environs import Env
from datetime import date


env = Env()
env.read_env()

class BotBack:
    """Класс отвечающий за логику общения между ботом b БД.
    """

    def __init__(self, token: str) -> None:
        self.api = vk_api.VkApi(token=token)
        self.offset = 0

    def _get_info(self, sender_id:int) -> None|dict:
        """Получаем информацию об отправителе:
        :sender_id: id начавшего диалог
        :return: имя, фамилия, возараст, пол, город
        """
        data =  {'id': sender_id, 'name' : None, 'city': None, 'age': None, 'sex': None}
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
    
    def search_users(self, params: dict) -> list:
        """Наинаем поиск подходящих анкет
        :params: словарь содержайщий: 
            :city: Москва
            :age: 35
            :sex: 1- Жен, 2-Муж
        :return: список анкет"""
        values = {'count': 5, 'offset': self.offset,
                  'age_from': params['age'] - 3,
                  'age_to': params['age'] + 3,
                  'sex': 1 if params['sex'] == 2 else 2,
                  'hometown': params['city'],
                  'status': (1, 6), 'is_closed': False,}
        self.offset += 5
        users = self.api.method('users.search', values=values)
        if users.get('items'):
            users = [{'id': user['id'], 
                      'f': f"{user.get('first_name', '')} {user.get('last_name', '')}"} 
                     for user in users['items'] if not user['is_closed']]
        return users
    
    def get_photos(self, id: int) -> list:
        """Принимает id профиля из найденной анкеты
        :return: список со ссылками на топ 3 фото анкеты
        """
        grade = {'x': 1, 'y': 2, 'z': 3, 'w': 4}
        photos = self.api.method('photos.get', {'owner_id': id,
                                                'album_id': 'profile',
                                                'extended': 1}) 
        if photos.get('items'):
            all_owners = [(item['id'], item['likes']['count'] + item['comments']['count']) 
                     for item in photos['items']]
            owners_top_3 = [k[0] for k in sorted(all_owners, key=lambda d: d[1], reverse=True)][0]

            # all_photos = [{sorted(item['sizes'], key=lambda x: grade.get(x['type'], 0))[-1]['url']:
            #                item['likes']['count'] + item['comments']['count']}
            #               for item in photos['items']]
            # url_top_3 = [k for ph in all_photos 
            #              for k, v in sorted(ph.items(), key=lambda i: i[1], reverse=True)][:3]
            return f'photo{id}_{owners_top_3}'
            return '\n'.join(f'photo{id}_{owner}' for owner in owners_top_3)
    
if __name__ == '__main__':
    bot = BotBack(token=env('ACCES_TOKEN'))
    # print(bot._get_info(2674056))
    # for anket in bot.search_users({'city': 'Москва',
    #                             'age': 35,
    #                             'sex': 2}):
    #     print(anket['id'])
    # for x in range(1, 3):
    #     print(bot.search_users(params={'city': 'Москва',
    #                             'age': 35,
    #                             'sex': 2}))
    print(bot.get_photos(2674056))
