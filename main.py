import telebot
import os
from flask import Flask, request
from telebot import types
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Загрузка переменных из .env (файл должен быть в той же папке)
load_dotenv()
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Настройка ИИ и бота
genai.configure(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

SYSTEM_PROMPT = "Ты — официальный виртуальный гид по Баянаулу. Отвечай вежливо, кратко, используй Markdown."
model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

# --- БАЗА ---
def load_data():
    try:
        with open("data.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "База знаний пока пуста."

# --- КНОПКИ ---
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏠 Жилье", "🏝 Дома отдыха", "🛠 Услуги", "🍔 Еда и напитки", "📜 Легенды", "📢 Реклама", "ℹ️ О боте")
    return markup

def get_houses_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏠 Дом №1", "🏠 Дом №2", "🏠 Дом №3", "🔙 Назад")
    return markup

def get_holiday_homes_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏝 Сабындыколь", "🏖 Жасыбай", "🔙 Назад")
    return markup

def get_services_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🚕 Такси", "🏗 Сварка", "⚡️ Электрик", "⛺️ Юрты", "🔙 Назад")
    return markup

def get_food_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🍺 BeerPoint", "🍹 Bar 2", "🔥 Шашлыки", "🔙 Назад")
    return markup

def get_legends_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📜 Жасыбай", "📜 Сабындыколь", "📜 Кемпиртас", "🔙 Назад")
    return markup

def get_ads_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📋 Условия размещения", "💰 Стоимость", "👤 Контакты", "🔙 Назад")
    return markup

# --- ХЕНДЛЕРЫ ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Добро пожаловать в гид по Баянаулу.", reply_markup=get_main_markup())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    txt = message.text
    chat_id = message.chat.id

    if txt == "🔙 Назад":
        bot.send_message(chat_id, "Главное меню:", reply_markup=get_main_markup())
    elif txt == "🏠 Жилье":
        bot.send_message(chat_id, "Выберите вариант:", reply_markup=get_houses_markup())
    elif txt == "🏠 Дом №1":
        bot.send_photo(chat_id, "AgACAgIAAxkBAAICx2pBZtg2C69bIoRxD60hEb104z71AAISG2sblMsRSgNKPSkRUB0jAQADAgADeQADPAQ", caption="🏠 *Дом №1*\nЦена: 7000 ₸ в сутки.\nКонтакт: Наталия 8 777 939 09 67.", parse_mode="Markdown")
    elif txt == "🏠 Дом №2":
        bot.send_message(chat_id, "🏠 *Дом №2*\nУютный дом.\nInstagram: [bulbul.realtor](https://instagram.com/bulbul.realtor)", parse_mode="Markdown")
    elif txt == "🏠 Дом №3":
        bot.send_photo(chat_id, "AgACAgIAAxkBAAIFG2pBc0FWZVvHWqviCs-aAkcea32rAAIdHGsblMsRSmRJU6_AbfyeAQADAgADEQADPAQ", caption="🏠 *Cheremushki Glemp*\n📍 Баянаул, озеро Сабындыколь.\n\n💰 *Цены:*\n• Будние дни: 20 000 ₸/сутки\n• Выходные дни: 25 000 ₸/сутки\n\n📞 Бронирование: +7 705 455 91 33.", parse_mode="Markdown")
    elif txt == "🏝 Дома отдыха":
        bot.send_message(chat_id, "Выберите локацию:", reply_markup=get_holiday_homes_markup())
    elif txt == "🏖 Жасыбай":
        bot.send_message(chat_id, "🏖 *Базы отдыха на озере Жасыбай:*\n\n1. [Султан](https://www.instagram.com/sultan_zhasybay)", parse_mode="Markdown")
    elif txt == "🛠 Услуги":
        bot.send_message(chat_id, "Выберите услугу:", reply_markup=get_services_markup())
    elif txt == "🚕 Такси":
        bot.send_message(chat_id, "🚕 *Такси:*\n8 705 707 7262, 8 747 612 7162", parse_mode="Markdown")
    elif txt == "🏗 Сварка":
        bot.send_message(chat_id, "🏗 *Сварщик (Ринат):* 8 705 342 7371", parse_mode="Markdown")
    elif txt == "⚡️ Электрик":
        bot.send_message(chat_id, "⚡️ *Электрик (Болат):* 8 771 277 7021", parse_mode="Markdown")
    elif txt == "⛺️ Юрты":
        bot.send_message(chat_id, "⛺️ *Юрты (Сарыарка):*\n8 705 769 9383", parse_mode="Markdown")
    elif txt == "🍔 Еда и напитки":
        bot.send_message(chat_id, "Выберите заведение:", reply_markup=get_food_markup())
    elif txt == "🍺 BeerPoint":
        bot.send_message(chat_id, "🍺 *BeerPoint*\nРежим работы: 10:00 - 23:00.\nДоставка: 8 705 176 5220", parse_mode="Markdown")
    elif txt == "🔥 Шашлыки":
        bot.send_message(chat_id, "🔥 *Шашлыки (Халал)*\nЗаказ: +7 777 688 6689", parse_mode="Markdown")
    elif txt == "📜 Легенды":
        bot.send_message(chat_id, "Выберите легенду:", reply_markup=get_legends_markup())
    elif txt == "📢 Реклама":
        bot.send_message(chat_id, "Выберите действие:", reply_markup=get_ads_markup())
    elif txt == "💰 Стоимость":
        bot.send_message(chat_id, "💰 *Стоимость*\nРазмещение объявления — 500 ₸ в месяц.", parse_mode="Markdown")
    elif txt == "👤 Контакты":
        bot.send_message(chat_id, "👤 *Админ:* [Связаться](https://t.me/Askelad_lucius_Artorius_Castus)", parse_mode="Markdown")
    elif txt == "ℹ️ О боте":
        bot.send_message(chat_id, "ℹ️ *Баянаул-помощник*\nВаш личный гид.", parse_mode="Markdown")
    else:
        # Интеграция ИИ для всех остальных сообщений
        bot.send_chat_action(chat_id, 'typing')
        try:
            data = load_data()
            response = model.generate_content(f"База знаний: {data}\n\nВопрос: {txt}")
            bot.send_message(chat_id, response.text, parse_mode="Markdown")
        except Exception:
            bot.send_message(chat_id, "Извините, сейчас я не могу ответить.")

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
