import telebot
import os

# Тот же токен, который ты используешь в main.py
TOKEN = '8201596025:AAHuAasTcCXYbiThDMprbcDjnXf_pNUY-ic' 
URL = 'https://bayan-bot-web.onrender.com' # Твоя ссылка из логов

bot = telebot.TeleBot(TOKEN)
bot.remove_webhook() # Сначала удаляем старые настройки
bot.set_webhook(url=URL) # Устанавливаем связь

print("Webhook успешно установлен!")
