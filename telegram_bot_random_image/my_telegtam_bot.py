import telebot
from telebot import types
import requests
import config

bot = telebot.TeleBot(config.TOKEN)

def picture_download(num, links):
  for i in range(num):
    responce = requests.get(f'{links}', allow_redirects=True, stream=True)
    with open(f'{i}.png', 'wb') as pic:
      for chunk in responce.iter_content(chunk_size=1024):
        if chunk:
          pic.write(chunk)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
  if message.text == '/help':
    bot.send_message(message.from_user.id, 'Напиши Привет')
  elif message.text == 'привет':
    keyboard = types.InlineKeyboardMarkup()
    key_200 = types.InlineKeyboardButton(text='Скачать (200х200)', callback_data='pic_200')
    keyboard.add(key_200)
    key_400 = types.InlineKeyboardButton(text='Скачать (400х400)', callback_data='pic_400')
    keyboard.add(key_400)
    bot.send_message(message.from_user.id, text='Привет. Могу предложить тебе скачать рандомную небольшую картинку. Выбери разрешение', reply_markup=keyboard)
  else:
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
  if call.data == 'pic_200':
    with open('0.png', 'rb') as f:
      picture_download(1, links = 'https://picsum.photos/200')
      bot.send_photo(call.message.chat.id, f)
  if call.data == 'pic_400':
    with open('0.png', 'rb') as f:
      picture_download(1, links = 'https://picsum.photos/400')
      bot.send_photo(call.message.chat.id, f)
bot.polling(none_stop=True, interval=0)
