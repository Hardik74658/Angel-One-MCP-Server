# server.py
import os
import sys
from mcp.server.fastmcp import FastMCP
from trade_on_angel_one import placeOrder

# Ensure we're in the correct working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create an MCP server with the exact same name as in settings.json
mcp = FastMCP("AngelOneTradeServer")


# Add a buy stock tool
@mcp.tool()
def buyStockFromAngelOne(stock_symbol: str, quantity: int) -> str:
    """Buy stock from Angel One"""
    try:
        result = placeOrder(stock_symbol, int(quantity), order_type='BUY')
        if not result:
            return f"Failed to buy {quantity} shares of {stock_symbol}. Please check the stock symbol and quantity."
        return f"Bought {quantity} shares of {stock_symbol}. Result: {result}"
    except Exception as e:
        return f"Error buying {quantity} shares of {stock_symbol}: {str(e)}"

# Add a sell stock tool 
@mcp.tool()
def sellStockFromAngelOne(stock_symbol: str, quantity: int) -> str:
    """Sell stock from Angel One"""
    try:
        result = placeOrder(stock_symbol, int(quantity), order_type='SELL')
        if not result:
            return f"Failed to sell {quantity} shares of {stock_symbol}. Please check the stock symbol and quantity."
        return f"Sold {quantity} shares of {stock_symbol}. Result: {result}"
    except Exception as e:
        return f"Error selling {quantity} shares of {stock_symbol}: {str(e)}"

mcp.run(transport="stdio")