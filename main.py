import telebot
import os
from flask import Flask
from threading import Thread
from telebot import types

# Твой токен
TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive"

# === ГЛАВНОЕ МЕНЮ ===
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🏠 Дома отдыха")
    btn2 = types.KeyboardButton("🔑 Жилье в аренду")
    btn3 = types.KeyboardButton("🚘 Таксисты")
    btn4 = types.KeyboardButton("🗺 Экскурсия и Гид")
    btn5 = types.KeyboardButton("🛠 Шиномонтаж и Карта")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n\nРады видеть тебя в Баянауле. Выбери нужную категорию:",
        reply_markup=markup
    )

# === ОБРАБОТКА КНОПОК ===
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "🏠 Дома отдыха":
        bot.send_message(message.chat.id, "🏠 **Дома отдыха на озере Жасыбай:**\n\n• Зона отдыха 'Самал'\n📞 +7 (705) 000-00-00\n\n• Зона отдыха 'Найзатас'\n📞 +7 (707) 000-00-00", parse_mode="Markdown")
    
    elif message.text == "🔑 Жилье в аренду":
        bot.send_message(message.chat.id, "🔑 **Жилье в аренду:**\n\nСдаются частные дома под ключ. Звоните по номеру: +7 (777) 000-00-00", parse_mode="Markdown")
        
    elif message.text == "🚘 Таксисты":
        bot.send_message(message.chat.id, "🚘 **Таксисты:**\n\nБаянаул — Павлодар: +7 (700) 000-00-00\nМестные поездки: +7 (700) 111-11-11", parse_mode="Markdown")
        
    elif message.text == "🗺 Экскурсия и Гид":
        bot.send_message(message.chat.id, "🗺 **Экскурсии:**\n\nИндивидуальные туры по пещерам и горам. Запись: +7 (705) 222-22-22", parse_mode="Markdown")
        
    elif message.text == "🛠 Шиномонтаж и Карта":
        bot.send_message(message.chat.id, "🛠 **Шиномонтаж:**\n\nРаботает круглосуточно на въезде в поселок.\n📞 +7 (777) 333-33-33", parse_mode="Markdown")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))