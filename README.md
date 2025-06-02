# Angel One Trading MCP Server

<div align="center">
  
![Angel One Logo](https://upload.wikimedia.org/wikipedia/commons/6/6d/Angel_One_Logo.svg)

**Automated Stock Trading with VS Code and AI Assistants Like Claude**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green.svg)](https://microsoft.github.io/model-context-protocol/)
[![Angel One](https://img.shields.io/badge/Angel%20One-Trading%20API-orange.svg)](https://smartapi.angelone.in/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

</div>

## 📖 Overview

Angel One MCP Server is a powerful integration that allows AI assistants in VS Code (using the Model Context Protocol) to execute stock trades on the Angel One trading platform directly. Place buy and sell orders using natural language, with your AI assistant handling the technical details.

## 🚀 Features

- **AI-Powered Trading**: Execute stock trades by simply asking your AI assistant
- **Seamless Integration**: Works with any MCP-compatible assistant (like GitHub Copilot)
- **Real-Time Order Execution**: Place market orders on Angel One instantly
- **Secure Authentication**: Uses TOTP-based secure authentication
- **Modern Python Environment**: Supports UV package manager for faster and more reliable dependency management

## 🔧 Setup & Installation

### Prerequisites

- Angel One trading account
- Python 3.10+
- VS Code with an MCP-compatible AI assistant

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/angel-one-mcp.git
   cd angel-one-mcp
   ```

2. Install dependencies using UV (recommended):
   ```bash
   # Install UV if you don't have it yet
   pip install uv
   
   # Create and activate a virtual environment with UV
   uv venv
   
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   # source .venv/bin/activate
   
   # Install dependencies with UV
   uv pip install -r requirements.txt
   ```

   Alternatively, use traditional pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Update your API credentials in `.env` file:
   ```
   ANGEL_ONE_API_KEY=YOUR_API_KEY
   ANGEL_ONE_API_SECRET=YOUR_API_SECRET
   ANGEL_ONE_USERNAME=YOUR_USERNAME
   ANGEL_ONE_PASSWORD=YOUR_PASSWORD
   ANGEL_ONE_TOTP_TOKEN=YOUR_TOTP_SECRET
   ```

4. Configure MCP.json File settings:
   ```json
   "mcp": {
       "servers": {
           "AngelOneTradeServer": {
               "type": "stdio",
               "command": "uv",
               "args": [
                   "--directory",
                   "C:\\path\\to\\angel-one-mcp",
                   "run",
                   "server.py"
               ]
           }
       }
   }
   ```

   Alternatively, if not using UV:
   ```json
   "mcp": {
       "servers": {
           "AngelOneTradeServer": {
               "type": "stdio",
               "command": "python",
               "args": [
                   "C:\\path\\to\\angel-one-mcp\\server.py"
               ]
           }
       }
   }
   ```

## 💼 Usage

Once configured, you can use natural language to place trades through your AI assistant:

- **Buy stocks**: "Buy 10 shares of RELIANCE-EQ"
- **Sell stocks**: "Sell 5 shares of TCS-EQ"

> **Note**: Always append "-EQ" to equity stock symbols (e.g., "RELIANCE-EQ", "TCS-EQ") when placing orders.

## 🛠️ How It Works

### Architecture

The system consists of three main components:

1. **MCP Server (`server.py`)**: Handles communication between VS Code and the trading functions
2. **Trading Logic (`trade_on_angel_one.py`)**: Implements the Angel One API integration
3. **Master Data**: Stock symbols and token mapping for the exchange

### Trading Flow

1. User issues a natural language command to the AI assistant
2. Assistant calls the appropriate MCP function (`buyStockFromAngelOne` or `sellStockFromAngelOne`)
3. The function invokes the Angel One API to place the order
4. Order confirmation is returned to the assistant and displayed to the user

## 📋 Available Functions

### Buy Stock
```python
buyStockFromAngelOne(stock_symbol: str, quantity: int) -> str
```
Places a buy order for the specified stock and quantity.

### Sell Stock
```python
sellStockFromAngelOne(stock_symbol: str, quantity: int) -> str
```
Places a sell order for the specified stock and quantity.

## 🔄 Master Data Management

The system uses pre-loaded master data to map stock symbols to their exchange tokens:

- `master_data.pkl`: Contains the mapping between stock symbols and their tokens
- `load_master_data()`: Loads the mapping from disk
- `find_symbol_token()`: Locates the appropriate token for a given stock symbol

## ⚠️ Security and Trading Considerations

- API credentials should be stored in a `.env` file which is excluded from version control
- TOTP authentication provides an additional security layer
- Never share your API credentials or TOTP secret
- **Important Note**: The Angel One API has limitations on buying certain equity stocks due to exchange restrictions. Some equity orders may be rejected despite using the correct symbol format with "-EQ" suffix. This is a limitation of the Angel One API and not of this integration

## 🐞 Troubleshooting

### Common Issues

1. **Symbol Not Found Error**: 
   - Ensure you're appending "-EQ" for equity stocks
   - Check if the stock is available in the master data by examining `master_data.json` or `master_data.pkl`

2. **Order Rejected by Exchange**:
   - Some equity stocks may be restricted by Angel One/exchange regulations
   - Try with different stock or consult Angel One documentation for specific stock restrictions

3. **Authentication Failure**:
   - Make sure your TOTP token is current and correctly configured
   - Check if your Angel One credentials are valid and account is active

### Handling Environment Issues

If you encounter issues with UV or Python environment:

```bash
# Clean up and recreate the environment
rm -rf .venv
uv venv
uv pip install -r requirements.txt
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 🙏 Acknowledgements

- [Angel One SmartAPI](https://smartapi.angelone.in/) for providing the trading API
- [Microsoft Model Context Protocol](https://microsoft.github.io/model-context-protocol/) for enabling AI assistant integrations
- [UV](https://github.com/astral-sh/uv) for modern Python package management