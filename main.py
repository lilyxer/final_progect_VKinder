from vk_api.longpoll import VkEventType
from models.VkBot import VkBot
from engine_db import *


if __name__ == '__main__':
    vk_bot = VkBot()  # создаём экземпляр бота
    vk_bot.run_bot()  # запуск бота
    create_db()  # создание/проверка БД, инициализация классов
    vk_engine = VKengine()
    # прослушивание событий чата
    for event in vk_bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                sender_id = event.user_id
                vk_bot.get_info(sender_id)
                # vk_bot.write_msg(user_id=sender_id, message=msg)
