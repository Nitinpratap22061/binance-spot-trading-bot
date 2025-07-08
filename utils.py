# utils.py

def is_valid_symbol(symbol):
    return isinstance(symbol, str) and len(symbol) > 0

def is_valid_order_type(order_type):
    return order_type.upper() in ['MARKET', 'LIMIT', 'STOP']

def is_valid_side(side):
    return side.upper() in ['BUY', 'SELL']
