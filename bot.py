import os
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Загрузка переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Функция приветствия
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я ИИ-бот. Напиши мне любой вопрос.")

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
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
