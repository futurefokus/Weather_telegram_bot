#Weather Telegram Bot

This Telegram bot provides weather information for any city, with support for different languages and temperature units. It also allows users to set daily weather notifications.

Features

Get current weather data (temperature, humidity, wind speed, weather condition).

Supports three languages: Russian, English, and Kazakh.

Choose between Celsius, Fahrenheit, or Kelvin for temperature units.

Set up daily weather summaries for a specified city and time.

Requirements

pip install pyTelegramBotAPI

pip install requests

pip install apscheduler

pip install python-dotenv

Setup

Create a Telegram Bot: Use BotFather to create a bot and get the token.

Get OpenWeather API Key: Sign up here for an API key.

Create a .env file with the following content:

Code

API=your_openweather_api_key

BOT_TOKEN=your_telegram_bot_token

Commands

/start: Start the bot and select a city.

/unit: Change temperature unit (°C, °F, K).

/language: Change language (Russian, English, Kazakh).

/daily: Set daily weather notifications. 

Example:

🌦 Weather in Astana:    
🌡 🌡 Temperature: -6.03°C    
🌬 🌬 Feels like: -13.03°C    
💧 💧 Humidity: 79%    
🌪 🌪 Wind speed: 7 m/s      
🌤 🌤 scattered clouds    

🌦 Қаладағы ауа райы Астана:      
🌡 🌡 Температура: 21.15°F      
🌬 🌬 Қалай сезіледі: 8.55°F      
💧 💧 Ылғалдылық: 79%      
🌪 🌪 Желдің жылдамдығы: 15.66 м/с      
🌤 🌤 Таралған бұлттар      
