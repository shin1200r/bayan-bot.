import telebot
import os
from flask import Flask, request
from telebot import types

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
MY_ADMIN_ID = 7885515418  # Твой ID теперь здесь

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- КЛАВИАТУРЫ ---
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("⛺️ Дома отдыха", "🏠 Жилье", "🛠 Услуги", "🍔 Еда и напитки", "📜 Легенды", "ℹ️ О боте", "📢 Реклама")
    return markup

def get_houses_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏠 Дом №1", "🏠 Дом №2", "🔙 Назад")
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

# Обработка фото (только для тебя)
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

    # Навигация
    if txt == "🔙 Назад" or txt == "Главное меню":
        send_welcome(message)
        
    elif "🏠 Жилье" in txt:
        bot.send_message(message.chat.id, "Выберите вариант жилья:", reply_markup=get_houses_markup())
        
    elif "🏠 Дом №1" in txt:
        # ЗАМЕНИ ЭТУ ССЫЛКУ НА СВОЮ
        photo_url = "https://images.unsplash.com/photo-1518780664697-55e3ad937233?q=80&w=1000" 
        text = ("🏠 *Дом №1*\n\n"
                "Все удобства, уютная атмосфера.\n"
                "Подробнее в Instagram: @bulbul.realtor")
        bot.send_photo(message.chat.id, photo_url, caption=text, parse_mode="Markdown")

    elif "🏠 Дом №2" in txt:
        bot.send_message(message.chat.id, 
                         "🏠 *Дом №2*\n\n"
                         "Здесь может быть ваше объявление!\n"
                         "Перейдите в раздел '📢 Реклама', чтобы узнать условия.", 
                         parse_mode="Markdown")

    elif "📢 Реклама" in txt:
        bot.send_message(message.chat.id, "Выберите интересующий вас вопрос по рекламе:", reply_markup=get_ads_markup())

    # --- Подменю Рекламы ---
    elif "📋 Условия размещения" in txt:
        bot.send_message(message.chat.id, "✅ *Условия:*\n1. Реклама должна соответствовать тематике отдыха.\n2. Мы не размещаем запрещенный контент.", parse_mode="Markdown")
    elif "💰 Стоимость" in txt:
        bot.send_message(message.chat.id, "💰 *Стоимость*\nРазмещение в разделе 'Жилье' — 5000 ₸/мес.", parse_mode="Markdown")
    elif "👤 Контакты" in txt:
        bot.send_message(message.chat.id, "👤 *Связь с нами:*\nПишите владельцу: @Askelad_lucius_Artorius_Castus")
    
    # ... Остальные обработчики (Услуги, Еда, Легенды) остаются как были ...

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))