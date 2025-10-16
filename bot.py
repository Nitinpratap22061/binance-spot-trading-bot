from binance.client import Client
from binance.exceptions import BinanceAPIException
import time
import os
from dotenv import load_dotenv
from logger import log

# 🔐 Load environment variables
load_dotenv()

# --- ENVIRONMENT VARIABLES ---
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
USE_TESTNET = os.getenv("USE_TESTNET", "false").lower() == "true"

# --- BASE URL (Testnet vs Mainnet) ---
BASE_URL = "https://testnet.binance.vision" if USE_TESTNET else "https://api.binance.com"


class BasicBot:
    def __init__(self, api_key=API_KEY, api_secret=API_SECRET):
        """Initialize Binance client safely with timestamp sync."""
        try:
            if not api_key or not api_secret:
                raise ValueError("API_KEY or API_SECRET is missing in environment variables.")

            self.client = Client(api_key, api_secret)
            self.client.API_URL = BASE_URL + "/api"

            # ⏱ Sync timestamp
            try:
                server_time = self.client.get_server_time()["serverTime"]
                local_time = int(time.time() * 1000)
                self.client._timestamp_offset = server_time - local_time
                log("🕒 Timestamp synced with Binance server.")
            except Exception as e:
                log(f"⚠️ Could not sync timestamp: {e}", "warning")

            mode = "Testnet" if USE_TESTNET else "Mainnet"
            log(f"✅ Bot initialized successfully ({mode}).")

        except Exception as e:
            log(f"❌ Error initializing Binance client: {e}", "error")

        self._symbol_cache = None
        self._price_map = None

    # 💹 MARKET ORDER
    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type="MARKET",
                quantity=quantity,
                recvWindow=6000
            )
            log(f"📦 Market Order placed: {order}")
            return order
        except BinanceAPIException as e:
            log(f"❌ Binance API Error: {e.message}", "error")
            return None
        except Exception as e:
            log(f"❌ Market order error: {e}", "error")
            return None

    # 💰 LIMIT ORDER
    def place_limit_order(self, symbol, side, quantity, price):
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol.upper())
            current_price = float(ticker["price"])

            # ✅ Adjust price if out of Binance’s ±5% range
            upper = current_price * 1.05
            lower = current_price * 0.95
            if not (lower <= price <= upper):
                price = round(
                    current_price * (0.995 if side.upper() == "BUY" else 1.005), 2
                )
                log(f"⚠️ Price adjusted to {price} to meet Binance limits.", "warning")

            order = self.client.create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type="LIMIT",
                quantity=quantity,
                price=str(price),
                timeInForce="GTC",
                recvWindow=6000
            )
            log(f"📦 Limit Order placed: {order}")
            return order
        except BinanceAPIException as e:
            log(f"❌ Binance API Error: {e.message}", "error")
            return None
        except Exception as e:
            log(f"❌ Limit order error: {e}", "error")
            return None

    # 🚨 STOP-MARKET ORDER
    def place_stop_market_order(self, symbol, side, quantity, stop_price):
        try:
            order = self.client.create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type="STOP_LOSS_MARKET",
                stopPrice=str(stop_price),
                quantity=quantity,
                recvWindow=6000
            )
            log(f"📦 Stop-Market Order placed: {order}")
            return order
        except BinanceAPIException as e:
            log(f"❌ Binance API Error: {e.message}", "error")
            return None
        except Exception as e:
            log(f"❌ Stop-Market order error: {e}", "error")
            return None

    # 💼 GET BALANCE
    def get_balance(self):
        try:
            info = self.client.get_account(recvWindow=6000)
            balances = info.get("balances", [])
            non_zero = [
                b for b in balances
                if float(b["free"]) > 0 or float(b["locked"]) > 0
            ]
            log("💰 Balance fetched successfully.")
            return non_zero
        except BinanceAPIException as e:
            log(f"❌ Binance API Error: {e.message}", "error")
            return []
        except Exception as e:
            log(f"❌ Error fetching balance: {e}", "error")
            return []

    # 📋 GET OPEN ORDERS
    def get_open_orders(self, symbol=None):
        try:
            orders = (self.client.get_open_orders(symbol=symbol.upper(), recvWindow=6000)
                      if symbol else self.client.get_open_orders(recvWindow=6000))
            log("📋 Open orders fetched.")
            return orders
        except BinanceAPIException as e:
            log(f"❌ Binance API Error: {e.message}", "error")
            return []
        except Exception as e:
            log(f"❌ Error fetching open orders: {e}", "error")
            return []

    # 🗑 CANCEL ORDER
    def cancel_order(self, symbol, order_id):
        try:
            result = self.client.cancel_order(
                symbol=symbol.upper(), orderId=order_id, recvWindow=6000
            )
            log(f"🗑 Order {order_id} cancelled successfully.")
            return result
        except BinanceAPIException as e:
            log(f"❌ Binance API Error: {e.message}", "error")
            return None
        except Exception as e:
            log(f"❌ Cancel order error: {e}", "error")
            return None

    # 📈 GET SYMBOLS & PRICES
    def get_all_symbols_with_prices(self):
        try:
            if not self._symbol_cache:
                exchange_info = self.client.get_exchange_info()
                self._symbol_cache = [
                    s["symbol"]
                    for s in exchange_info["symbols"]
                    if s["status"] == "TRADING" and s["quoteAsset"] == "USDT"
                ]

            tickers = self.client.get_all_tickers()
            prices = {t["symbol"]: t["price"] for t in tickers if t["symbol"] in self._symbol_cache}

            log("📈 Symbols & prices fetched successfully.")
            return prices
        except BinanceAPIException as e:
            log(f"❌ Binance API Error: {e.message}", "error")
            return {}
        except Exception as e:
            log(f"❌ Error fetching symbols/prices: {e}", "error")
            return {}
