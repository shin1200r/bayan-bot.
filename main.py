import telebot
from telebot import types

# 🛑 ВСТАВЬ СВОЙ ТОКЕН СЮДА (ПОЛУЧЕННЫЙ У @BotFather)
TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
bot = telebot.TeleBot(TOKEN)

# Главное меню
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton("🏡 Дома отдыха")
    btn2 = types.KeyboardButton("🔑 Жилье в аренду")
    btn3 = types.KeyboardButton("🚗 Таксисты")
    btn4 = types.KeyboardButton("🗺 Экскурсия и Гид")
    btn5 = types.KeyboardButton("🛠 Шиномонтаж и Карта")
   

    markup.add(btn1, btn2)
    markup.add(btn3, btn4, btn5)
   
    
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! 👋\nРады видеть тебя в Баянауле. Выбери нужную категорию:", 
        reply_markup=markup
    )

# Обработка всех нажатий
@bot.message_handler(content_types=['text'])
def handle_text(message):
    
    # === ДОМА ОТДЫХА ===
    if message.text == "🏡 Дома отдыха":
        text = ("**🏢 Дома отдыха на озере Жасыбай:**\n\n"
                "• Зона отдыха 'Самал'\n📞 +7 (705) 000-00-00\n\n"
                "• Зона отдыха 'Найзатас'\n📞 +7 (707) 000-00-00\n\n"
                "• Отель 'Жасыбай'\n📞 +7 (701) 000-00-00")
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        
# === ЖИЛЬЕ В АРЕНДУ ===
    if message.text == "🔑 Жилье в аренду":
        text = (
            "**🔑 Жилье в аренду в Баянауле:**\n\n"
            "• Сдаются частные дома под ключ\n"
            "• Уютные комнаты в частном секторе\n"
            "• Летние домики и топчаны\n\n"
            "ℹ️ Раздел находится в разработке. Скоро здесь появятся проверенные контакты владельцев!"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    # === ПОДМЕНЮ ТАКСИ ===
    elif message.text == "🚗 Таксисты":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        t1 = types.KeyboardButton("🚖 Баянаул (Внутри)")
        t2 = types.KeyboardButton("🚌 Баянаул - Павлодар")
        t3 = types.KeyboardButton("🚘 Баянаул - Экибастуз")
        t4 = types.KeyboardButton("🏖 Баянаул - Жасыбай")
        t5 = types.KeyboardButton("🏞 Баянаул - Торайгыр")
        t_back = types.KeyboardButton("⬅️ В главное меню")
        markup.add(t1, t2, t3, t4, t5, t_back)
        
        bot.send_message(message.chat.id, "Выбери нужное направление поездки:", reply_markup=markup)
        
    elif message.text == "🚖 Баянаул (Внутри)":
        bot.send_message(message.chat.id, "**🚖 Внутреннее такси по поселку:**\n\n• Водитель Азамат: +7 (701) 333-33-33\n• Водитель Берик: +7 (705) 444-44-44")
    elif message.text == "🚌 Баянаул - Павлодар":
        bot.send_message(message.chat.id, "**🚌 Маршрут Баянаул ↔️ Павлодар:**\n\n• Минивэн (выезд каждое утро):\n• Водитель Сакен: +7 (777) 555-55-55")
    elif message.text == "🚘 Баянаул - Экибастуз":
        bot.send_message(message.chat.id, "**🚘 Маршрут Баянаул ↔️ Экибастуз:**\n\n• Машины на автовокзале / попутки:\n• Водитель Данияр: +7 (707) 666-66-66")
    elif message.text == "🏖 Баянаул - Жасыбай":
        bot.send_message(message.chat.id, "**🏖 Такси Баянаул ↔️ Озеро Жасыбай:**\n\n• Курсируют круглосуточно в сезон:\n• Телефон диспетчера: +7 (747) 777-77-77")
    elif message.text == "🏞 Баянаул - Торайгыр":
        bot.send_message(message.chat.id, "**🏞 Маршрут Баянаул ↔️ Озеро Торайгыр:**\n\n• Водитель Марат: +7 (702) 888-88-88")

    # === ЭКСКУРСИИ И ГИДЫ ===
    elif message.text == "🗺 Экскурсия и Гид":
        text = ("**🥾 Туры, экскурсии и проводники:**\n\n"
                "• **Местный гид Сакен** (Пешие подъемы на Кемпиртас, Найзатас, Коныр-Аулие)\n📞 +7 (705) 999-99-99\n\n"
                "• **Организованная экскурсия** (Автобусные туры с Жасыбая)\n📞 +7 (701) 123-45-67")
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    # === КАРТА И ШИНОМОНТАЖ ===
    elif message.text == "🛠 Шиномонтаж и Карта":
        # Создаем встроенные кнопки со ссылками на карты
        inline_markup = types.InlineKeyboardMarkup()
        
        # Сюда вставляются скопированные из Google Maps / 2ГИС ссылки-карты
        url_map = types.InlineKeyboardButton(text="🗺 Открыть карту Баянаула", url="https://maps.app.goo.gl/uXv7R6T5v2WepS1J9")
        url_shina = types.InlineKeyboardButton(text="🛠 Шиномонтаж на карте", url="https://maps.app.goo.gl/uXv7R6T5v2WepS1J9")

        inline_markup.add(url_map, url_shina)
        
        text_help = ("**🛠 Шиномонтаж и техпомощь:**\n\n"
                     "• **Круглосуточный шиномонтаж (Въезд в Баянаул):**\n"
                     "📍 ул. Сатпаева (напротив АЗС)\n"
                     "📞 Мастер: +7 (705) 555-11-22\n\n"
                     "Нажми на кнопки ниже, чтобы открыть навигатор:")
                     
        bot.send_message(message.chat.id, text_help, reply_markup=inline_markup)
        
        # Бонус: отправка точной гео-точки центра Баянаула прямо в чат
        bot.send_location(message.chat.id, latitude=50.7876, longitude=75.6974)


    # === ВОЗВРАТ В МЕНЮ ===
    elif message.text == "⬅️ В главное меню":
        start_command(message)

# Запуск
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Ошибка: {e}. Перезапуск через 5 секунд...")
        import time
        time.sleep(5)