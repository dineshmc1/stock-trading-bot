# /stock_bot/config.py

# --- API Credentials ---
OPENAI_API_KEY = "" 
FINNHUB_API_KEY = "" # <-- ADD YOUR FINNHUB KEY

# --- Trading Assets ---
# List of US stock symbols to be analyzed by the bot
TRADING_SYMBOLS = ["AAPL", "NVDA", "MSFT", "GOOGL"]

# --- Generic Charting Configuration ---
# These settings will be applied to each symbol in the list above.
# The orchestrator will dynamically generate titles and file paths.
GENERIC_CHART_SETTINGS = {
    "1D": {
        "resolution": "D",
        "num_points": 200 
    },
    "4H": {
        "resolution": "240",
        "num_points": 150 
    }
}

# --- FIX: Timeframe-Specific Indicator Settings ---
# Settings for the Daily chart, which can include long-term indicators
INDICATOR_SETTINGS_DAILY = {
    "moving_averages": [20, 50, 200],
    "rsi_period": 14,
    "macd_fast": 12, "macd_slow": 26, "macd_signal": 9,
    "bollinger_period": 20, "bollinger_dev": 2
}

# Settings for the Hourly chart, using shorter-term indicators
# The 200 MA is removed to prevent errors with shorter data series.
INDICATOR_SETTINGS_HOURLY = {
    "moving_averages": [20, 50], # Removed 200
    "rsi_period": 14,
    "macd_fast": 12, "macd_slow": 26, "macd_signal": 9,
    "bollinger_period": 20, "bollinger_dev": 2
}

# --- VLM Prompting Strategy ---
# This prompt is general enough for any stock chart.
VLM_PROMPT = """
Analyze the provided stock price chart image for a trading decision. Your analysis must be comprehensive and structured.

**Instructions:**
1.  **Identify Candlestick Patterns:** Look for the most recent and significant candlestick patterns (e.g., Bullish/Bearish Engulfing, Hammer, Doji). Note their location.
2.  **Identify Chart Patterns:** Recognize any classical chart patterns (e.g., Head and Shoulders, Double Top/Bottom, Triangles, Channels).
3.  **Identify Support and Resistance:** Pinpoint key horizontal support and resistance levels and significant trendlines. Assess their strength and provide specific price values.
4.  **Assess Trend:** Determine the primary trend direction (Uptrend, Downtrend, Sideways) based on price action and moving averages.
5.  **Interpret Indicators:** Analyze RSI, MACD, and Bollinger Bands for overbought/oversold conditions, crossovers, and volatility.
6.  **Provide a Final Summary and Sentiment:** Synthesize all points into a concise summary. Conclude with an overall technical sentiment (e.g., "Strong Bullish," "Bearish Correction") and a confidence score.

**Output Format:**
Provide your response *exclusively* in a valid JSON format. Do not include any text before or after the JSON block.

{
  "candlestick_patterns": [{"pattern": "...", "location": "...", "implication": "...", "confidence": "..."}],
  "chart_patterns": [{"pattern": "...", "status": "...", "implication": "...", "confidence": "..."}],
  "support_resistance": {
    "support": [{"level": 180.50, "type": "horizontal", "strength": "strong"}],
    "resistance": [{"level": 195.00, "type": "horizontal", "strength": "moderate"}]
  },
  "trend_analysis": {"direction": "...", "strength": "...", "details": "..."},
  "indicator_analysis": {"rsi": {"value": 0, "status": "..."}, "macd": {"status": "..."}, "bollinger_bands": {"status": "..."}},
  "technical_sentiment": {"sentiment": "...", "confidence": "...", "reasoning": "..."}
}
"""

# --- Risk Management Parameters ---
RISK_SETTINGS = {
    "account_equity": 10000.00,
    "risk_per_trade_percent": 1.0,
    "min_reward_to_risk": 2.0
}

# --- Fundamental Analysis Mock ---
# In a real bot, this would fetch news specific to the symbol being analyzed.
MOCK_FUNDAMENTAL_DATA = {
    "headline": "Broader market sentiment remains cautious ahead of CPI data.",
    "source": "Simulated News API",
    "impact_magnitude": "medium",
    "interpretation": "General market sentiment can influence individual stocks."
}