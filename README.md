# Multi-Stock Trading Bot

A modular Python bot that analyzes multiple US stocks (AAPL, NVDA, MSFT, GOOGL) using technical charting, OpenAI's Vision Language Model (VLM) for chart analysis, and mock fundamental news. The bot generates trading signals, applies risk management, and simulates trade execution.

## Features
- **Automated Chart Generation**: Fetches historical data and generates candlestick charts with technical indicators (Moving Averages, RSI, MACD, Bollinger Bands).
- **Vision-Based Chart Analysis**: Uses OpenAI's VLM to analyze chart images and extract structured technical insights.
- **Mock Fundamental Analysis**: Simulates news-based sentiment for each stock.
- **Risk Management**: Calculates position size, stop loss, and take profit based on account equity and risk parameters.
- **Simulated Trade Execution**: Logs trade signals and parameters for backtesting or demonstration.
- **Extensible & Modular**: Easily add new symbols, indicators, or real broker integration.

## Requirements
- Python 3.8+
- The following Python packages (see `requirements.txt`):
  - openai
  - pandas
  - numpy
  - matplotlib
  - mplfinance
  - requests
  - Pillow
  - yfinance

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Setup
1. **Clone the repository** and navigate to the project directory.
2. **Configure API Keys**:
   - Open `config.py` and add your OpenAI API key to `OPENAI_API_KEY`.
   - (Optional) Add your Finnhub API key to `FINNHUB_API_KEY` if you plan to extend fundamental analysis.
3. **(Optional) Adjust Trading Symbols**:
   - Edit `TRADING_SYMBOLS` in `config.py` to analyze different stocks.
4. **Review Risk Settings**:
   - Adjust `RISK_SETTINGS` in `config.py` to match your risk profile.

## Usage
Run the bot from the command line:
```bash
python main.py
```
- The bot will analyze each symbol in `TRADING_SYMBOLS`, generate charts, run VLM analysis, apply risk management, and simulate trades.
- Logs and results are saved to `trading_bot.log` and chart images are saved as PNG files in the project directory.

## Configuration
- **API Keys**: Set in `config.py` (`OPENAI_API_KEY`, `FINNHUB_API_KEY`).
- **Symbols**: Edit `TRADING_SYMBOLS` in `config.py`.
- **Risk Management**: Adjust `RISK_SETTINGS` for account equity, risk per trade, and reward/risk ratio.
- **Chart/Indicator Settings**: Modify `GENERIC_CHART_SETTINGS`, `INDICATOR_SETTINGS_DAILY`, and `INDICATOR_SETTINGS_HOURLY` in `config.py`.

## File Structure
- `main.py` — Entry point; runs the analysis cycle for all symbols.
- `orchestrator.py` — Central logic for coordinating charting, analysis, and trade simulation.
- `chart_generator.py` — Fetches data and generates charts with indicators.
- `vlm_analyzer.py` — Sends chart images to OpenAI VLM and parses the response.
- `news_analyzer.py` — Mock fundamental news analysis.
- `risk_manager.py` — Calculates position size, stop loss, and take profit.
- `trade_executor.py` — Simulates trade execution and logs results.
- `config.py` — All configuration (API keys, symbols, risk, indicator settings).
- `requirements.txt` — Python dependencies.
- `trading_bot.log` — Log file with all analysis and trade actions.

## Notes
- **API Keys**: The bot will not run VLM analysis without a valid OpenAI API key.
- **Fundamental Analysis**: Currently uses mock data; extend `news_analyzer.py` for real news APIs.
- **Broker Integration**: Trade execution is simulated; integrate with a real broker for live trading.
- **Extensibility**: Add new symbols, indicators, or analysis modules as needed.

---

*For research, educational, and backtesting purposes only. Not financial advice.* 