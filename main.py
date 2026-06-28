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
    markup.add("📢 Реклама", "ℹ️ О Баянауле")
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать в цифровой гид по Баянаулу! 🏔", reply_markup=get_main_markup())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # ДИАГНОСТИКА: выводим в логи Render то, что реально нажал пользователь
    print(f"DEBUG: Получен текст: '{message.text}' от пользователя {message.from_user.id}")
    
    if message.text == "🔙 Главное меню":
        send_welcome(message)
    
    # Используем .strip() для удаления лишних пробелов, если они есть
    elif message.text.strip() == "📢 Реклама":
        ads_info = ("📢 *Размещение рекламы*\n\n"
            "Хотите, чтобы информация о вашем бизнесе появилась в этом боте? "
            "Это отличный способ привлечь туристов в Баянауле!\n\n"
            "📩 *Связаться с разработчиком:*\n"
            "Напишите мне лично: @Askelad_lucius_Artorius_Castus\n"
            "Обсудим условия и форматы размещения.")
        bot.send_message(message.chat.id, ads_info, parse_mode="Markdown", reply_markup=get_main_markup())

    elif message.text == "🏠 Жилье":
        photo_id = "AgACAgIAAxkBAAIBPGpAGjHsRzNxN8Fp0FxGxh580C5iAAIFGGsblMsJSkDowOd5raV3AQADAgADeQADPAQ"
        desc = "🏠 *Уютный домик*\n\n💰 Цена: 7000 тг/сутки с человека.\n📞 Телефон: +7 (777) 939 09 67\n📝 Ваш идеальный отдых в окружении гор."
        bot.send_photo(message.chat.id, photo_id, caption=desc, parse_mode="Markdown", reply_markup=get_main_markup())

    elif message.text == "🚚 Доставка":
        text = ("🍗 *Grill Bayanaul*\n\n"
                "• Куры гриль: от 4000 тг\n"
                "• Фри: 750 тг | Наггетсы: 1200 тг\n"
                "🕒 Работаем: 09:00 - 00:00\n"
                "🚚 Доставка: 500 тг (09:00 - 21:00)\n"
                "📞 +7 (777) 127-64-40")
        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_markup())
    
    else:
        bot.send_message(message.chat.id, "Я получил сообщение, но не знаю такой команды. Нажми /start", reply_markup=get_main_markup())

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))