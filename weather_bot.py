import os
import telebot

TOKEN = str(os.environ.get('TELEGRAM_BOT_TOKEN'))

print(TOKEN)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "hello")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
