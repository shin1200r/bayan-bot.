import telebot
import os
from flask import Flask, request
from telebot import types
import google.generativeai as genai

# --- КОНФИГУРАЦИЯ ---
# Вставь сюда свой токен
TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
# Вставь сюда свой API ключ
GEMINI_API_KEY = 'AQ.Ab8RN6Lq1-HozzGXfYcJ-GDyNqMA7FveMeMKKPqRXaieGNU6XQ' 
VERSION = "v2.0.9 (AI_INTEGRATED_FULL)"

genai.configure(api_key=GEMINI_API_KEY)

# Настройка ИИ
SYSTEM_PROMPT = """
Ты — официальный виртуальный гид по Баянаулу. 
Твоя задача — отвечать на вопросы пользователя, используя данные из базы знаний.
Если ответа нет в базе, вежливо направляй к администратору @Askelad_lucius_Artorius_Castus.
Никогда не выдумывай факты. Будь вежливым, кратким, используй Markdown.
"""

model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- ФУНКЦИЯ ДЛЯ ЧТЕНИЯ БАЗЫ ---
def load_data():
    try:
        with open("data.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Информации пока нет."

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

# --- ВЕБХУК (ИСПРАВЛЕНО) ---
@app.route('/', methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# --- ОБРАБОТЧИКИ ---
@bot.message_handler(content_types=['photo'])
def get_photo_id(message):
    file_id = message.photo[-1].file_id
    bot.reply_to(message, f"📸 *Твой file_id:*\n`{file_id}`", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Добро пожаловать в официальный гид по Баянаулу.", reply_markup=get_main_markup())

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
        bot.send_message(chat_id, "Выберите озеро:", reply_markup=get_holiday_homes_markup())
    elif txt == "🏝 Сабындыколь":
        bot.send_message(chat_id, "🏝 *Сабындыколь*\nИнформация по базам отдыха уточняется.", parse_mode="Markdown")
    elif txt == "🏖 Жасыбай":
        bot.send_message(chat_id, "🏖 *Базы отдыха на озере Жасыбай:*\n\n1. [Султан](https://www.instagram.com/sultan_zhasybay?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==)", parse_mode="Markdown")
    elif txt == "🛠 Услуги":
        bot.send_message(chat_id, "Выберите услугу:", reply_markup=get_services_markup())
    elif txt == "🚕 Такси":
        bot.send_message(chat_id, "🚕 *Такси (Диспетчеры):*\n8 705 707 7262, 8 747 612 7162\n\n*Частные водители:*\n8 705 340 8663, 8 771 850 1458, 8 706 721 3032, 8 777 435 8777", parse_mode="Markdown")
    elif txt == "🏗 Сварка":
        bot.send_message(chat_id, "🏗 *Сварщик (Ринат):* 8 705 342 7371", parse_mode="Markdown")
    elif txt == "⚡️ Электрик":
        bot.send_message(chat_id, "⚡️ *Электрик (Болат):* 8 771 277 7021", parse_mode="Markdown")
    elif txt == "⛺️ Юрты":
        bot.send_message(chat_id, "⛺️ *Юрты (Сарыарка):*\n8 705 769 9383\nДоп. номера: 8 705 606 1067, 8 706 721 3032", parse_mode="Markdown")
    elif txt == "🍔 Еда и напитки":
        bot.send_message(chat_id, "Выберите заведение:", reply_markup=get_food_markup())
    elif txt == "🍺 BeerPoint":
        bot.send_message(chat_id, "🍺 *BeerPoint*\nРежим работы: 10:00 - 23:00.\nДоставка: 8 705 176 5220, 8 705 501 8458", parse_mode="Markdown")
    elif txt == "🍹 Bar 2":
        bot.send_message(chat_id, "🍹 *Bar 2*\nИнформация о меню уточняется.", parse_mode="Markdown")
    elif txt == "🔥 Шашлыки":
        bot.send_message(chat_id, "🔥 *Шашлыки (Халал)*\nЗаказ по телефону: +7 777 688 6689", parse_mode="Markdown")
    elif txt == "📜 Легенды":
        bot.send_message(chat_id, "Выберите легенду:", reply_markup=get_legends_markup())
    elif txt == "📜 Жасыбай":
        bot.send_message(chat_id, "📜 *Легенда о Жасыбае*\nДревнее предание гласит...", parse_mode="Markdown")
    elif txt == "📜 Сабындыколь":
        bot.send_message(chat_id, "📜 *Легенда о Сабындыколе*\nНазвание озера переводится как 'Мыльное озеро'...", parse_mode="Markdown")
    elif txt == "📜 Кемпиртас":
        bot.send_message(chat_id, "📜 *Легенда о Кемпиртас*\nВ народе говорят о мудрой старухе...", parse_mode="Markdown")
    elif txt == "📢 Реклама":
        bot.send_message(chat_id, "Выберите действие:", reply_markup=get_ads_markup())
    elif txt == "💰 Стоимость":
        bot.send_message(chat_id, "💰 *Стоимость*\nРазмещение объявления — 500 ₸ в месяц.", parse_mode="Markdown")
    elif txt == "📋 Условия размещения":
        bot.send_message(chat_id, "✅ *Условия:*\nТематика должна соответствовать туризму и отдыху.", parse_mode="Markdown")
    elif txt == "👤 Контакты":
        bot.send_message(chat_id, "👤 *Администратор бота:*\nСвяжитесь по вопросам рекламы: [Админ](https://t.me/Askelad_lucius_Artorius_Castus)", parse_mode="Markdown")
    elif txt == "ℹ️ О боте":
        bot.send_message(chat_id, f"ℹ️ *Баянаул-помощник {VERSION}*\n\nЭтот бот — ваш личный гид.", parse_mode="Markdown")
    
    # --- ИНТЕГРАЦИЯ ИИ ---
    else:
        try:
            bot.send_chat_action(chat_id, 'typing')
            data = load_data()
            prompt = f"База знаний:\n{data}\n\nВопрос пользователя: {txt}"
            response = model.generate_content(prompt)
            bot.send_message(chat_id, response.text, parse_mode="Markdown")
      
        except Exception as e:
            # Бот пришлет ошибку прямо в чат, чтобы мы её увидели
            bot.send_message(chat_id, f"Ошибка ИИ: {str(e)}")
            
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
