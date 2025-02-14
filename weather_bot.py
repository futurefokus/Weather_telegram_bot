import telebot
import requests
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
API = os.getenv('API')
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Словари для хранения выбранных единиц измерения и языка
user_units = {}
user_languages = {}

# Словарь с переводами для погоды
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
        "city_not_found": "🚫 Город не найден!"
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
        "city_not_found": "🚫 City not found!"
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
        "city_not_found": "🚫 Қала табылмады!"
    }
}

# Ручной перевод описаний погоды на казахский язык
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

@bot.message_handler(commands=['start'])
def main(message):
    user_lang = user_languages.get(message.chat.id, 'ru')  # По умолчанию русский
    # Приветственное сообщение
    bot.send_message(message.chat.id, translations[user_lang]["welcome"])
    # Кнопки для выбора города
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button1 = types.KeyboardButton('Астана')
    markup.row(button1)
    button2 = types.KeyboardButton('Алматы')
    button3 = types.KeyboardButton('Караганда')
    markup.row(button2, button3)
    bot.send_message(message.chat.id, translations[user_lang]["choose_city"], reply_markup=markup)

@bot.message_handler(commands=['unit'])
def set_unit(message):
    user_lang = user_languages.get(message.chat.id, 'ru')  # По умолчанию русский
    # Кнопки для выбора единицы измерения
    unit_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_celsius = types.KeyboardButton('°C')
    button_fahrenheit = types.KeyboardButton('°F')
    button_kelvin = types.KeyboardButton('K')
    unit_markup.row(button_celsius, button_fahrenheit, button_kelvin)
    bot.send_message(message.chat.id, translations[user_lang]["choose_unit"], reply_markup=unit_markup)

@bot.message_handler(commands=['language'])
def set_language(message):
    user_lang = user_languages.get(message.chat.id, 'ru')  # По умолчанию русский
    # Кнопки для выбора языка
    lang_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_russian = types.KeyboardButton('Русский')
    button_english = types.KeyboardButton('English')
    button_kazakh = types.KeyboardButton('Қазақша')
    lang_markup.row(button_russian, button_english, button_kazakh)
    bot.send_message(message.chat.id, translations[user_lang]["choose_language"], reply_markup=lang_markup)

@bot.message_handler(content_types=['text'])
def get_weather(message):
    user_lang = user_languages.get(message.chat.id, 'ru')  # По умолчанию русский

    # Если сообщение - это выбор единицы измерения, сохраняем его
    if message.text in ['°C', '°F', 'K']:
        user_units[message.chat.id] = message.text
        bot.send_message(message.chat.id, translations[user_lang]["unit_changed"].format(unit=message.text))
        return

    # Если сообщение - это выбор языка, сохраняем его
    if message.text in ['Русский', 'English', 'Қазақша']:
        user_languages[message.chat.id] = 'ru' if message.text == 'Русский' else 'en' if message.text == 'English' else 'kk'
        bot.send_message(message.chat.id, translations[user_lang]["language_changed"].format(language=message.text))
        return

    # Получаем город из сообщения
    city = message.text
    unit = user_units.get(message.chat.id, '°C')  # По умолчанию °C
    language = user_languages.get(message.chat.id, 'ru')  # По умолчанию русский

    # Преобразуем единицу в соответствующий параметр для API
    if unit == '°C':
        unit_param = 'metric'
    elif unit == '°F':
        unit_param = 'imperial'
    elif unit == 'K':
        unit_param = 'standard'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units={unit_param}&lang={language}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        main = data['main']
        temp = main['temp']
        feels_like = main['feels_like']
        humidity = main['humidity']
        wind = data['wind']['speed']
        weather = data['weather'][0]['description']

        # Если язык казахский, переводим описание погоды
        if language == 'kk':
            weather = weather_translations.get(weather, weather)  # Переводим, если возможно, иначе оставляем как есть

        # Переводим температуру в строку в зависимости от выбранной единицы измерения
        if unit == '°C':
            temp_str = f'{temp}°C'
            feels_like_str = f'{feels_like}°C'
        elif unit == '°F':
            temp_str = f'{temp}°F'
            feels_like_str = f'{feels_like}°F'
        elif unit == 'K':
            temp_str = f'{temp} K'
            feels_like_str = f'{feels_like} K'

        # Формируем сообщение с добавленными \n между предложениями
        response_message = f"{translations[user_lang]['weather'].format(city=city)}\n" + \
                           f"🌡 {translations[user_lang]['temperature'].format(temp=temp_str)}\n" + \
                           f"🌬 {translations[user_lang]['feels_like'].format(feels_like=feels_like_str)}\n" + \
                           f"💧 {translations[user_lang]['humidity'].format(humidity=humidity)}\n" + \
                           f"🌪 {translations[user_lang]['wind_speed'].format(wind=wind)}\n" + \
                           f"🌤 {translations[user_lang]['weather_condition'].format(weather=weather)}"
        bot.send_message(message.chat.id, response_message)
    else:
        bot.send_message(message.chat.id, translations[user_lang]["city_not_found"])

@bot.message_handler(func=lambda message: message.text in ['Астана', 'Алматы', 'Караганда'])
def handle_city_buttons(message):
    get_weather(message)

bot.polling(non_stop=True)
