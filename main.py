тimport telebot
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
        bot.reply_to(message, f"📸 ID фото: `{message.photo[-1].file_id}`", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать в цифровой гид по Баянаулу! 🏔", reply_markup=get_main_markup())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "🔙 Главное меню":
        send_welcome(message)
    
    elif message.text == "🏠 Жилье":
        # Твой ID вставлен сюда:
        photo_id = "AgACAgIAAxkBAAIBPGpAGjHsRzNxN8Fp0FxGxh580C5iAAIFGGsblMsJSkDowOd5raV3AQADAgADeQADPAQ"
        desc = "🏠 *Уютный домик*\n\n💰 Цена: 7000 тг/сутки с человека.\n📞 Телефон: +7 (777) 939 09 67\n📝 Ваш идеальный отдых в окружении гор."
        bot.send_photo(message.chat.id, photo_id, caption=desc, parse_mode="Markdown", reply_markup=get_main_markup())

    elif message.text == "🏠 Базы отдыха":
        bot.send_message(message.chat.id, "🏠 *Базы отдыха:*\n• [Султан](https://www.instagram.com/sultan_zhasybay/)", parse_mode="Markdown", reply_markup=get_main_markup())

    elif message.text == "🏔 Локации":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add("Баба-Яга", "Жасыбай", "Сабындыколь", "Торайгыр", "🔙 Главное меню")
        bot.send_message(message.chat.id, "📍 Выберите локацию:", reply_markup=markup)

    elif message.text == "📜 Легенды":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add("Баба-Яга", "Жасыбай", "Сабындыколь", "Торайгыр", "🔙 Главное меню")
        bot.send_message(message.chat.id, "📜 Выберите легенду:", reply_markup=markup)

    elif message.text in ["Баба-Яга", "Жасыбай", "Сабындыколь", "Торайгыр"]:
        stories = {
            "Баба-Яга": "👹 *Легенда о пещере Бабы-Яги:*\nСкала, напоминающая сгорбленную старуху — это окаменевшая колдунья, навеки застывшая в камне, охраняя тайны баянаульских лесов.",
            "Жасыбай": "⚔️ *Легенда об озере Жасыбай:*\nОзеро названо в честь славного батыра Жасыбая, героически погибшего, прикрывая отход своего народа от захватчиков.",
            "Сабындыколь": "✨ *Легенда о Сабындыколь:*\nНазвание означает «мыльное озеро». По легенде, Баян-Сулу обронила в озеро свое мыло, и вода стала такой же гладкой и нежной.",
            "Торайгыр": "🏔 *Легенда о Торайгыр:*\nОзеро, названное в честь знаменитого поэта Султанмахмута Торайгырова, воспевшего красоту этого края."
        }
        bot.send_message(message.chat.id, stories.get(message.text, "История скоро появится!"), parse_mode="Markdown", reply_markup=get_main_markup())

    elif message.text == "🚕 Такси по Баянаулу":
        text = ("🚕 *Такси по Баянаулу и району*\n\n"
                "📞 8 (777) 435-87-77\n"
                "📞 8 (705) 699-64-65\n\n"
                "🍷 Услуга «Трезвый водитель».")
        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_markup())

    elif message.text == "🚚 Доставка":
        text = ("🍗 *Grill Bayanaul*\n\n"
                "• Куры гриль: от 4000 тг\n"
                "• Фри: 750 тг | Наггетсы: 1200 тг\n"
                "🕒 Работаем: 09:00 - 00:00\n"
                "🚚 Доставка: 500 тг (09:00 - 21:00)\n"
                "📞 +7 (777) 127-64-40")
        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_markup())

    elif message.text == "ℹ️ О Баянауле":
        bot.send_message(message.chat.id, "🏔 *Баянаул — край легенд и героев!*\n\nЭто колыбель выдающихся ученых, поэтов и деятелей. Край кристальных озер и уникальных скал, вдохновляющий на великие свершения!", parse_mode="Markdown", reply_markup=get_main_markup())

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return "!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))