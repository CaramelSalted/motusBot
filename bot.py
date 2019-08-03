from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import settings

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
	'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
	level=logging.INFO,
	filename='bot.log')

def greet_user(bot, update, user_data):
	emo = get_user_emo(user_data)
	text = 'Привет {}'.format(emo)
	my_keyboard = ReplyKeyboardMarkup([['Прислать вау картинку'], ['Сменить эмоджи']])
	update.message.reply_text(text, reply_markup=my_keyboard)

def talk_to_me(bot, update, user_data):
	emo = get_user_emo(user_data)
	user_text = "Привет {} {}! Ты написал: {}".format(update.message.chat.first_name, emo, update.message.text)
	logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
		update.message.chat.id, update.message.text)
	update.message.reply_text(user_text)

def send_wow_picture(bot, update, user_data):
	wow_list = glob('img/*.jp*g')
	wow_pic = choice(wow_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(wow_pic, 'rb'))

def change_emo(bot, update, user_data):
	if 'emo' in user_data:
		del user_data['emo']
	emo = get_user_emo(user_data)
	update.message.reply_text('Готово: {} !'.format(emo))

def get_user_emo(user_data):
	if 'emo' in user_data:
		return user_data['emo']
	else:
		user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases = True)
		return user_data['emo']

def main():
	mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

	logging.info('Бот запускается')

	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user, pass_user_data = True))
	dp.add_handler(CommandHandler("wow", send_wow_picture, pass_user_data = True))
	dp.add_handler(RegexHandler('^(Прислать вау картинку)$', send_wow_picture, pass_user_data = True))
	dp.add_handler(RegexHandler('^(Сменить эмоджи)$', change_emo, pass_user_data = True))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data = True))

	mybot.start_polling()
	mybot.idle()

main()