import telebot
import os
from flask import Flask, request
from telebot import types

# Конфигурация
TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
VERSION = "v2.0.6 (FINAL_MENU_STRUCTURE)"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- КЛАВИАТУРЫ ---
def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏠 Жилье", "🏝 Дома отдыха", "🛠 Услуги", "🍔 Еда и напитки", "📜 Легенды", "📢 Реклама", "ℹ️ О боте")
    return markup

def get_houses_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏠 Дом №1", "🏠 Дом №2", "🏠 Дом №3", "🔙 Назад")
    return markup

def get_holiday_homes_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏝 Сабындыколь", "🏖 Жасыбай", "🔙 Назад")
    return markup

def get_services_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🚕 Такси", "🏗 Сварка", "⚡️ Электрик", "⛺️ Юрты", "🔙 Назад")
    return markup

def get_food_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🍺 BeerPoint", "🍹 Bar 2", "🔥 Шашлыки", "🔙 Назад")
    return markup

def get_legends_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📜 Жасыбай", "📜 Сабындыколь", "📜 Кемпиртас", "🔙 Назад")
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

@bot.message_handler(content_types=['photo'])
def get_photo_id(message):
    file_id = message.photo[-1].file_id
    bot.reply_to(message, f"📸 *Твой file_id для кода:*\n`{file_id}`", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Добро пожаловать в официальный гид по Баянаулу. Выберите раздел:", reply_markup=get_main_markup())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    txt = message.text

    if txt == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=get_main_markup())

    # --- ЖИЛЬЕ ---
    elif txt == "🏠 Жилье":
        bot.send_message(message.chat.id, "Выберите вариант:", reply_markup=get_houses_markup())
    
    elif txt == "🏠 Дом №1":
        bot.send_photo(message.chat.id, "AgACAgIAAxkBAAICx2pBZtg2C69bIoRxD60hEb104z71AAISG2sblMsRSgNKPSkRUB0jAQADAgADeQADPAQ", 
                       caption="🏠 *Дом №1*\nЦена: 7000 ₸ в сутки.\nКонтакт: Наталия 8 777 939 09 67.", parse_mode="Markdown")
    
    elif txt == "🏠 Дом №2":
        bot.send_message(message.chat.id, "🏠 *Дом №2*\nУютный дом.\nInstagram: [bulbul.realtor](https://instagram.com/bulbul.realtor)", parse_mode="Markdown")
    
    elif txt == "🏠 Дом №3":
        bot.send_photo(message.chat.id, "AgACAgIAAxkBAAIFG2pBc0FWZVvHWqviCs-aAkcea32rAAIdHGsblMsRSmRJU6_AbfyeAQADAgADEQADPAQ", 
                       caption="🏠 *Cheremushki Glemp*\n📍 Баянаул, озеро Сабындыколь.\n\n💰 *Цены:*\n• Будние дни: 20 000 ₸/сутки\n• Выходные дни: 25 000 ₸/сутки\n\n📞 Бронирование: +7 705 455 91 33.", parse_mode="Markdown")

    # --- ДОМА ОТДЫХА ---
    elif txt == "🏝 Дома отдыха":
        bot.send_message(message.chat.id, "Выберите озеро:", reply_markup=get_holiday_homes_markup())
    
    elif txt == "🏝 Сабындыколь":
        bot.send_message(message.chat.id, "🏝 *Сабындыколь*\nИнформация по базам отдыха уточняется.", parse_mode="Markdown")
    
    elif txt == "🏖 Жасыбай":
        # Сюда вставь реальную ссылку вместо 'instagram.com/sultan_link'
        bot.send_message(message.chat.id, "🏖 *Базы отдыха на озере Жасыбай:*\n\n1. [Султан](https://instagram.com/sultan_link)", parse_mode="Markdown")

    # --- УСЛУГИ ---
    elif txt == "🛠 Услуги":
        bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=get_services_markup())
    elif txt == "🚕 Такси":
        bot.send_message(message.chat.id, "🚕 *Такси (Диспетчеры):*\n8 705 707 7262, 8 747 612 7162\n\n*Частные водители:*\n8 705 340 8663, 8 771 850 1458, 8 706 721 3032, 8 777 435 8777", parse_mode="Markdown")
    elif txt == "🏗 Сварка":
        bot.send_message(message.chat.id, "🏗 *Сварщик (Ринат):* 8 705 342 7371", parse_mode="Markdown")
    elif txt == "⚡️ Электрик":
        bot.send_message(message.chat.id, "⚡️ *Электрик (Болат):* 8 771 277 7021", parse_mode="Markdown")
    elif txt == "⛺️ Юрты":
        bot.send_message(message.chat.id, "⛺️ *Юрты (Сарыарка):*\n8 705 769 9383\nДоп. номера: 8 705 606 1067, 8 706 721 3032", parse_mode="Markdown")

    # --- ЕДА ---
    elif txt == "🍔 Еда и напитки":
        bot.send_message(message.chat.id, "Выберите заведение:", reply_markup=get_food_markup())
    elif txt == "🍺 BeerPoint":
        bot.send_message(message.chat.id, "🍺 *BeerPoint*\nРежим работы: 10:00 - 23:00.\nДоставка: 8 705 176 5220, 8 705 501 8458", parse_mode="Markdown")
    elif txt == "🍹 Bar 2":
        bot.send_message(message.chat.id, "🍹 *Bar 2*\nИнформация о меню уточняется.", parse_mode="Markdown")
    elif txt == "🔥 Шашлыки":
        bot.send_message(message.chat.id, "🔥 *Шашлыки (Халал)*\nЗаказ по телефону: +7 777 688 6689", parse_mode="Markdown")

    # --- ЛЕГЕНДЫ ---
    elif txt == "📜 Легенды":
        bot.send_message(message.chat.id, "Выберите легенду:", reply_markup=get_legends_markup())
    elif txt == "📜 Жасыбай":
        bot.send_message(message.chat.id, "📜 *Легенда о Жасыбае*\nДревнее предание гласит, что Жасыбай батыр, защищая свой народ от набегов джунгар, совершил невероятный подвиг. Он занял стратегическую оборону в узком горном проходе. Несмотря на численное превосходство врага, батыр держался до последнего, но получил смертельное ранение. Умирая, он попросил похоронить его там, откуда видна родная степь. Теперь его именем названо самое красивое озеро Баянаула.", parse_mode="Markdown")
    elif txt == "📜 Сабындыколь":
        bot.send_message(message.chat.id, "📜 *Легенда о Сабындыколе*\nНазвание озера переводится как 'Мыльное озеро'. Легенда рассказывает о прекрасной Баян-Сулу, которая, умываясь у берега, случайно уронила свой кусок мыла в прозрачные воды. Вода вмиг стала удивительно мягкой и нежной, как будто приняла в себя чистоту и красоту самой девушки. С тех пор вода в озере славится своими целебными свойствами.", parse_mode="Markdown")
    elif txt == "📜 Кемпиртас":
        bot.send_message(message.chat.id, "📜 *Легенда о Кемпиртас*\nВ народе говорят о мудрой старухе, чьи сыновья ушли на войну защищать родную землю. Она каждое утро поднималась на высокую скалу и вглядывалась вдаль, ожидая их возвращения. Прошли годы, она так и не дождалась вестей, но её вера и материнская любовь были настолько сильны, что боги решили увековечить её образ. Она окаменела, и теперь скала Кемпиртас вечно охраняет покой этих мест.", parse_mode="Markdown")

    # --- РЕКЛАМА ---
    elif txt == "📢 Реклама":
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=get_ads_markup())
    elif txt == "💰 Стоимость":
        bot.send_message(message.chat.id, "💰 *Стоимость*\nРазмещение объявления — 500 ₸ в месяц.", parse_mode="Markdown")
    elif txt == "📋 Условия размещения":
        bot.send_message(message.chat.id, "✅ *Условия:*\nТематика должна соответствовать туризму и отдыху. Без спама и мошенничества.", parse_mode="Markdown")
    elif txt == "👤 Контакты":
        bot.send_message(message.chat.id, "👤 *Администратор бота:*\nСвяжитесь по вопросам рекламы: [Админ](https://t.me/Askelad_lucius_Artorius_Castus)", parse_mode="Markdown")
    
    # --- ИНФО ---
    elif txt == "ℹ️ О боте":
        bot.send_message(message.chat.id, f"ℹ️ *Баянаул-помощник {VERSION}*\n\nЭтот бот — ваш личный гид по Баянаулу. Мы собрали всё самое важное: от проверенных домов отдыха до легенд нашего края.\n\nРазработчик: [Админ](https://t.me/Askelad_lucius_Artorius_Castus)", parse_mode="Markdown")
    
    else:
        bot.send_message(message.chat.id, "Команда не найдена. Воспользуйтесь меню.", reply_markup=get_main_markup())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))