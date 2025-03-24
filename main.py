import time
import threading
import requests
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext

# Токены и ID
TELEGRAM_TOKEN = "7666979213:AAESg9nVlPfCkx_lg0gyNUdgoNUFXSbsw0Y"
UZUM_API_KEY = "vCRhQSWjWcuusOQzTTAGP9mnI6op6wTaZ1QU7NgWxac="
CHAT_ID = 998980322

# URL API Uzum
UZUM_API_URL = "https://api-seller.uzum.uz/api/seller/v1/orders"

# Инициализация бота
bot = Bot(token=TELEGRAM_TOKEN)

# Для отслеживания заказов
processed_orders = set()

def get_new_orders():
    headers = {
        "Authorization": f"Bearer {UZUM_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(UZUM_API_URL, headers=headers)
        if response.status_code == 200:
            return response.json().get('orders', [])
        else:
            print("Ошибка получения заказов:", response.status_code)
            return []
    except Exception as e:
        print("Ошибка запроса:", e)
        return []

def format_order(order):
    order_id = order.get("id")
    customer = order.get("customer", {})
    customer_name = customer.get("name", "Неизвестный клиент")
    items = order.get("items", [])
    items_text = "\n".join([
        f"- {item.get('productName', 'Товар')} (x{item.get('quantity', 1)})"
        for item in items
    ])
    return (
        f"📦 Новый заказ #{order_id}\n"
        f"👤 Клиент: {customer_name}\n"
        f"🛒 Товары:\n{items_text}"
    )

def check_and_notify():
    orders = get_new_orders()
    for order in orders:
        order_id = order.get("id")
        if order_id and order_id not in processed_orders:
            message = format_order(order)
            bot.send_message(chat_id=CHAT_ID, text=message)
            processed_orders.add(order_id)

def periodic_check():
    while True:
        check_and_notify()
        time.sleep(300)  # каждые 5 минут

# === Команды Telegram ===

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Бот запущен. Я буду уведомлять о новых заказах!")

def check(update: Update, context: CallbackContext):
    update.message.reply_text("🔄 Проверяю заказы...")
    check_and_notify()
    update.message.reply_text("✅ Проверка завершена!")

# === Запуск ===

def main():
    # Отправляем сообщение о запуске
    bot.send_message(chat_id=CHAT_ID, text="✅ Бот успешно запущен и ждёт заказы!")

    # Стартуем периодическую проверку заказов в фоновом потоке
    thread = threading.Thread(target=periodic_check)
    thread.start()

    # Обработка команд в Telegram
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("check", check))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
