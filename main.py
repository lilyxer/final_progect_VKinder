import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import config


token = config.TOKEN
authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)


def write_msg(user_id, message):
    authorize.method('messages.send', {'user_id': user_id, 'message': message,
                                       'random_id': get_random_id(),})
 
# Прослушивание сервера на событие
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text
        sender = event.user_id  # айдишник отправителя

        if request == "привет":
            write_msg(event.user_id, f"Хай, {sender}")
        elif request == "пока":
            write_msg(event.user_id, "Пока((")
        else:
            write_msg(event.user_id, "Не поняла вашего ответа...")
