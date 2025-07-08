# cli.py
from bot import BasicBot
from config import API_KEY, API_SECRET
from utils import *
import time

def main_menu():
    print("\n📊 Choose an option:")
    print("1. ➕ Place an Order")
    print("2. 💰 Check Balance")
    print("3. 📋 View Open Orders")
    print("4. 🗑 Cancel an Order")
    print("5. 📈 List Symbols with Prices")
    print("6. 🚪 Exit")

def get_order_input():
    symbol = input("🔸 Enter Symbol (e.g., BTCUSDT): ").strip().upper()
    side = input("🔸 Side (BUY / SELL): ").strip().upper()
    order_type = input("🔸 Order Type (MARKET / LIMIT / STOP): ").strip().upper()
    quantity = float(input("🔸 Quantity: "))

    price = None
    stop_price = None

    if order_type == "LIMIT":
        price = float(input("🔸 Enter Limit Price: "))
    elif order_type == "STOP":
        stop_price = float(input("🔸 Enter Stop Price: "))

    print("\n📝 Order Summary:")
    print(f"▶ Symbol: {symbol}")
    print(f"▶ Side: {side}")
    print(f"▶ Type: {order_type}")
    print(f"▶ Quantity: {quantity}")
    if price: print(f"▶ Limit Price: {price}")
    if stop_price: print(f"▶ Stop Price: {stop_price}")

    confirm = input("✅ Proceed? (y/n): ").strip().lower()
    if confirm == 'y':
        return symbol, side, order_type, quantity, price, stop_price
    else:
        return None, None, None, None, None, None

def main():
    bot = BasicBot(API_KEY, API_SECRET)

    while True:
        main_menu()
        choice = input("🔹 Enter choice: ").strip()

        if choice == '1':
            symbol, side, order_type, quantity, price, stop_price = get_order_input()
            if not symbol:
                print("❌ Cancelled by user.")
                continue

            if order_type == "MARKET":
                result = bot.place_market_order(symbol, side, quantity)
            elif order_type == "LIMIT":
                result = bot.place_limit_order(symbol, side, quantity, price)
            elif order_type == "STOP":
                result = bot.place_stop_market_order(symbol, side, quantity, stop_price)
            else:
                print("❌ Invalid order type")
                continue

            print("✅ Order Response:")
            print(result)

        elif choice == '2':
            balances = bot.get_balance()
            print("💰 Your Balance (non-zero only):")
            for b in balances:
                print(f" - {b['asset']}: {b['free']} (free), {b['locked']} (locked)")

        elif choice == '3':
            symbol = input("🔸 Enter symbol to filter (or press Enter to see all): ").strip().upper()
            symbol = symbol if symbol else None
            orders = bot.get_open_orders(symbol)
            print("📋 Open Orders:")
            for o in orders:
                print(f" - ID: {o['orderId']} | Symbol: {o['symbol']} | Type: {o['type']} | Qty: {o['origQty']} | Price: {o['price']}")

        elif choice == '4':
            symbol = input("🔸 Symbol of order to cancel (e.g., BTCUSDT): ").strip().upper()
            order_id = input("🔸 Order ID to cancel: ").strip()
            result = bot.cancel_order(symbol, int(order_id))
            print("🗑 Cancel Response:")
            print(result)

        elif choice == '5':
            prices = bot.get_all_symbols_with_prices()
            print("📈 Symbols and Prices:")
            for sym, price in prices.items():
                print(f" - {sym}: {price}")
            print(f"Total symbols listed: {len(prices)}")

        elif choice == '6':
            print("👋 Exiting... Bye!")
            break

        else:
            print("❌ Invalid choice, try again!")

        time.sleep(1)

if __name__ == "__main__":
    main()
