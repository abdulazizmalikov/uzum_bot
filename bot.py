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
