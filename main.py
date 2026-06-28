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

# КИБЕР-МЕНЮ
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏢 Жилье", "⛺️ Лагеря", "📜 Легенды", "🚕 Такси", "🚚 Доставка", "📢 Реклама", "⚙️ О системе")
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "```\n"
        "[ SYSTEM ACCESS GRANTED ]\n"
        "STATUS: ONLINE\n"
        "REGION: BAYANAUL_CORE_V1.0\n"
        "```\n"
        "Привет, юзер. Выбери модуль для доступа к данным:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_markup())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    txt = message.text
    
    # ЛЕГЕНДЫ (Подменю)
    if "Легенды" in txt:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add("📖 Жасыбай", "📖 Сабындыколь", "🔙 Главное меню")
        bot.send_message(message.chat.id, "Выберите архив легенд:", reply_markup=markup)
        
    elif "Жасыбай" in txt:
        bot.send_message(message.chat.id, "📜 *Легенда о Жасыбае:*\nБатыр погиб, защищая перевал от врагов. Озеро названо в его честь.", parse_mode="Markdown")

    # ЖИЛЬЕ
    elif "Жилье" in txt:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🏡 VIP-Сектор", "🏠 Эконом-Сектор", "🔙 Главное меню")
        bot.send_message(message.chat.id, "Сканирование доступных ячеек жилья...", reply_markup=markup)

    # ОСНОВНЫЕ МОДУЛИ
    elif "Такси" in txt:
        bot.send_message(message.chat.id, "🚕 *ТРАНСПОРТНЫЙ МОДУЛЬ*\nОператор: 8-777-435-87-77", parse_mode="Markdown")
        
    elif "Доставка" in txt:
        bot.send_message(message.chat.id, "🚚 *ЛОГИСТИКА ЕДЫ*\nGrill Bayanaul: +7 777 127-64-40", parse_mode="Markdown")
        
    elif "Реклама" in txt:
        bot.send_message(message.chat.id, "📢 *ADVERTISING_PROTOCOL*\nСвязь: @Askelad_lucius_Artorius_Castus", parse_mode="Markdown")

    elif "О системе" in txt:
        bot.send_message(message.chat.id, "🖥 *Cyber-Bayanaul v1.0*\nРазработчик: Askelad\nЛокация: Pavlodar Region", parse_mode="Markdown")
        
    elif "Главное меню" in txt or "🔙" in txt:
        send_welcome(message)

    else:
        bot.send_message(message.chat.id, "Команда не распознана. Используйте кнопки управления.", reply_markup=get_main_markup())

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))