import os
import openai
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
)

# Загрузка переменных окружения
TELEGRAM_TOKEN = "6743094389:AAGhSkJ0Tt8nQxrBT_SPzQx6zhdNNy49oYI"
OPENAI_API_KEY = "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"

# Настройка OpenAI
openai.api_key = "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"

# Функция приветствия
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я ИИ-бот ThermoPlus. Напиши мне любой вопрос.")

# Обработка сообщений
async def handle_message(update, context):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Или "gpt-3.5-turbo", если используете эту модель
            messages=[
                {"role": "system", "content": "Ты умный помощник, готовый помочь."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response['choices'][0]['message']['content']
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


# Основной цикл бота
def main():
    # Создаём приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
