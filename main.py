import telebot
import os
from flask import Flask, request

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Путь для приема сообщений от Telegram
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    print("Пришло сообщение!") 
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def home():
    return "Bot is alive"

def set_webhook():
    webhook_url = f"https://bayan-bot-web.onrender.com/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    set_webhook()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))