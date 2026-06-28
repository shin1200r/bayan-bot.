import os
import telebot
from telebot import types
from flask import Flask, request
import google.generativeai as genai

# --- СЮДА ВСТАВЬ СВОИ ДАННЫЕ ---
TELEGRAM_TOKEN = "8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA"
GEMINI_API_KEY = "AQ.Ab8RN6K5G3E1oRLtmZ8Z7SZa4z57FBHIQ16l67onOTiRkawhSQ"
# -------------------------------

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# ИСПРАВЛЕНИЕ ТУТ: заменили на актуальную модель
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

# --- МЕНЮ ---
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("Информация", callback_data="info")
    btn2 = types.InlineKeyboardButton("Помощь", callback_data="help")
    btn3 = types.InlineKeyboardButton("Настройки", callback_data="settings")
    btn4 = types.InlineKeyboardButton("Связаться", callback_data="contact")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот с ИИ. Выбери пункт из меню:", reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "info":
        bot.answer_callback_query(call.id, "Загрузка...")
        bot.send_message(call.message.chat.id, "Тут будет информация о боте.")
    elif call.data == "help":
        bot.answer_callback_query(call.id, "Загрузка...")
        bot.send_message(call.message.chat.id, "Список команд: /start")
    elif call.data == "settings":
        bot.answer_callback_query(call.id, "Настройки")
        bot.send_message(call.message.chat.id, "Раздел настроек в разработке.")
    elif call.data == "contact":
        bot.answer_callback_query(call.id, "Связь")
        bot.send_message(call.message.chat.id, "Пишите нам в поддержку.")

# --- ИИ ОБРАБОТЧИК ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        bot.reply_to(message, "Ошибка ИИ. Попробуй позже.")

# --- WEBHOOK ---
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Not allowed', 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
