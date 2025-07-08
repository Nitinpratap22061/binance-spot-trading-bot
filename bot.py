# bot.py
from binance.client import Client
from config import API_KEY, API_SECRET, BASE_URL
from logger import log
import time

class BasicBot:
    def __init__(self, api_key=API_KEY, api_secret=API_SECRET):
        self.client = Client(api_key, api_secret)
        self.client.API_URL = BASE_URL + "/api"

        try:
            server_time = self.client.get_server_time()['serverTime']
            local_time = int(time.time() * 1000)
            self.client._timestamp_offset = server_time - local_time
            log("🕒 Timestamp synced with Binance server.")
        except Exception as e:
            log(f"❌ Error syncing timestamp: {str(e)}", "error")

        log("✅ Bot initialized successfully.")
        self._symbol_cache = None
        self._price_map = None

    # ✅ Market Order
    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='MARKET',
                quantity=quantity,
                recvWindow=6000
            )
            log(f"📦 Market Order placed: {order}")
            return order
        except Exception as e:
            log(f"❌ Market order error: {str(e)}", "error")
            return None

    # ✅ Limit Order with PERCENT_PRICE_BY_SIDE safety
    def place_limit_order(self, symbol, side, quantity, price):
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol.upper())
            current_price = float(ticker['price'])

            # Binance constraint workaround: adjust price within ±5%
            upper = current_price * 1.05
            lower = current_price * 0.95
            if not (lower <= price <= upper):
                price = round(current_price * (0.995 if side.upper() == 'BUY' else 1.005), 2)
                log(f"⚠️ Price adjusted to {price} to meet Binance limits.", "warning")

            order = self.client.create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='LIMIT',
                quantity=quantity,
                price=str(price),
                timeInForce='GTC',
                recvWindow=6000
            )
            log(f"📦 Limit Order placed: {order}")
            return order
        except Exception as e:
            log(f"❌ Limit order error: {str(e)}", "error")
            return None

    # ✅ Stop-Market Order
    def place_stop_market_order(self, symbol, side, quantity, stop_price):
        try:
            order = self.client.create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='STOP_LOSS',
                stopPrice=str(stop_price),
                quantity=quantity,
                timeInForce='GTC',
                recvWindow=6000
            )
            log(f"📦 Stop-Market Order placed: {order}")
            return order
        except Exception as e:
            log(f"❌ Stop-Market order error: {str(e)}", "error")
            return None

    # ✅ Get Balance (non-zero)
    def get_balance(self):
        try:
            info = self.client.get_account(recvWindow=6000)
            balances = info['balances']
            non_zero = [b for b in balances if float(b['free']) > 0 or float(b['locked']) > 0]
            log("💰 Balance fetched.")
            return non_zero
        except Exception as e:
            log(f"❌ Error fetching balance: {str(e)}", "error")
            return []

    # ✅ Get Open Orders
    def get_open_orders(self, symbol=None):
        try:
            symbol = symbol.upper() if symbol else None
            orders = self.client.get_open_orders(symbol=symbol, recvWindow=6000) if symbol else self.client.get_open_orders(recvWindow=6000)
            log("📋 Open orders fetched.")
            return orders
        except Exception as e:
            log(f"❌ Error fetching open orders: {str(e)}", "error")
            return []

    # ✅ Cancel Order
    def cancel_order(self, symbol, order_id):
        try:
            result = self.client.cancel_order(symbol=symbol.upper(), orderId=order_id, recvWindow=6000)
            log(f"🗑 Order {order_id} cancelled.")
            return result
        except Exception as e:
            log(f"❌ Cancel order error: {str(e)}", "error")
            return None

    # ✅ Optimized: Get all symbols with prices (cached)
    def get_all_symbols_with_prices(self):
        try:
            if not self._symbol_cache:
                exchange_info = self.client.get_exchange_info()
                self._symbol_cache = [
                    s['symbol'] for s in exchange_info['symbols']
                    if s['status'] == 'TRADING' and s['quoteAsset'] == 'USDT'
                ]

            if not self._price_map:
                tickers = self.client.get_all_tickers()
                self._price_map = {item['symbol']: item['price'] for item in tickers}

            prices = {
                s: self._price_map[s]
                for s in self._symbol_cache if s in self._price_map
            }

            log("📈 Symbols & prices fetched (optimized).")
            return prices
        except Exception as e:
            log(f"❌ Error fetching symbols/prices: {str(e)}", "error")
            return {}
