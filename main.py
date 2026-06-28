import telebot
import os
from flask import Flask, request
from telebot import types

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
MY_ADMIN_ID = 7885515418
VERSION = "v1.4.0 (FINAL)"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- КЛАВИАТУРЫ ---
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("⛺️ Дома отдыха", "🏠 Жилье", "🛠 Услуги", "🍔 Еда и напитки", "📜 Легенды", "ℹ️ О боте", "📢 Реклама")
    return markup

def get_houses_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏠 Дом №1", "🏠 Дом №2", "🏠 Дом №3", "🔙 Назад")
    return markup

def get_rest_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏝 Жасыбай", "💧 Сабындыколь", "🔙 Назад")
    return markup

def get_food_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🍺 BeerPoint", "🍹 Bar 2", "🔥 Шашлыки", "🔙 Назад")
    return markup

def get_services_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🚕 Такси", "🏗 Сварка", "⛺️ Юрты", "🔙 Назад")
    return markup

def get_legends_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📜 Жасыбай", "📜 Сабындыколь", "📜 Кемпиртас", "🔙 Назад")
    return markup

def get_ads_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📋 Условия размещения", "💰 Стоимость", "👤 Контакты", "🔙 Назад")
    return markup

# --- ВЕБХУК ---
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# --- ОБРАБОТЧИКИ ---

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.from_user.id == MY_ADMIN_ID:
        file_id = message.photo[-1].file_id
        bot.reply_to(message, f"Вот ID фото:\n`{file_id}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Я не обрабатываю фото от посторонних.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Добро пожаловать в Баянаул-бот. Выберите раздел:", reply_markup=get_main_markup())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    txt = message.text

    # --- НАВИГАЦИЯ ---
    if txt == "🔙 Назад":
        send_welcome(message)
    
    # --- ЖИЛЬЕ ---
    elif "🏠 Жилье" in txt:
        bot.send_message(message.chat.id, "Выберите вариант жилья:", reply_markup=get_houses_markup())
    
    elif "🏠 Дом №1" in txt:
        # ID фото для Дома №1
        bot.send_photo(message.chat.id, "AgACAgIAAxkBAAICx2pBZtg2C69bIoRxD60hEb104z71AAISG2sblMsRSgNKPSkRUB0jAQADAgADeQADPAQ", 
                       caption="🏠 *Дом №1*\nЦена: 7000 ₸ в сутки.\nКонтакт: Наталия 8 777 939 09 67.", parse_mode="Markdown")
    
    elif "🏠 Дом №2" in txt:
        bot.send_message(message.chat.id, "🏠 *Дом №2*\nУютный дом.\nInstagram: [bulbul.realtor](https://instagram.com/bulbul.realtor)", parse_mode="Markdown")
    
    elif "🏠 Дом №3" in txt:
        bot.send_message(message.chat.id, "📢 *Дом №3*\nЗдесь может быть ваше объявление! Перейдите в раздел '📢 Реклама' для размещения.", parse_mode="Markdown")

    # --- ДОМА ОТДЫХА ---
    elif "⛺️ Дома отдыха" in txt:
        bot.send_message(message.chat.id, "Выберите локацию:", reply_markup=get_rest_markup())
    elif "🏝 Жасыбай" in txt:
        bot.send_message(message.chat.id, "🏠 *Дома отдыха: Жасыбай*\nСписок домов на Жасыбае.", parse_mode="Markdown")
    elif "💧 Сабындыколь" in txt:
        bot.send_message(message.chat.id, "🏠 *Дома отдыха: Сабындыколь*\nСписок домов на Сабындыколе.", parse_mode="Markdown")

    # --- ЕДА (ПОДМЕНЮ) ---
    elif "🍔 Еда и напитки" in txt:
        bot.send_message(message.chat.id, "Выберите заведение:", reply_markup=get_food_markup())
    elif "🍺 BeerPoint" in txt:
        bot.send_message(message.chat.id, "🍺 *BeerPoint*\n10:00 - 23:00.\nДоставка: 8 705 176 5220, 8 705 501 8458", parse_mode="Markdown")
    elif "🍹 Bar 2" in txt:
        bot.send_message(message.chat.id, "🍹 *Bar 2*\nИнформация о баре.", parse_mode="Markdown")
    elif "🔥 Шашлыки" in txt:
        bot.send_message(message.chat.id, "🔥 *Шашлыки (Халал)*\nЗаказ по телефону: +7 777 688 6689", parse_mode="Markdown")

    # --- УСЛУГИ ---
    elif "🛠 Услуги" in txt:
        bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=get_services_markup())
    elif "🚕 Такси" in txt:
        bot.send_message(message.chat.id, "🚕 *Такси*\nДиспетчеры: 8 705 707 7262, 8 747 612 7162.", parse_mode="Markdown")
    elif "🏗 Сварка" in txt:
        bot.send_message(message.chat.id, "🏗 *Сварщик (Ринат)*: 8 705 342 7371", parse_mode="Markdown")
    elif "⛺️ Юрты" in txt:
        bot.send_message(message.chat.id, "⛺️ *Юрты*: 8 705 769 9383 (Сарыарка)", parse_mode="Markdown")

    # --- ЛЕГЕНДЫ ---
    elif "📜 Легенды" in txt:
        bot.send_message(message.chat.id, "Выберите легенду:", reply_markup=get_legends_markup())
    elif "📜 Жасыбай" in txt:
        bot.send_message(message.chat.id, "📜 *Легенда о Жасыбае*\nИстория батыра.", parse_mode="Markdown")
    elif "📜 Сабындыколь" in txt:
        bot.send_message(message.chat.id, "📜 *Легенда о Сабындыколе*\nИстория об озере.", parse_mode="Markdown")
    elif "📜 Кемпиртас" in txt:
        bot.send_message(message.chat.id, "📜 *Легенда о Кемпиртас*\nИстория о скале.", parse_mode="Markdown")

    # --- РЕКЛАМА ---
    elif "📢 Реклама" in txt:
        bot.send_message(message.chat.id, "Выберите вопрос:", reply_markup=get_ads_markup())
    elif "💰 Стоимость" in txt:
        bot.send_message(message.chat.id, "💰 *Стоимость*\nРазмещение объявления — 500 ₸ в месяц.", parse_mode="Markdown")
    elif "📋 Условия размещения" in txt:
        bot.send_message(message.chat.id, "✅ *Условия:*\nТематика отдыха, без спама.", parse_mode="Markdown")
    elif "👤 Контакты" in txt:
        bot.send_message(message.chat.id, "👤 *Контакты для связи:* @Askelad_lucius_Artorius_Castus", parse_mode="Markdown")
    
    # --- ИНФО ---
    elif "ℹ️ О боте" in txt:
        bot.send_message(message.chat.id, f"Версия бота: {VERSION}\nБаянаул-бот.", parse_mode="Markdown")
        
    else:
        bot.send_message(message.chat.id, "Команда не распознана. Используйте кнопки меню.", reply_markup=get_main_markup())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))