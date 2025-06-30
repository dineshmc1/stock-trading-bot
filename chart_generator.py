# /stock_bot/chart_generator.py

import pandas as pd
import mplfinance as mpf
import logging
import yfinance as yf
# We no longer import INDICATOR_SETTINGS from config here

def fetch_market_data(symbol, resolution, num_points):
    # ... (This function remains exactly the same as the previous version) ...
    logging.info(f"Fetching {num_points} data points for {symbol} with {resolution} resolution from Yahoo Finance...")
    try:
        interval = '1d'
        if resolution == '240':
            interval = '1h'
            logging.warning(f"yfinance does not support '4h' interval. Using '1h' as the closest alternative for {symbol}.")
        period_to_fetch = f"{int(num_points * 1.5)}d"
        if interval == '1h':
            period_to_fetch = "720d"
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period_to_fetch, interval=interval)
        if df.empty:
            logging.error(f"yfinance returned no data for {symbol}.")
            return None
        df.index = df.index.tz_localize(None)
        df = df.tail(num_points)
        logging.info(f"Successfully fetched {len(df)} data points for {symbol}.")
        return df
    except Exception as e:
        logging.error(f"An unexpected error occurred during data fetching for {symbol} with yfinance: {e}", exc_info=True)
        return None

# --- FIX: This function now accepts indicator settings as an argument ---
def _calculate_indicators(df, indicator_settings):
    """Calculates and adds technical indicators to the dataframe based on provided settings."""
    for ma in indicator_settings['moving_averages']:
        df[f'MA_{ma}'] = df['Close'].rolling(window=ma).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=indicator_settings['rsi_period']).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=indicator_settings['rsi_period']).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    exp1 = df['Close'].ewm(span=indicator_settings['macd_fast'], adjust=False).mean()
    exp2 = df['Close'].ewm(span=indicator_settings['macd_slow'], adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['MACD_Signal'] = df['MACD'].ewm(span=indicator_settings['macd_signal'], adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    ma_bb = df['Close'].rolling(window=indicator_settings['bollinger_period']).mean()
    std_dev = df['Close'].rolling(window=indicator_settings['bollinger_period']).std()
    df['BB_Upper'] = ma_bb + (std_dev * indicator_settings['bollinger_dev'])
    df['BB_Lower'] = ma_bb - (std_dev * indicator_settings['bollinger_dev'])
    return df

# --- FIX: This function now accepts indicator settings as an argument ---
def generate_chart_image(symbol, resolution, num_points, title, file_path, indicator_settings):
    """
    Fetches real data from yfinance, generates, and saves a chart image.
    """
    try:
        logging.info(f"Creating chart for {symbol} ({resolution} resolution)...")
        df = fetch_market_data(symbol, resolution, num_points)
        if df is None or df.empty:
            logging.error(f"No data fetched for {symbol}, cannot generate chart.")
            return None, None
        
        df_with_indicators = _calculate_indicators(df.copy(), indicator_settings).dropna()
        
        # Add a check to ensure the dataframe is not empty AFTER dropping NaNs
        if df_with_indicators.empty:
            logging.error(f"DataFrame for {symbol} became empty after indicator calculation. Not enough data points for the given indicators.")
            return None, None

        ap = [
            mpf.make_addplot(df_with_indicators[[f'MA_{ma}' for ma in indicator_settings['moving_averages']]]),
            mpf.make_addplot(df_with_indicators[['BB_Upper', 'BB_Lower']], color='grey', alpha=0.3),
            mpf.make_addplot(df_with_indicators[['MACD', 'MACD_Signal']], panel=2, ylabel='MACD'),
            mpf.make_addplot(df_with_indicators['MACD_Hist'], type='bar', panel=2, color='dimgray', alpha=0.7),
            mpf.make_addplot(df_with_indicators['RSI'], panel=3, ylabel='RSI', y_on_right=False),
        ]
        mpf.plot(df_with_indicators, type='candle', style='yahoo', title=title, ylabel='Price (USD)',
                 volume=True, volume_panel=1, panel_ratios=(6, 2, 2, 2), addplot=ap,
                 figsize=(15, 10), savefig=dict(fname=file_path, dpi=100, pad_inches=0.25))
        logging.info(f"Chart for {symbol} saved successfully to {file_path}")
        return file_path, df
        
    except Exception as e:
        logging.error(f"Failed to generate chart image for {symbol}: {e}", exc_info=True)
        return None, None