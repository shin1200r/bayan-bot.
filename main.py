import telebot
import os
from flask import Flask, request
from telebot import types

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- ЛОГИКА БОТА ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем кнопки
    item1 = types.KeyboardButton("🏔 Локации")
    item2 = types.KeyboardButton("ℹ️ О Баянауле")
    item3 = types.KeyboardButton("📍 Как добраться")
    item4 = types.KeyboardButton("🚕 Такси")
    item5 = types.KeyboardButton("🏠 Базы отдыха")
    item6 = types.KeyboardButton("📜 Легенды")
    
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, "Добро пожаловать в гид по Баянаулу! Выберите раздел:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "🏔 Локации":
        bot.send_message(message.chat.id, "Популярные места:\n1. Озеро Сабындыколь\n2. Озеро Торайгыр\n3. Пещера Коныр-Аулие\n4. Гора Найзатас")
    
    elif message.text == "ℹ️ О Баянауле":
        bot.send_message(message.chat.id, "Баянаул — это государственный национальный природный парк, жемчужина Казахстана, где горы встречаются с кристально чистыми озерами.")
    
    elif message.text == "📍 Как добраться":
        bot.send_message(message.chat.id, "Добраться можно из Павлодара или Экибастуза на личном авто или рейсовых автобусах.")
    
    elif message.text == "🚕 Такси":
        bot.send_message(message.chat.id, "Здесь можно добавить контакты местных таксистов или ссылки на службы заказа.")
    
    elif message.text == "🏠 Базы отдыха":
        bot.send_message(message.chat.id, "Список популярных баз отдыха: (Здесь можно перечислить основные базы отдыха в Баянауле).")
    
    elif message.text == "📜 Легенды":
        bot.send_message(message.chat.id, "📜 *Легенда о Коныр-Аулие*\n\nСогласно преданиям, в пещере Коныр-Аулие скрывался святой старец. Вода в этой пещере считается целебной и исполняет желания. Приезжайте, чтобы ощутить эту магию сами!")
    
    else:
        bot.reply_to(message, "Я вас не совсем понял. Используйте кнопки для навигации!")

# --- WEBHOOK ---
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
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