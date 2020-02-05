# Bot poster v 2.01 created by Mace @Themaceg0d,call me
import telebot
import vk_api
from telebot import types
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from threading import *

bot = telebot.TeleBot( 'TOKEN' )
domain = 'DOMAIN'
access_token = 'ACCESS_TOKEN'
chanelid = '@CHANEL_ID'
domain_name = 'DOMAIN_NAME'

class MyVkLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try: # без этого try-except, бот падает каждый раз, когда вк обновляет сервера
                for event in self.check():
                    yield event
            except Exception as e:
                print('error', e)

class Main(Thread):
    def __init__(self, token, domain):
        Thread.__init__(self)
        self.token = token
        self.domain = domain

    def run(self):
        vk_session = vk_api.VkApi(token=self.token)
        long_poll = MyVkLongPoll(vk_session, self.domain)
        print(f'подключился к {domain_name}')
        while True:
            for event in long_poll.listen():
                print(f'получил пост от {domain_name}')
                if event.type == VkBotEventType.WALL_POST_NEW and event.obj.post_type == 'post': # отсев рекламы\постов пользователей(если стена соо-ва открыта)
                    if event.object.attachments:
                        try:
                            ph = event.object.attachments[0]['photo']['photo_604']  
                            button_1 = types.InlineKeyboardButton(text='BUY SOME SHIT', url='SOMESHIT.COM')
                            markup = types.InlineKeyboardMarkup()
                            markup.add(button_1)
                            bot.send_photo(chanelid, ph, caption=str(event.obj.text), reply_markup=markup)

                        except Exception as e:
                            print('error', e)

                    else:
                        bot.send_message(chanelid, str(event.obj.text), reply_markup=markup)


def take_posts(token, domain):
    x = Main(token, domain)
    x.start()


if __name__ == '__Main__':
    take_posts(access_token, domain)
    bot.polling(none_stop=True)
