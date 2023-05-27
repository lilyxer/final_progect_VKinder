from vk_api.longpoll import VkLongPoll, VkEventType
from models.VkBot import VkBot


# def write_msg(user_id, message):
#     authorize.method('messages.send', {'user_id': user_id, 'message': message,
#                                        'random_id': get_random_id()})

# # авторизуемся
# authorize = vk_api.VkApi(token=config.GROUP_TOKEN)
# user_access = vk_api.VkApi(token=config.CLIENT_TOKEN)

# # получаем доступ к событиям
# longpoll = VkLongPoll(authorize)
# vk = authorize.get_api() 
# # user_vk = user_access.get_api()

if __name__ == '__main__':
    vk_bot = VkBot()
    # Прослушивание сервера на событие
    print('ckeiftv')
    for event in vk_bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                sender = event.user_id
                vk_bot.write_msg(user_id=sender, message=msg)
