import telebot
import os
from flask import Flask, request
from telebot import types

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- ГЛАВНОЕ МЕНЮ ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🏠 Жилье"), types.KeyboardButton("🏠 Базы отдыха"))
    markup.add(types.KeyboardButton("🏔 Локации"), types.KeyboardButton("📜 Легенды"))
    markup.add(types.KeyboardButton("📍 Как добраться"), types.KeyboardButton("🚕 Такси"))
    markup.add(types.KeyboardButton("ℹ️ О Баянауле"))
    bot.send_message(message.chat.id, "Добро пожаловать в гид по Баянаулу! Выберите раздел:", reply_markup=markup)

# --- ОБРАБОТКА КНОПОК ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "🏔 Локации":
        bot.send_message(message.chat.id, "📍 Выберите локацию:", 
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                             types.KeyboardButton("Баба-Яга"), types.KeyboardButton("Жасыбай"), 
                             types.KeyboardButton("Сабындыколь"), types.KeyboardButton("Торайгыр")
                         ))

    elif message.text == "📜 Легенды":
        bot.send_message(message.chat.id, "📜 Выберите легенду, чтобы узнать историю:", 
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                             types.KeyboardButton("Баба-Яга"), types.KeyboardButton("Жасыбай"), 
                             types.KeyboardButton("Сабындыколь"), types.KeyboardButton("Торайгыр")
                         ))

    elif message.text == "Баба-Яга":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📍 Найти в 2GIS", url="https://2gis.kz/pavlodar/search/%D0%BF%D0%B5%D1%89%D0%B5%D1%80%D0%B0%20%D0%91%D0%B0%D0%B1%D0%B0-%D0%AF%D0%B3%D0%B0"))
        bot.send_message(message.chat.id, "👹 *Легенда о Пещере Бабы-Яги:*\nСкальная фигура, напоминающая старуху, по легенде является окаменевшей колдуньей.", parse_mode="Markdown", reply_markup=markup)

    elif message.text == "Жасыбай":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📍 Найти в 2GIS", url="https://2gis.kz/pavlodar/search/%D0%BE%D0%B7%D0%B5%D1%80%D0%BE%20%D0%96%D0%B0%D1%81%D1%8B%D0%B1%D0%B0%D0%B9"))
        bot.send_message(message.chat.id, "⚔️ *Легенда о Жасыбае:*\nХрабрый батыр, погибший в бою. Озеро названо в его честь.", parse_mode="Markdown", reply_markup=markup)

    elif message.text == "Сабындыколь":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📍 Найти в 2GIS", url="https://2gis.kz/pavlodar/search/%D0%BE%D0%B7%D0%B5%D1%80%D0%BE%20%D0%A1%D0%B0%D0%B1%D1%8B%D0%BD%D0%B4%D1%8B%D0%BA%D0%BE%D0%BB%D1%8C"))
        bot.send_message(message.chat.id, "🧼 *Легенда о Сабындыколе:*\nКрасавица Баян уронила мыло, и озеро стало 'мыльным'.", parse_mode="Markdown", reply_markup=markup)

    elif message.text == "Торайгыр":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📍 Найти в 2GIS", url="https://2gis.kz/pavlodar/search/%D0%BE%D0%B7%D0%B5%D1%80%D0%BE%20%D0%A2%D0%BE%D1%80%D0%B0%D0%B9%D0%B3%D1%8B%D1%80"))
        bot.send_message(message.chat.id, "📖 *Легенда о Торайгыре:*\nОзеро вдохновения великого поэта Султанмахмута.", parse_mode="Markdown", reply_markup=markup)

    elif message.text == "🏠 Базы отдыха":
        bot.send_message(message.chat.id, "🏠 *Базы отдыха:*\n\n• [Султан](https://www.instagram.com/sultan_zhasybay/)", parse_mode="Markdown")

    elif message.text == "🏠 Жилье":
        text_info = """🏠 Домик

💰 Цена: 7000 тг/сутки с человека.
📞 Телефон: +7 (777) 939 09 67
📝 Уютный домик у самого леса, чистый воздух."""
        try:
            # Ищем файл в папке images
            photo = open('images/domik.jpg', 'rb')
            bot.send_photo(message.chat.id, photo, caption=text_info)
            photo.close()
        except FileNotFoundError:
            bot.send_message(message.chat.id, text_info + "\n\n(Фото временно недоступно)")

    elif message.text == "📍 Как добраться":
        bot.send_message(message.chat.id, "🚗 Добраться можно из Павлодара или Экибастуза на авто или маршрутке.")

    elif message.text == "🚕 Такси":
        bot.send_message(message.chat.id, "🚕 Для заказа такси используйте 2GIS или местные службы.")

    elif message.text == "ℹ️ О Баянауле":
        bot.send_message(message.chat.id, "🏔 Баянаул — первый природный парк Казахстана. Жемчужина наших гор!")

    else:
        bot.reply_to(message, "Используйте кнопки для навигации.")

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))