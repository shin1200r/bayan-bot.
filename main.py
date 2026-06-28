import os
import telebot
from telebot import types
import google.generativeai as genai
from flask import Flask, request

# --- Инициализация ---
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

# --- Кнопки и Меню ---
def get_main_menu():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Информация", callback_data="info")
    button2 = types.InlineKeyboardButton("Помощь", callback_data="help")
    markup.add(button1, button2)
    return markup

# --- Обработка команд ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Выбери действие:", reply_markup=get_main_menu())

# --- Обработка нажатий на кнопки ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "info":
        bot.answer_callback_query(call.id, "Это информационное сообщение")
        bot.send_message(call.message.chat.id, "Ты нажал на кнопку Информации!")
    elif call.data == "help":
        bot.answer_callback_query(call.id, "Помощь в разработке")
        bot.send_message(call.message.chat.id, "Бот готов к работе.")

# --- Основной обработчик сообщений (ИИ) ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Попытка получить ответ от Gemini
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Это выведет реальную причину ошибки в логи Render
        print(f"DEBUG ERROR: {e}")
        bot.reply_to(message, "Ошибка ИИ.")

# --- Webhook для Render ---
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Not allowed', 403

if __name__ == '__main__':
    # Запуск
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
