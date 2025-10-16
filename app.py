# app.py
import streamlit as st
from bot import BasicBot
import os
from dotenv import load_dotenv

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Default to Testnet always (for Streamlit Cloud safety)
USE_TESTNET = os.getenv("USE_TESTNET", "true").lower() == "true"

# ---------------------------
# Initialize the bot
# ---------------------------
try:
    bot = BasicBot(API_KEY, API_SECRET)
    symbol_prices = bot.get_all_symbols_with_prices()
    symbols = list(symbol_prices.keys())
except Exception as e:
    st.error("⚠️ Failed to connect to Binance. Using Testnet mode only.")
    st.exception(e)
    symbols = []
    symbol_prices = {}

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Binance Spot Bot (Testnet)", page_icon="🪙")
st.title("🪙 Binance Spot Trading Bot (Testnet)")
st.markdown("Place trades, view balances & manage orders on **Binance Testnet**.")

menu = st.sidebar.selectbox("Select Action", [
    "💹 Place Order",
    "💰 Check Balance",
    "📋 Open Orders",
    "🗑 Cancel Order",
    "🔍 View Symbols & Prices"
])

# 💹 1. Place Order
if menu == "💹 Place Order":
    st.subheader("💹 Place New Order")

    if not symbols:
        st.warning("⚠️ No symbols found. Please check internet or API connection.")
    else:
        symbol = st.selectbox("Select Symbol", symbols)
        current_price = symbol_prices.get(symbol, "N/A")
        st.info(f"📉 Current Market Price for {symbol}: **{current_price} USDT**")

        side = st.selectbox("Side", ["BUY", "SELL"])
        order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "STOP"])
        quantity = st.number_input("Quantity", min_value=0.0, format="%.6f")

        price = None
        stop_price = None
        if order_type == "LIMIT":
            price = st.number_input("Limit Price", min_value=0.0, format="%.2f")
        elif order_type == "STOP":
            stop_price = st.number_input("Stop Price", min_value=0.0, format="%.2f")

        if st.button("✅ Place Order"):
            if quantity <= 0:
                st.error("Please enter a valid quantity.")
            else:
                result = None
                try:
                    if order_type == "MARKET":
                        result = bot.place_market_order(symbol, side, quantity)
                    elif order_type == "LIMIT":
                        result = bot.place_limit_order(symbol, side, quantity, price)
                    elif order_type == "STOP":
                        result = bot.place_stop_market_order(symbol, side, quantity, stop_price)
                except Exception as e:
                    st.error("❌ Failed to place order.")
                    st.exception(e)

                if result:
                    st.success("✅ Order Placed Successfully!")
                    st.json(result)

# 💰 2. Balance
elif menu == "💰 Check Balance":
    st.subheader("💰 Your Balances")
    try:
        balances = bot.get_balance()
        if not balances:
            st.warning("No assets found.")
        else:
            for b in balances:
                st.write(f"{b['asset']} → Free: {b['free']} | Locked: {b['locked']}")
    except Exception as e:
        st.error("Failed to fetch balances.")
        st.exception(e)

# 📋 3. Open Orders
elif menu == "📋 Open Orders":
    st.subheader("📋 Your Open Orders")
    symbol = st.selectbox("Select Symbol (optional)", ["All"] + symbols)
    if st.button("Fetch Orders"):
        selected_symbol = symbol if symbol != "All" else None
        try:
            orders = bot.get_open_orders(selected_symbol)
            if not orders:
                st.info("No open orders found.")
            else:
                for o in orders:
                    st.json(o)
        except Exception as e:
            st.error("Failed to fetch open orders.")
            st.exception(e)

# 🗑 4. Cancel Order
elif menu == "🗑 Cancel Order":
    st.subheader("🗑 Cancel an Order")
    symbol = st.selectbox("Select Symbol", symbols)
    order_id = st.text_input("Order ID")
    if st.button("Cancel"):
        if order_id.isdigit():
            try:
                result = bot.cancel_order(symbol, int(order_id))
                if result:
                    st.success("✅ Order Cancelled!")
                    st.json(result)
                else:
                    st.error("❌ Failed to cancel order.")
            except Exception as e:
                st.error("Error cancelling order.")
                st.exception(e)
        else:
            st.error("Please enter a valid numeric Order ID.")

# 🔍 5. Symbol Prices
elif menu == "🔍 View Symbols & Prices":
    st.subheader("🪙 Live Prices")
    for sym, price in symbol_prices.items():
        st.write(f"**{sym}** : {price}")
