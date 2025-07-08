# 📈 Binance Spot Trading Bot (Testnet)

A Python-powered trading bot with a Streamlit interface to interact with the **Binance Spot Testnet**. This bot provides an intuitive way to simulate placing and managing spot trades without using real funds.

---

## 🚀 Overview

This bot is designed for learning and testing trading strategies in a safe, sandboxed environment using Binance Testnet APIs. The key features include:

- Placing **Market**, **Limit**, and **Stop-Market** orders.
- Viewing **real-time balances** and **open orders**.
- Cancelling orders directly from a web-based UI.
- Viewing **live symbol prices**.

---

## 🛠 Technologies Used

- **[binance](https://github.com/binance/binance-spot-api-docs)** Python SDK  
- **Streamlit** – Fast and simple UI for Python apps  
- **Python Logging** – Track operations and errors for debugging

---

## ⚙️ Functionalities

### 1. 📦 Place Orders

Supports the following order types:

- **MARKET** – Executes immediately at the current price.
- **LIMIT** – Executes when the market price hits your defined limit.
  - Automatically adjusts price within Binance bounds to avoid `PERCENT_PRICE_BY_SIDE` errors.
- **STOP-MARKET** – Triggers a market order once a specific stop price is reached.

---

### 2. 💰 View Balances

- Fetches non-zero balances from your Binance Testnet account.
- Displays both **available** and **locked** funds.
- Helpful for checking capital before trading.

---

### 3. 📋 View Open Orders

- View open orders for a specific symbol (e.g., `BTCUSDT`) or all symbols.
- Displays:
  - Order ID
  - Symbol
  - Side (BUY/SELL)
  - Price & Quantity
  - Timestamp

---

### 4. 🗑 Cancel Orders

- Cancel any open order by specifying:
  - Trading pair (symbol)
  - Order ID
- Handy for correcting mistakes or removing stale/pending orders.

---

### 5. 🔍 View Symbol Prices

- Shows all symbols with **USDT** as the quote currency.
- Displays **live prices** fetched from Binance Testnet.
- Helps in market overview and entry point decisions.

---

## 🧠 Optimization & Error Handling

- ⏱ Syncs system time with Binance server to avoid `-1021 timestamp errors`.
- 📉 Filters price for LIMIT orders to avoid `-1013 filter failures`.
- 🔄 Batches API requests efficiently to reduce latency and rate-limit issues.
- 🛑 All sensitive logic wrapped in `try-except` blocks to ensure app stability.
- 🪟 Uses `recvWindow` param in API requests to avoid timing errors.

---

## 📁 File Structure

```bash
.
├── app.py         # Streamlit UI logic
├── bot.py         # Core Binance API logic
├── logger.py      # Logs actions and errors
├── config.py      # Stores API keys and Testnet endpoint
├── README.md      # Project documentation
└── report.docx    # Optional Word/PDF summary
```

---

## 🚀 Getting Started

### 🔐 Prerequisites

- Python 3.7+
- Binance Testnet Account (https://testnet.binance.vision/)
- Binance API Key & Secret

### 📦 Installation

```bash
git clone https://github.com/your-username/binance-spot-testnet-bot.git
cd binance-spot-testnet-bot
pip install -r requirements.txt
```

### 🔑 Configure API Keys

Edit the `config.py` file:

```python
API_KEY = "your_testnet_api_key"
API_SECRET = "your_testnet_api_secret"
BASE_URL = "https://testnet.binance.vision"
```

### ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧪 Use Cases

- Learning how to use Binance API
- Simulating trading strategies without risking real money
- Educational/training tool for trading enthusiasts
- Prototyping automated trading systems

---

## 📌 Notes

- This bot uses the **Binance Spot Testnet**, which **does not involve real money**.
- API keys for Testnet are different from the main Binance account.
- Streamlit runs on `http://localhost:8501` by default.

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [Binance API Docs](https://binance-docs.github.io/apidocs/spot/en/)
- [Streamlit](https://streamlit.io/)
- Contributors, testers, and the open-source community ❤️
