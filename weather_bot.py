import telebot
import requests
from telebot import types
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

load_dotenv()
API = os.getenv('API')
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

user_units = {}
user_languages = {}
daily_subscriptions = {}
daily_subscription_setup = {}

translations = {
    "ru": {
        "welcome": "Добро пожаловать! Я помогу узнать погоду в вашем городе. \n\nВыберите один из вариантов:",
        "weather": "🌦 Погода в городе {city}:",
        "temperature": "🌡 Температура: {temp}",
        "feels_like": "🌬 Ощущается как: {feels_like}",
        "humidity": "💧 Влажность: {humidity}%",
        "wind_speed": "🌪 Скорость ветра: {wind} м/с",
        "weather_condition": "🌤 {weather}",
        "unit_changed": "Единица измерения температуры установлена на {unit}. \n\nТеперь выберите город.",
        "language_changed": "Язык изменен на {language}. \n\nТеперь выберите город.",
        "choose_city": "Выберите город:",
        "choose_unit": "Выберите единицу измерения температуры:",
        "choose_language": "Выберите язык:",
        "city_not_found": "🚫 Город не найден!",
        "enter_subscription_city": "Введите город для ежедневной сводки:",
        "enter_subscription_time": "Введите время отправки в формате ЧЧ:ММ (24-часовой формат):",
        "subscription_set": "Ежедневная сводка установлена для города {city} в {time}."
    },
    "en": {
        "welcome": "Welcome! I can help you with weather information. \n\nChoose an option below:",
        "weather": "🌦 Weather in {city}:",
        "temperature": "🌡 Temperature: {temp}",
        "feels_like": "🌬 Feels like: {feels_like}",
        "humidity": "💧 Humidity: {humidity}%",
        "wind_speed": "🌪 Wind speed: {wind} m/s",
        "weather_condition": "🌤 {weather}",
        "unit_changed": "Temperature unit set to {unit}. \n\nNow choose a city.",
        "language_changed": "Language changed to {language}. \n\nNow choose a city.",
        "choose_city": "Choose a city:",
        "choose_unit": "Choose a temperature unit:",
        "choose_language": "Choose a language:",
        "city_not_found": "🚫 City not found!",
        "enter_subscription_city": "Enter the city for the daily weather summary:",
        "enter_subscription_time": "Enter the delivery time in HH:MM format (24-hour):",
        "subscription_set": "Daily weather summary set for {city} at {time}."
    },
    "kk": {
        "welcome": "Қош келдіңіз! Мен сіздің қалаңыздың ауа райы туралы мәліметтер беру үшін көмектесемін. \n\nТөменде біреуін таңдаңыз:",
        "weather": "🌦 Қаладағы ауа райы {city}:",
        "temperature": "🌡 Температура: {temp}",
        "feels_like": "🌬 Қалай сезіледі: {feels_like}",
        "humidity": "💧 Ылғалдылық: {humidity}%",
        "wind_speed": "🌪 Желдің жылдамдығы: {wind} м/с",
        "weather_condition": "🌤 {weather}",
        "unit_changed": "Температураның өлшем бірлігі {unit} етіп өзгертілді. \n\nЕнді қаланы таңдаңыз.",
        "language_changed": "Тіл {language} деп өзгертілді. \n\nЕнді қаланы таңдаңыз.",
        "choose_city": "Қаланы таңдаңыз:",
        "choose_unit": "Температураның өлшем бірлігін таңдаңыз:",
        "choose_language": "Тілді таңдаңыз:",
        "city_not_found": "🚫 Қала табылмады!",
        "enter_subscription_city": "Күнделікті ауа райы сводкасы үшін қала енгізіңіз:",
        "enter_subscription_time": "Жіберу уақытын ЧЧ:ММ (24 сағаттық формат) түрінде енгізіңіз:",
        "subscription_set": "Күнделікті сводка {city} қаласы үшін {time} уақытында орнатылды."
    }
}

weather_translations = {
    "clear sky": "Ашық аспан",
    "few clouds": "Аздаған бұлттар",
    "scattered clouds": "Таралған бұлттар",
    "broken clouds": "Жартылай бұлтты",
    "shower rain": "Жаңбыр жаууы",
    "rain": "Жаңбыр",
    "thunderstorm": "Жылғалық",
    "snow": "Қар",
    "mist": "Тұман"
}

def send_daily_weather(chat_id, city):
    language = user_languages.get(chat_id, 'ru')
    unit = user_units.get(chat_id, '°C')
    if unit == '°C':
        unit_param = 'metric'
    elif unit == '°F':
        unit_param = 'imperial'
    else:
        unit_param = 'standard'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units={unit_param}&lang={language}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        main_data = data['main']
        temp = main_data['temp']
        feels_like = main_data['feels_like']
        humidity = main_data['humidity']
        wind = data['wind']['speed']
        weather = data['weather'][0]['description']

        if language == 'kk':
            weather = weather_translations.get(weather, weather)

        if unit == '°C':
            temp_str = f'{temp}°C'
            feels_like_str = f'{feels_like}°C'
        elif unit == '°F':
            temp_str = f'{temp}°F'
            feels_like_str = f'{feels_like}°F'
        else:
            temp_str = f'{temp} K'
            feels_like_str = f'{feels_like} K'

        response_message = (
            f"{translations[language]['weather'].format(city=city)}\n"
            f"🌡 {translations[language]['temperature'].format(temp=temp_str)}\n"
            f"🌬 {translations[language]['feels_like'].format(feels_like=feels_like_str)}\n"
            f"💧 {translations[language]['humidity'].format(humidity=humidity)}\n"
            f"🌪 {translations[language]['wind_speed'].format(wind=wind)}\n"
            f"🌤 {translations[language]['weather_condition'].format(weather=weather)}"
        )
        bot.send_message(chat_id, response_message)
    else:
        bot.send_message(chat_id, translations[language]["city_not_found"])

