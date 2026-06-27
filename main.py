import telebot
import os
from flask import Flask, request
from telebot import types

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

MY_USER_ID = 7885515418

def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🏠 Жилье", "🏠 Базы отдыха")
    markup.add("🏔 Локации", "📜 Легенды")
    markup.add("🚕 Такси по Баянаулу", "🚚 Доставка")
    markup.add("ℹ️ О Баянауле")
    return markup

@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    if message.from_user.id == MY_USER_ID:
        file_id = message.photo[-1].file_id
        bot.reply_to(message, f"📸 ID этой фотографии:\n`{file_id}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Я принимаю фото только от администратора.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать в цифровой гид по Баянаулу! 🏔", reply_markup=get_main_markup())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "🔙 Главное меню":
        send_welcome(message)

    elif message.text == "🚚 Доставка":
        menu_info = (
            "🍗 *Grill Bayanaul — Меню*\n\n"
            "*Куры гриль:*\n"
            "• Крупные: 5500 тг\n"
            "• Средние: 4500 тг\n"
            "• Мелкие: 4000 тг\n\n"
            "🍟 *Дополнения:*\n"
            "• Фри (150г): 750 тг\n"
            "• Наггетсы (7 шт): 1200 тг\n"
            "• Лаваш: 150 тг\n"
            "• Фирменный соус: 150 тг\n\n"
            "🕒 *График работы:* 09:00 - 00:00\n"
            "🚚 *Доставка:* 500 тг (по Баянаулу с 09:00 до 21:00, далее самовывоз)\n\n"
            "📞 *Заказ:* +7 (777) 127-64-40"
        )
        bot.send_message(message.chat.id, menu_info, parse_mode="Markdown", reply_markup=get_main_markup())

    # ... (далее твоя остальная логика: Жилье, Такси, и т.д.) ...
    
    elif message.text == "🏠 Жилье":
        photo_id = "ВСТАВЬ_СЮДА_ID_КОТОРЫЙ_ПРИШЛЕТ_БОТ" 
        bot.send_photo(message.chat.id, photo_id, caption="🏠 Уютный домик", reply_markup=get_main_markup())

    elif message.text == "🚕 Такси по Баянаулу":
        taxi_info = "🚕 *Такси по Баянаулу:*\n👉 8 (777) 435-87-77\n👉 8 (705) 699-64-65\n🍷 Услуга «Трезвый водитель»."
        bot.send_message(message.chat.id, taxi_info, parse_mode="Markdown", reply_markup=get_main_markup())
    
    # ... (остальные кнопки) ...

    else:
        bot.send_message(message.chat.id, "Используйте кнопки меню.", reply_markup=get_main_markup())

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return "!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))