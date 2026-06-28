import telebot
import os
from flask import Flask, request
from telebot import types

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
WEBHOOK_URL = 'https://bayan-bot-web.onrender.com/' 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL + TOKEN)

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
    # Приводим текст к нижнему регистру для надежности
    text = message.text.strip().lower()
    
    if "реклам" in text:
        ads_info = ("📢 *Размещение рекламы*\n\n"
            "Хотите, чтобы информация о вашем бизнесе появилась в этом боте?\n\n"
            "📩 *Связаться с разработчиком:*\n"
            "@Askelad_lucius_Artorius_Castus")
        bot.send_message(message.chat.id, ads_info, parse_mode="Markdown", reply_markup=get_main_markup())

    elif "жиль" in text:
        photo_id = "AgACAgIAAxkBAAIBPGpAGjHsRzNxN8Fp0FxGxh580C5iAAIFGGsblMsJSkDowOd5raV3AQADAgADeQADPAQ"
        bot.send_photo(message.chat.id, photo_id, caption="🏠 *Уютный домик*", parse_mode="Markdown", reply_markup=get_main_markup())

    elif "доставк" in text:
        text_delivery = "🍗 *Grill Bayanaul*\n📞 +7 (777) 127-64-40"
        bot.send_message(message.chat.id, text_delivery, parse_mode="Markdown", reply_markup=get_main_markup())
    
    else:
        # Если ничего не подошло, отправляем главное меню
        send_welcome(message)

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))