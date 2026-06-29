import telebot
import os
from flask import Flask, request
from telebot import types

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
ADMIN_ID = 7885515418

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- 1. ОБРАБОТЧИК ФОТО (САМЫЙ ПЕРВЫЙ) ---
@bot.message_handler(content_types=['photo', 'document'])
def get_file_id(message):
    if message.chat.id == ADMIN_ID:
        # Получаем ID файла
        if message.content_type == 'photo':
            file_id = message.photo[-1].file_id
        else:
            file_id = message.document.file_id
        
        # Отправляем ответ
        bot.reply_to(message, f"Твой file_id:\n`{file_id}`", parse_mode="Markdown")
        print(f"DEBUG: Успешно отправлен ID: {file_id}")
    else:
        print(f"DEBUG: Фото пришло от чужого ID: {message.chat.id}")

# --- 2. ОБРАБОТЧИК КОМАНДЫ /START ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Добро пожаловать в официальный гид по Баянаулу.", reply_markup=get_main_markup())

# --- 3. ОБРАБОТЧИК ТЕКСТА (СТРОГО ТЕКСТ!) ---
@bot.message_handler(content_types=['text'])
def handle_text(message):
    txt = message.text
    chat_id = message.chat.id

    if txt == "🔙 Назад":
        bot.send_message(chat_id, "Главное меню:", reply_markup=get_main_markup())
    
    elif txt == "🏠 Жилье":
        bot.send_message(chat_id, "Выберите вариант:", reply_markup=get_houses_markup())
    
    elif txt == "🏠 Дом №1":
        bot.send_photo(chat_id, "AgACAgIAAxkBAAICx2pBZtg2C69bIoRxD60hEb104z71AAISG2sblMsRSgNKPSkRUB0jAQADAgADeQADPAQ", caption="🏠 *Дом №1*\nЦена: 7000 ₸ в сутки.\nКонтакт: Наталия 8 777 939 09 67.", parse_mode="Markdown")
    
    elif txt == "🏠 Дом №3":
        bot.send_photo(chat_id, "AgACAgIAAxkBAAIFG2pBc0FWZVvHWqviCs-aAkcea32rAAIdHGsblMsRSmRJU6_AbfyeAQADAgADEQADPAQ", caption="🏠 *Cheremushki Glemp*\n📍 Баянаул, озеро Сабындыколь.\n\n💰 *Цены:*\n• Будние дни: 20 000 ₸/сутки\n• Выходные дни: 25 000 ₸/сутки\n\n📞 Бронирование: +7 705 455 91 33.", parse_mode="Markdown")
    
    elif txt == "🏝 Дома отдыха":
        bot.send_message(chat_id, "Выберите озеро:", reply_markup=get_holiday_homes_markup())
    
    # ... (дальше твой код меню, я сократил для наглядности, вставь свой остальной код сюда) ...
    # Главное убедись, что после последнего elif стоит else
    else:
        bot.send_message(chat_id, "Я не понимаю эту команду. Выберите пункт меню.")

# --- ФУНКЦИИ КЛАВИАТУР ---
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏠 Жилье", "🏝 Дома отдыха", "🛠 Услуги", "🍔 Еда и напитки", "📜 Легенды", "📢 Реклама", "ℹ️ О боте")
    return markup

def get_houses_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏠 Дом №1", "🏠 Дом №3", "🔙 Назад")
    return markup

def get_holiday_homes_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏝 Сабындыколь", "🏖 Жасыбай", "🔙 Назад")
    return markup

# --- ВЕБХУК ---
@app.route('/', methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
