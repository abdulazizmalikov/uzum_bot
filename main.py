import time
import requests
from telegram import Bot

# Токены и ID
TELEGRAM_TOKEN = "7666979213:AAESg9nVlPfCkx_lg0gyNUdgoNUFXSbsw0Y"
UZUM_API_KEY = "vCRhQSWjWcuusOQzTTAGP9mnI6op6wTaZ1QU7NgWxac="
CHAT_ID = "998980322"

# URL API Uzum
UZUM_API_URL = "https://api-seller.uzum.uz/api/seller/v1/orders"

# Инициализация бота
bot = Bot(token=TELEGRAM_TOKEN)

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

def send_telegram_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    processed_orders = set()

    # Приветственное сообщение
    send_telegram_message("✅ Бот успешно запущен и ждёт заказы!")

    while True:
        orders = get_new_orders()
        for order in orders:
            order_id = order.get("id")
            if order_id and order_id not in processed_orders:
                customer = order.get("customer", {})
                customer_name = customer.get("name", "Неизвестный клиент")
                items = order.get("items", [])
                items_text = "\n".join([
                    f"- {item.get('productName', 'Товар')} (x{item.get('quantity', 1)})"
                    for item in items
                ])
                message = (
                    f"📦 Новый заказ #{order_id}\n"
                    f"👤 Клиент: {customer_name}\n"
                    f"🛒 Товары:\n{items_text}"
                )
                send_telegram_message(message)
                processed_orders.add(order_id)
        time.sleep(300)

if __name__ == "__main__":
    main()
