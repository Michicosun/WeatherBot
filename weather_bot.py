import os
import telebot
from bs4 import BeautifulSoup
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' +
    'AppleWebKit/537.36 (KHTML, like Gecko)' +
    'Chrome/58.0.3029.110 Safari/537.3'}

def weather(city, init_name):
    city = city.replace(" ", "+")
    res = ""
    try:
        res = requests.get(
            f'https://www.google.com/search?q={city}&oq={city}' +
            '&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
            headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        cur_location = soup.select('#wob_loc')[0].getText().strip()
        cur_time = soup.select('#wob_dts')[0].getText().strip()
        cur_info = soup.select('#wob_dc')[0].getText().strip()
        cur_weather = soup.select('#wob_tm')[0].getText().strip()
        ret_str = ""
        ret_str += cur_location + "\n"
        ret_str += cur_time + "\n"
        ret_str += cur_info + "\n"
        ret_str += cur_weather + "°C" + "\n"
        return ret_str
    except Exception:
        return "Can't find city: " + init_name

city_list = {}

def create_if_not_created(chat_id):
    if chat_id not in city_list:
        city_list.update({chat_id : []})

def add_city(city, chat_id):
    create_if_not_created(chat_id)
    if city not in city_list[chat_id]:
        city_list[chat_id].append(city)

def del_city(city, chat_id):
    create_if_not_created(chat_id)
    if city in city_list[chat_id]:
        city_list[chat_id].remove(city)

def print_weather_for_all(chat_id):
    create_if_not_created(chat_id)
    ans = ""
    for city in city_list[chat_id]:
        request = city+" weather"
        ans += weather(request, city) + "\n"
    if ans == "":
        ans = "none"
    return ans

TOKEN = str(os.environ.get('TELEGRAM_BOT_TOKEN'))
print(TOKEN)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "hello")
    create_if_not_created(message.chat.id)

@bot.message_handler(commands=['add_city'])
def add_func(message):
    msg = bot.send_message(message.chat.id, "type name of the city")
    bot.register_next_step_handler(msg, get_city_name_for_add)

def get_city_name_for_add(message):
    add_city(message.text, message.chat.id)

@bot.message_handler(commands=['delete_city'])
def delete_func(message):
    msg = bot.send_message(message.chat.id, "type name of the city")
    bot.register_next_step_handler(msg, get_city_name_for_del)

def get_city_name_for_del(message):
    del_city(message.text, message.chat.id)

def get_all_cities(chat_id):
    create_if_not_created(chat_id)
    ans = "list of tracking cities:\n"
    for city in city_list[chat_id]:
        ans += str(city) + "\n"
    return ans

@bot.message_handler(commands=['list'])
def list_func(message):
    bot.send_message(message.chat.id, get_all_cities(message.chat.id))

@bot.message_handler(func=lambda message: True)
def send_response(message):
    bot.send_message(message.chat.id, print_weather_for_all(message.chat.id))

bot.infinity_polling()
