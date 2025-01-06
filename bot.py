from telegram.ext import filters  # Новый импорт для фильтров
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram import Update
import os
import openai

# Загрузка переменных окружения
TELEGRAM_TOKEN = os.getenv("6743094389:AAFIGOFnDcYYFWPZNEV1I5gzEi_2G9HBjrs")
OPENAI_API_KEY = os.getenv("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")

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Функция приветствия
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я ИИ-бот Thermo Plus. Напиши мне любой вопрос.")

# Обработка сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response["choices"][0]["message"]["content"]
        update.message.reply_text(bot_reply)
    except Exception as e:
        update.message.reply_text("Извините, произошла ошибка: " + str(e))

# Основной цикл бота
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
