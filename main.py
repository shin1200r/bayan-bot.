import telebot
import os
from flask import Flask, request
from telebot import types

TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
VERSION = "v1.2.6"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- КЛАВИАТУРЫ ---
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("⛺️ Дома отдыха", "🏠 Жилье", "🛠 Услуги", "🍔 Еда и напитки", "📜 Легенды", "ℹ️ О боте", "📢 Реклама")
    return markup

def get_rest_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏝 Жасыбай", "💧 Сабындыколь", "🔙 Назад")
    return markup

def get_legends_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📜 Жасыбай", "📜 Сабындыколь", "📜 Кемпиртас", "🔙 Назад")
    return markup

def get_services_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🚕 Такси", "🏗 Сварка", "⛺️ Юрты", "🔙 Назад")
    return markup

# --- ВЕБХУК (ИСПРАВЛЕНИЕ 404) ---
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# --- ОБРАБОТЧИКИ ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Добро пожаловать в Баянаул-бот. Выберите раздел:", reply_markup=get_main_markup())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    txt = message.text

    # Главное меню
    if "Дома отдыха" in txt:
        bot.send_message(message.chat.id, "Выберите локацию:", reply_markup=get_rest_markup())
    
    elif "Жилье" in txt:
        bot.send_message(message.chat.id, "Тут будет информация по доступному жилью.")
        
    elif "Услуги" in txt:
        bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=get_services_markup())
        
    elif "Еда и напитки" in txt:
        msg = ("🍔 *Еда и напитки*\n\n"
               "🍺 *BeerPoint*\n"
               "Различные напитки, пенное, чипсы, закуски.\n"
               "Режим: 10:00 - 23:00 (без выходных).\n"
               "Доставка: 8 705 176 5220, 8 705 501 8458\n\n"
               "🍗 *Grill Bayanaul*\n"
               "Тел: +7 777 127-64-40\n\n"
               "🔥 *Шашлыки (Халал)*\n"
               "Тел: +7 777 688 6689")
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")

    elif "Легенды" in txt:
        bot.send_message(message.chat.id, "Выберите легенду:", reply_markup=get_legends_markup())
        
    elif "ℹ️ О боте" in txt:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🔄 Что нового?", "🔙 Назад")
        bot.send_message(message.chat.id, f"Версия бота: {VERSION}\nРазработчик: Баянаул-бот", reply_markup=markup)
        
    elif "🔄 Что нового?" in txt:
        update_log = ("🚀 *Список изменений (v1.2.6):*\n"
                      "• Исправлена ошибка 404 (бот теперь отвечает!).\n"
                      "• Полная интеграция всех данных (BeerPoint, легенды).\n"
                      "• Навигация полностью восстановлена.")
        bot.send_message(message.chat.id, update_log, parse_mode="Markdown")

    # --- ЛЕГЕНДЫ (ДЛИННЫЕ) ---
    elif "📜 Жасыбай" in txt:
        bot.send_message(message.chat.id, "📜 *Легенда об озере Жасыбай*\n\nМного веков назад Жасыбай батыр, защищая свой народ от джунгар, получил смертельное ранение. Истекая кровью, он добрался до этого красивого озера, спрятанного среди скал, и там обрел покой. С тех пор озеро носит его имя, а его воды считаются священными и целебными.", parse_mode="Markdown")
    
    elif "📜 Сабындыколь" in txt:
        bot.send_message(message.chat.id, "📜 *Легенда об озере Сабындыколь*\n\nНазвание переводится как «Мыльное озеро». По легенде, красавица Баян-Сулу умывалась здесь, и кусок мыла случайно упал в воду. Вода мгновенно стала мягкой и приятной на ощупь, как будто хранит чистоту и нежность самой красавицы. Говорят, эта вода дарит молодость.", parse_mode="Markdown")
    
    elif "📜 Кемпиртас" in txt:
        bot.send_message(message.chat.id, "📜 *Легенда о скале Кемпиртас*\n\nКемпиртас, или «Голова старухи» — это гранитный утес. Старая легенда гласит, что мудрая старуха всю жизнь ждала своих сыновей с войны, всматриваясь в горизонт. Она так долго и неподвижно ждала, что боги превратили её в камень, чтобы увековечить её верность и терпение.", parse_mode="Markdown")

    # --- УСЛУГИ ---
    elif "Такси" in txt:
        msg = ("🚕 *Такси*\n"
               "Диспетчеры: 8 705 707 7262, 8 747 612 7162.\n"
               "Частные: 8 705 340 8663, 8 771 850 1458, 8 706 721 3032, 8 777 435 8777.")
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        
    elif "Сварка" in txt:
        bot.send_message(message.chat.id, "🏗 *Сварщик (Ринат)*: 8 705 342 7371", parse_mode="Markdown")
        
    elif "Юрты" in txt:
        bot.send_message(message.chat.id, "⛺️ *Юрты*: 8 705 769 9383 (Сарыарка), 8 705 606 1067, 8 706 721 3032", parse_mode="Markdown")
    
    # Навигация
    elif "Назад" in txt:
        send_welcome(message)

# --- ЗАПУСК ---
if __name__ == "__main__":
    # Убедись, что WEBHOOK_URL настроен в Render
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))