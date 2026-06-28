import os
import telebot
from telebot import types
import google.generativeai as genai
from flask import Flask, request

# --- ВСТАВЬ СВОИ ДАННЫЕ СЮДА ---
# Я вписал их прямо в код, чтобы точно ничего не слетало
TELEGRAM_TOKEN = "ТВОЙ_ТОКЕН" 
GEMINI_API_KEY = "ТВОЙ_API_КЛЮЧ"
# -------------------------------

# --- Инициализация объектов ---
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
app = Flask(__name__)

# --- БЛОК КНОПОК И МЕНЮ ---
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Здесь твои кнопки, добавил их все обратно
    btn1 = types.InlineKeyboardButton("Информация", callback_data="info")
    btn2 = types.InlineKeyboardButton("Помощь", callback_data="help")
    btn3 = types.InlineKeyboardButton("Настройки", callback_data="settings")
    btn4 = types.InlineKeyboardButton("Связаться", callback_data="contact")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# --- ОБРАБОТЧИКИ КОМАНД ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Твоя приветственная логика
    bot.reply_to(message, "Привет! Я бот с ИИ. Выбери пункт из меню:", reply_markup=get_main_menu())

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Это раздел помощи. Если что-то не работает — пиши админу.")

# --- ОБРАБОТЧИК КНОПОК (CALLBACK) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "info":
        bot.answer_callback_query(call.id, "Загрузка информации...")
        bot.send_message(call.message.chat.id, "Тут будет информация о боте или проекте.")
    elif call.data == "help":
        bot.answer_callback_query(call.id, "Загрузка помощи...")
        bot.send_message(call.message.chat.id, "Список команд: /start, /help")
    elif call.data == "settings":
        bot.answer_callback_query(call.id, "Настройки")
        bot.send_message(call.message.chat.id, "Раздел настроек пока в разработке.")
    elif call.data == "contact":
        bot.answer_callback_query(call.id, "Связь")
        bot.send_message(call.message.chat.id, "Пишите нам в поддержку.")

# --- ОСНОВНОЙ ОБРАБОТЧИК ИИ (С ОТЛАДКОЙ) ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Здесь мы оставляем весь твой код, просто добавили try-except
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # ЭТА ЧАСТЬ НУЖНА ДЛЯ ОТЛАДКИ
        # Если что-то падает, мы увидим ошибку в логах, а не просто "Ошибка ИИ"
        print(f"DEBUG ERROR: {e}")
        bot.reply_to(message, "Произошла ошибка при обращении к ИИ. Попробуй позже.")

# --- ВЕБХУК ДЛЯ RENDER ---
# Используем корень '/', чтобы не было 404 ошибок
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Not allowed', 403

# --- ЗАПУСК ---
if __name__ == '__main__':
    # Flask запустится на порту 5000 (стандарт для Render)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
