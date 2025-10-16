# app.py
import streamlit as st
from bot import BasicBot
import os
from dotenv import load_dotenv

#  Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Initialize bot
bot = BasicBot(API_KEY, API_SECRET)

#Fetch symbols + prices once
symbol_prices = bot.get_all_symbols_with_prices()
symbols = list(symbol_prices.keys())

#  App Title
st.set_page_config(page_title="Binance Spot Bot", page_icon="")
st.title(" Binance Spot Trading Bot (Testnet)")
st.markdown(" Place trades, view balances & manage orders on Binance Testnet.")

# Sidebar Menu
menu = st.sidebar.selectbox(" Select Action", [
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
        current_price = symbol_prices[symbol]
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
                if order_type == "MARKET":
                    result = bot.place_market_order(symbol, side, quantity)
                elif order_type == "LIMIT":
                    result = bot.place_limit_order(symbol, side, quantity, price)
                elif order_type == "STOP":
                    result = bot.place_stop_market_order(symbol, side, quantity, stop_price)

                if result:
                    st.success("✅ Order Placed!")
                    st.json(result)
                else:
                    st.error("❌ Failed to place order.")

# 💰 2. Balance
elif menu == "💰 Check Balance":
    st.subheader("💰 Your Balances")
    balances = bot.get_balance()
    if not balances:
        st.warning("No assets found.")
    for b in balances:
        st.write(f"{b['asset']} → Free: {b['free']} | Locked: {b['locked']}")

# 📋 3. Open Orders
elif menu == "📋 Open Orders":
    st.subheader("📋 Your Open Orders")
    symbol = st.selectbox("Select Symbol (optional)", ["All"] + symbols)
    if st.button("Fetch Orders"):
        selected_symbol = symbol if symbol != "All" else None
        orders = bot.get_open_orders(selected_symbol)
        if not orders:
            st.info("No open orders found.")
        else:
            for o in orders:
                st.json(o)

# 🗑 4. Cancel Order
elif menu == "🗑 Cancel Order":
    st.subheader("🗑 Cancel an Order")
    symbol = st.selectbox("Select Symbol", symbols)
    order_id = st.text_input("Order ID")
    if st.button("Cancel"):
        if order_id.isdigit():
            result = bot.cancel_order(symbol, int(order_id))
            if result:
                st.success("✅ Order Cancelled!")
                st.json(result)
            else:
                st.error("❌ Failed to cancel order.")
        else:
            st.error("Please enter a valid numeric order ID.")

# 🔍 5. Symbol Prices
elif menu == "🔍 View Symbols & Prices":
    st.subheader("🪙 Live Prices")
    for sym, price in symbol_prices.items():
        st.write(f"**{sym}** : {price}")
