import telebot
import os
from flask import Flask
from threading import Thread

# Твой токен
TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Этот роут нужен, чтобы Render видел, что «сайт» работает
@app.route('/')
def home():
    return "Bot is alive"

# Твой обработчик команд
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот успешно запущен в облаке!")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Запускаем бота
    Thread(target=run_bot).start()
    # Запускаем сервер на порту, который требует Render
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))