def check_daily_weather():
    now = datetime.now().strftime("%H:%M")
    for chat_id, sub in daily_subscriptions.items():
        if sub['time'] == now:
            send_daily_weather(chat_id, sub['city'])

scheduler = BackgroundScheduler()
scheduler.add_job(check_daily_weather, 'interval', minutes=1)
scheduler.start()

@bot.message_handler(commands=['start'])
def main(message):
    user_lang = user_languages.get(message.chat.id, 'ru')
    bot.send_message(message.chat.id, translations[user_lang]["welcome"])
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row(types.KeyboardButton('Астана'))
    markup.row(types.KeyboardButton('Алматы'), types.KeyboardButton('Караганда'))
    bot.send_message(message.chat.id, translations[user_lang]["choose_city"], reply_markup=markup)

@bot.message_handler(commands=['unit'])
def set_unit(message):
    user_lang = user_languages.get(message.chat.id, 'ru')
    unit_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    unit_markup.row(types.KeyboardButton('°C'), types.KeyboardButton('°F'), types.KeyboardButton('K'))
    bot.send_message(message.chat.id, translations[user_lang]["choose_unit"], reply_markup=unit_markup)

@bot.message_handler(commands=['language'])
def set_language(message):
    user_lang = user_languages.get(message.chat.id, 'ru')
    lang_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    lang_markup.row(types.KeyboardButton('Русский'), types.KeyboardButton('English'), types.KeyboardButton('Қазақша'))
    bot.send_message(message.chat.id, translations[user_lang]["choose_language"], reply_markup=lang_markup)

@bot.message_handler(commands=['daily'])
def set_daily(message):
    chat_id = message.chat.id
    daily_subscription_setup[chat_id] = {"step": "city"}
    user_lang = user_languages.get(chat_id, 'ru')
    bot.send_message(chat_id, translations[user_lang]["enter_subscription_city"])

@bot.message_handler(func=lambda message: message.chat.id in daily_subscription_setup)
def daily_setup_handler(message):
    chat_id = message.chat.id
    user_lang = user_languages.get(chat_id, 'ru')
    setup = daily_subscription_setup.get(chat_id)

    if setup["step"] == "city":
        setup["city"] = message.text
        setup["step"] = "time"
        bot.send_message(chat_id, translations[user_lang]["enter_subscription_time"])
    elif setup["step"] == "time":
        time_text = message.text.strip()
        try:
            datetime.strptime(time_text, "%H:%M")
            daily_subscriptions[chat_id] = {"city": setup["city"], "time": time_text}
            bot.send_message(chat_id, translations[user_lang]["subscription_set"].format(city=setup["city"], time=time_text))
            del daily_subscription_setup[chat_id]
        except ValueError:
            bot.send_message(chat_id, translations[user_lang]["enter_subscription_time"])

@bot.message_handler(content_types=['text'])
def get_weather(message):
    chat_id = message.chat.id
    user_lang = user_languages.get(chat_id, 'ru')

    city = message.text
    unit = user_units.get(chat_id, '°C')
    if unit == '°C':
        unit_param = 'metric'
    elif unit == '°F':
        unit_param = 'imperial'
    else:
        unit_param = 'standard'

    if city in ['Русский', 'English', 'Қазақша']:
        user_languages[chat_id] = 'ru' if city == 'Русский' else 'en' if city == 'English' else 'kk'
        bot.send_message(chat_id, translations[user_lang]["language_changed"].format(language=city))
        return

    if city in ['°C', '°F', 'K']:
        user_units[chat_id] = city
        bot.send_message(chat_id, translations[user_lang]["unit_changed"].format(unit=city))
        return

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units={unit_param}&lang={user_lang}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        main_data = data['main']
        temp = main_data['temp']
        feels_like = main_data['feels_like']
        humidity = main_data['humidity']
        wind = data['wind']['speed']
        weather_desc = data['weather'][0]['description']

        if user_lang == 'kk':
            weather_desc = weather_translations.get(weather_desc, weather_desc)

        if unit == '°C':
            temp_str = f'{temp}°C'
            feels_like_str = f'{feels_like}°C'
        elif unit == '°F':
            temp_str = f'{temp}°F'
            feels_like_str = f'{feels_like}°F'
        else:
            temp_str = f'{temp} K'
            feels_like_str = f'{feels_like} K'

        response_message = (
            f"{translations[user_lang]['weather'].format(city=city)}\n"
            f"🌡 {translations[user_lang]['temperature'].format(temp=temp_str)}\n"
            f"🌬 {translations[user_lang]['feels_like'].format(feels_like=feels_like_str)}\n"
            f"💧 {translations[user_lang]['humidity'].format(humidity=humidity)}\n"
            f"🌪 {translations[user_lang]['wind_speed'].format(wind=wind)}\n"
            f"🌤 {translations[user_lang]['weather_condition'].format(weather=weather_desc)}"
        )
        bot.send_message(chat_id, response_message)
    else:
        bot.send_message(chat_id, translations[user_lang]["city_not_found"])

@bot.message_handler(func=lambda message: message.text in ['Астана', 'Алматы', 'Караганда'])
def handle_city_buttons(message):
    get_weather(message)

bot.polling(non_stop=True)
