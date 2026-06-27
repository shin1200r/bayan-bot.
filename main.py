import telebot
from telebot import types
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# === КОСТЫЛЬ ДЛЯ RENDER (чтобы сервис не засыпал и был статус Live) ===
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

# Запуск фейкового веб-сервера в отдельном потоке
threading.Thread(target=run_server, daemon=True).start()
# ====================================================================

# 🔴 ВСТАВЬ СВОЙ ТОКЕН СЮДА (ПОЛУЧЕННЫЙ У @BotFather)
TOKEN = '8201596025:AAHi7UUJdAr6EWX6JiQAISrnaDsrDHRPvWA'
bot = telebot.TeleBot(TOKEN)

# Главное меню
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton("🏠 Дома отдыха")
    btn2 = types.KeyboardButton("🔑 Жилье в аренду")
    btn3 = types.KeyboardButton("🚘 Таксисты")
    btn4 = types.KeyboardButton("🗺 Экскурсия и Гид")
    btn5 = types.KeyboardButton("🛠 Шиномонтаж и Карта")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4, btn5)
    
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n\nРады видеть тебя в Баянауле. Выбери нужную категорию:",
        reply_markup=markup
    )

# Обработка всех нажатий
@bot.message_handler(content_types=['text'])
def handle_text(message):
    
    # === ДОМА ОТДЫХА ===
    if message.text == "🏠 Дома отдыха":
        text = ("**🏠 Дома отдыха на озере Жасыбай:**\n\n"
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
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

# Бесконечный запуск с защитой от падений
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Ошибка пуллинга: {e}")
        import time
        time.sleep(5)