import telebot
import os
from flask import Flask, request
from telebot import types

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ МЕНЮ ---
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🏠 Жилье", "🏠 Базы отдыха")
    markup.add("🏔 Локации", "📜 Легенды")
    markup.add("📍 Как добраться", "🚕 Такси")
    markup.add("ℹ️ О Баянауле")
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать в гид по Баянаулу! Выберите раздел:", reply_markup=get_main_markup())

# --- ОБРАБОТКА ВСЕХ КНОПОК ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "🔙 Главное меню":
        send_welcome(message)

    elif message.text == "🏠 Жилье":
        desc = "🏠 *Домик*\n\n💰 Цена: 7000 тг/сутки с человека.\n📞 Телефон: +7 (777) 939 09 67\n📝 Уютный домик у самого леса."
        
        # ВСТАВЬ СЮДА ТОТ ДЛИННЫЙ ID, КОТОРЫЙ ТЕБЕ ПРИШЛЕТ БОТ В ОТВЕТ НА ФОТО
        photo_id = "СЮДА_ВСТАВЬ_ПОЛУЧЕННЫЙ_ID" 
        
        bot.send_photo(message.chat.id, photo_id, caption=desc, parse_mode="Markdown", reply_markup=get_main_markup())

    elif message.text == "🏠 Базы отдыха":
        bot.send_message(message.chat.id, "🏠 *Базы отдыха:*\n\n• [Султан](https://www.instagram.com/sultan_zhasybay/)", parse_mode="Markdown", reply_markup=get_main_markup())

    elif message.text == "🏔 Локации":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add("Баба-Яга", "Жасыбай", "Сабындыколь", "Торайгыр", "🔙 Главное меню")
        bot.send_message(message.chat.id, "📍 Выберите локацию:", reply_markup=markup)

    elif message.text == "📜 Легенды":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add("Баба-Яга", "Жасыбай", "Сабындыколь", "Торайгыр", "🔙 Главное меню")
        bot.send_message(message.chat.id, "📜 Выберите легенду:", reply_markup=markup)

    elif message.text in ["Баба-Яга", "Жасыбай", "Сабындыколь", "Торайгыр"]:
        bot.send_message(message.chat.id, f"Вы выбрали: {message.text}. Здесь будет история...", reply_markup=get_main_markup())

    elif message.text == "📍 Как добраться":
        bot.send_message(message.chat.id, "🚗 Добраться можно из Павлодара или Экибастуза.", reply_markup=get_main_markup())

    elif message.text == "🚕 Такси":
        bot.send_message(message.chat.id, "🚕 Используйте 2GIS для заказа.", reply_markup=get_main_markup())

    elif message.text == "ℹ️ О Баянауле":
        bot.send_message(message.chat.id, "🏔 Баянаул — жемчужина гор!", reply_markup=get_main_markup())

# --- ВЕБХУК (ДЛЯ RENDER) ---
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return "!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))