# Simple Angel One Trading Script
from SmartApi import SmartConnect
import pyotp
import time
import requests
import json
import pickle
import dotenv
import os
# Load environment variables from .env file
dotenv.load_dotenv()

# API credentials
api_key = os.getenv("ANGEL_ONE_API_KEY")
api_secret = os.getenv("ANGEL_ONE_API_SECRET")
username = os.getenv("ANGEL_ONE_USERNAME")
pwd = os.getenv("ANGEL_ONE_PASSWORD")

# Initialize API
smartApi = SmartConnect(api_key)


# Generate TOTP
token = os.getenv("ANGEL_ONE_TOTP_TOKEN")
totp = pyotp.TOTP(token).now()

# Create session
data = smartApi.generateSession(username, pwd, totp)

if data['status']:
    # Session successful
    authToken = data['data']['jwtToken']
    refreshToken = data['data']['refreshToken']
    
    # Get feed token
    feedToken = smartApi.getfeedToken()
    
    # Fetch user profile
    smartApi.getProfile(refreshToken)
    smartApi.generateToken(refreshToken)
    
   


def load_master_data():
    """
    Load existing master data without downloading

    Returns:
        Data in specified format (tuple )
    """
    tuple_file = "master_data.pkl"
    
    # Load based on requested format
    try:
        with open(tuple_file, "rb") as f:
            data = pickle.load(f)
        print(f"Loaded {len(data)} symbols from tuple file")
        return data
      
    except Exception as e:
        print(f"Error loading master data: {e}")
        return []


def find_symbol_token(symbol, exchange=None):
    """
    Find token for a given symbol
    
    Args:
        symbol (str): Symbol to search for
        exchange (str): Optional exchange to filter by
    Returns:
        str: Token if found, None otherwise
    """
    
    data = load_master_data()

    symbol = symbol.upper()
    
    # Tuples are indexed as: 0=symbol, 1=token, 2=exch_seg
    for item in data:
        if item[0] == symbol:
            if exchange is None or item[2] == exchange:
                print(f"Found token for {symbol} on {exchange}: {item[1]}")
                return item[1]
    
    return None

def buy_order(trading_symbol, quantity=1):
    """
    Place a buy order for the given trading symbol.
    
    Args:
        trading_symbol (str): The symbol to buy.
        quantity (int): Number of shares to buy.
    
    Returns:
        str: Order ID if successful, None otherwise.
    """
    # Define order parameters
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": trading_symbol,
        "symboltoken": find_symbol_token(trading_symbol, "NSE"),
        "transactiontype": "BUY",
        "exchange": "NSE",
        "ordertype": "MARKET",
        "producttype": "DELIVERY",
        "duration": "DAY",
        "price": "0",
        "squareoff": "0",
        "stoploss": "0",
        "quantity": str(quantity)
    }
    
    # Place the order
    return smartApi.placeOrder(orderparams)


def sell_order(trading_symbol, quantity=1):
    """
    Place a sell order for the given trading symbol.
    
    Args:
        trading_symbol (str): The symbol to sell.
        quantity (int): Number of shares to sell.
    
    Returns:
        str: Order ID if successful, None otherwise.
    """
    # Define order parameters
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": trading_symbol,
        "symboltoken": find_symbol_token(trading_symbol, "NSE"),
        "transactiontype": "SELL",
        "exchange": "NSE",
        "ordertype": "MARKET",
        "producttype": "DELIVERY",
        "duration": "DAY",
        "price": "0",
        "squareoff": "0",
        "stoploss": "0",
        "quantity": str(quantity)
    }
    
    # Place the order
    return smartApi.placeOrder(orderparams)


def placeOrder(trading_symbol, quantity=1, order_type='BUY'):
    """
    Place an order for the given trading symbol.
    
    Args:
        trading_symbol (str): The symbol to trade.
        quantity (int): Number of shares to trade.
        order_type (str): 'BUY' or 'SELL'.
    
    Returns:
        str: Order ID if successful, None otherwise.
    """
    if order_type.upper() == 'BUY':
        return buy_order(trading_symbol, quantity)
    elif order_type.upper() == 'SELL':
        return sell_order(trading_symbol, quantity)
    else:
        raise ValueError("Invalid order type. Use 'BUY' or 'SELL'.")