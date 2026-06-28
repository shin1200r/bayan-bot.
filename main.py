import telebot
import os
from flask import Flask, request
from telebot import types

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Функция для создания клавиатуры
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🏠 Жилье", "🏠 Базы отдыха")
    markup.add("🏔 Локации", "📜 Легенды")
    markup.add("🚕 Такси по Баянаулу", "🚚 Доставка")
    markup.add("📢 Реклама", "ℹ️ О Баянауле")
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать в цифровой гид по Баянаулу! 🏔", reply_markup=get_main_markup())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.strip()
    print(f"DEBUG: Получен текст: {text}") # Для отладки в логах Render

    if text == "🔙 Главное меню":
        send_welcome(message)
    
    # Гибкая проверка кнопки Рекламы
    elif "Реклама" in text:
        ads_info = ("📢 *Размещение рекламы*\n\n"
            "Хотите, чтобы информация о вашем бизнесе появилась в этом боте? "
            "Это отличный способ привлечь туристов в Баянауле!\n\n"
            "📩 *Связаться с разработчиком:*\n"
            "Напишите мне лично: @Askelad_lucius_Artorius_Castus\n"
            "Обсудим условия и форматы размещения.")
        bot.send_message(message.chat.id, ads_info, parse_mode="Markdown", reply_markup=get_main_markup())

    elif "Жилье" in text:
        photo_id = "AgACAgIAAxkBAAIBPGpAGjHsRzNxN8Fp0FxGxh580C5iAAIFGGsblMsJSkDowOd5raV3AQADAgADeQADPAQ"
        desc = "🏠 *Уютный домик*\n\n💰 Цена: 7000 тг/сутки с человека.\n📞 Телефон: +7 (777) 939 09 67\n📝 Ваш идеальный отдых в окружении гор."
        bot.send_photo(message.chat.id, photo_id, caption=desc, parse_mode="Markdown", reply_markup=get_main_markup())

    elif "Доставка" in text:
        text_delivery = ("🍗 *Grill Bayanaul*\n\n"
                "• Куры гриль: от 4000 тг\n"
                "• Фри: 750 тг | Наггетсы: 1200 тг\n"
                "🕒 Работаем: 09:00 - 00:00\n"
                "🚚 Доставка: 500 тг (09:00 - 21:00)\n"
                "📞 +7 (777) 127-64-40")
        bot.send_message(message.chat.id, text_delivery, parse_mode="Markdown", reply_markup=get_main_markup())
    
    else:
        bot.send_message(message.chat.id, f"Вы нажали: {text}. Если бот не отреагировал, нажмите /start", reply_markup=get_main_markup())

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))