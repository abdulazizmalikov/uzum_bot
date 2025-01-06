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
openai.api_key = OPENAI_API_KEY

# Функция приветствия
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я ИИ-бот ThermoPlus. Напиши мне любой вопрос.")

# Обработка сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    try:
        # Новый способ вызова API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты умный помощник."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response['choices'][0]['message']['content']
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text(f"Извините, произошла ошибка: {str(e)}")


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
