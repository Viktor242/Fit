import telebot
import random
import threading
import time
from telebot import types
import datetime
import os

bot = telebot.TeleBot('7816515855:AAF1idjN_00bUSGViUXHLEbw5CMNchEolM4')

# Команда /start — приветствие и меню
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💧Расписание")
    btn2 = types.KeyboardButton("📚 Факты о ЗОЖ")
    btn3 = types.KeyboardButton("🥪 Перекус")
    btn4 = types.KeyboardButton("💪 Персональные тренировки")
    btn5 = types.KeyboardButton("⚙️ Поддержка")
    markup.add(btn1, btn2, btn3, btn4,btn5 )

    # Запуск приветствия
    bot.send_message(message.chat.id,
                     "🚀 Добро пожаловать в ЗОЖ-Bot!\nВыберите действие:",
                     reply_markup=markup)

    # Запуск потока для напоминаний
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,), daemon=True)
    reminder_thread.start()

# Обработка кнопки "Факты о здоровом образе жизни"
@bot.message_handler(func=lambda message: message.text == "📚 Факты о ЗОЖ")
def handle_fact_button(message):
    facts = [
        "🏃‍♂️ Регулярные физические нагрузки улучшают здоровье сердца и повышают энергию.",
        "🥗 Правильное питание укрепляет иммунитет и поддерживает обмен веществ.",
        "😴 Хороший сон восстанавливает организм и улучшает психоэмоциональное состояние.",
        "🚭 Отказ от вредных привычек снижает риск хронических заболеваний."
    ]
    random_fact = random.choice(facts)
    bot.send_message(message.chat.id, f"📚 Факт о ЗОЖ:\n\n{random_fact}")


# Обработка кнопки "Поддержка"
@bot.message_handler(func=lambda message: message.text == "⚙️ Поддержка")
def handle_support(message):
    help_text = [
        "⚙️ Привет! Я чат-бот вашей службы поддержки, посвященный ЗОЖ. Чем могу помочь?",
        "Выберите одну из опций ниже:",
        "1️⃣ **Как запустить чат-бот** - Напишите /start для начала работы с ботом.",
        "2️⃣ **Расписание** - Получите информацию о расписании приема воды.",
        "3️⃣ **Факты о здоровом образе жизни** - Интересные и полезные факты о здоровье.",
        "4️⃣ **Как написать в тех. поддержку** - Напиши /help.",
        "5️⃣ **Персональные тренировки** - Контроль физической активности."
    ]
    bot.send_message(message.chat.id, "\n".join(help_text), parse_mode="Markdown")

# Обработка кнопки "Расписание"
@bot.message_handler(func=lambda message: message.text == "💧Расписание")
def handle_schedule(message):
    schedule = [
        "💧 Расписание приема воды:",
        "• Утром - выпейте стакан воды сразу после пробуждения (Напоминание).",
        "• Каждый час - пейте по 1 стакану воды."
    ]
    bot.send_message(message.chat.id, "\n".join(schedule))


@bot.message_handler(func=lambda m: m.text == "🥪 Перекус")
def support_handler(message):
    image_path = "image.jpg"  # Заменить на нужное изображение

    if os.path.exists(image_path):
        with open(image_path, 'rb') as img:
            bot.send_photo(message.chat.id, img, caption="Правильное питание, залог долголетия!")


@bot.message_handler(func=lambda m: m.text == "💪 Персональные тренировки")
def handle_personal_training(message):
    # Создаем инлайн-клавиатуру с кнопкой
    markup = types.InlineKeyboardMarkup()

    # Добавляем кнопку со ссылкой на приложение
    markup.add(
        types.InlineKeyboardButton(
            text="📲 Установить приложение для Android",
            url="https://play.google.com/store/apps/details?id=com.omy.run"
        )
    )
    # Отправляем сообщение с кнопкой
    bot.send_message(
        chat_id=message.chat.id,
        text="""💪 <b>Персональные тренировки</b>

Для индивидуальной программы тренировок установите приложение:""",
        parse_mode="HTML",
        reply_markup=markup
    )

def send_reminders(chat_id):
    reminder_time = "22:35"  # Задаем время для первого напоминания
    while True:
        # Получаем текущее время в формате HH:MM
        now = datetime.datetime.now().strftime("%H:%M")

        # Проверяем, совпадает ли текущее время с временем напоминания
        if now == reminder_time:
            bot.send_message(chat_id, "💧 Напоминание - выпей стакан воды!")
            # Ожидаем 60 секунд перед следующей проверкой, чтобы не отправить несколько уведомлений
            time.sleep(60)
        else:
            time.sleep(20)

# Запуск бота
bot.polling(none_stop=True)