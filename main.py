import telebot
import os
from flask import Flask, request
from telebot import types
import google.generativeai as genai
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

SYSTEM_PROMPT = "Ты — официальный виртуальный гид по Баянаулу. Отвечай вежливо, кратко, используй Markdown."
model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

# --- БАЗА ЗНАНИЙ ---
def load_data():
    try:
        with open("data.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""

# --- КЛАВИАТУРЫ ---
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

# --- ЛОГИКА ---
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
        bot.send_message(chat_id, "Выберите дом:", reply_markup=get_houses_markup())
    elif txt == "🏠 Дом №1":
        bot.send_photo(chat_id, "AgACAgIAAxkBAAICx2pBZtg2C69bIoRxD60hEb104z71AAISG2sblMsRSgNKPSkRUB0jAQADAgADeQADPAQ", caption="🏠 *Дом №1*\nЦена: 7000 ₸.\nКонтакт: Наталия 8 777 939 09 67.")
    elif txt == "🏠 Дом №2":
        bot.send_message(chat_id, "🏠 *Дом №2*\nInstagram: [bulbul.realtor](https://instagram.com/bulbul.realtor)", parse_mode="Markdown")
    elif txt == "🏠 Дом №3":
        bot.send_photo(chat_id, "AgACAgIAAxkBAAIFG2pBc0FWZVvHWqviCs-aAkcea32rAAIdHGsblMsRSmRJU6_AbfyeAQADAgADEQADPAQ", caption="🏠 *Cheremushki Glemp*\nБудни: 20 000 ₸. Выходные: 25 000 ₸.\nТел: +7 705 455 91 33.")
    elif txt == "🏝 Дома отдыха":
        bot.send_message(chat_id, "Выберите локацию:", reply_markup=get_holiday_homes_markup())
    elif txt == "🏝 Сабындыколь":
        bot.send_message(chat_id, "🏝 *Сабындыколь* — информация уточняется.")
    elif txt == "🏖 Жасыбай":
        bot.send_message(chat_id, "🏖 *Базы отдыха Жасыбай:*\n[Султан](https://www.instagram.com/sultan_zhasybay)", parse_mode="Markdown")
    elif txt == "🛠 Услуги":
        bot.send_message(chat_id, "Выберите услугу:", reply_markup=get_services_markup())
    elif txt == "🚕 Такси":
        bot.send_message(chat_id, "🚕 *Такси:* 8 705 707 7262, 8 747 612 7162")
    elif txt == "🏗 Сварка":
        bot.send_message(chat_id, "🏗 *Сварщик (Ринат):* 8 705 342 7371")
    elif txt == "⚡️ Электрик":
        bot.send_message(chat_id, "⚡️ *Электрик (Болат):* 8 771 277 7021")
    elif txt == "⛺️ Юрты":
        bot.send_message(chat_id, "⛺️ *Юрты (Сарыарка):* 8 705 769 9383")
    elif txt == "🍔 Еда и напитки":
        bot.send_message(chat_id, "Выберите заведение:", reply_markup=get_food_markup())
    elif txt == "🍺 BeerPoint":
        bot.send_message(chat_id, "🍺 *BeerPoint*\n10:00 - 23:00. Доставка: 8 705 176 5220")
    elif txt == "🍹 Bar 2":
        bot.send_message(chat_id, "🍹 *Bar 2* — информация уточняется.")
    elif txt == "🔥 Шашлыки":
        bot.send_message(chat_id, "🔥 *Шашлыки (Халал):* +7 777 688 6689")
    elif txt == "📜 Легенды":
        bot.send_message(chat_id, "Выберите легенду:", reply_markup=get_legends_markup())
    elif txt == "📜 Жасыбай":
        bot.send_message(chat_id, "📜 *Легенда о Жасыбае*...")
    elif txt == "📜 Сабындыколь":
        bot.send_message(chat_id, "📜 *Легенда о Сабындыколе*...")
    elif txt == "📜 Кемпиртас":
        bot.send_message(chat_id, "📜 *Легенда о Кемпиртас*...")
    elif txt == "📢 Реклама":
        bot.send_message(chat_id, "Раздел рекламы:", reply_markup=get_ads_markup())
    elif txt == "📋 Условия размещения":
        bot.send_message(chat_id, "✅ Тематика только туризм.")
    elif txt == "💰 Стоимость":
        bot.send_message(chat_id, "💰 500 ₸ в месяц.")
    elif txt == "👤 Контакты":
        bot.send_message(chat_id, "👤 [Связаться с админом](https://t.me/Askelad_lucius_Artorius_Castus)", parse_mode="Markdown")
    elif txt == "ℹ️ О боте":
        bot.send_message(chat_id, "ℹ️ *Баянаул-помощник* — ваш гид.")
    else:
        # ИИ (если текст не совпал с кнопкой)
        bot.send_chat_action(chat_id, 'typing')
        try:
            data = load_data()
            response = model.generate_content(f"База знаний: {data}\n\nВопрос: {txt}")
            bot.send_message(chat_id, response.text, parse_mode="Markdown")
        except:
            bot.send_message(chat_id, "Ошибка ИИ.")

# ВЕБХУК ДЛЯ RENDERS
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))