# /stock_bot/orchestrator.py

import logging
# --- FIX: Import the new settings dictionaries ---
from config import GENERIC_CHART_SETTINGS, INDICATOR_SETTINGS_DAILY, INDICATOR_SETTINGS_HOURLY
from chart_generator import generate_chart_image
# ... other imports are the same ...
from vlm_analyzer import VLMTechnicalAnalyzer
from news_analyzer import FundamentalAnalyzer
from risk_manager import RiskManager
from trade_executor import TradeExecutor


class CentralOrchestrationModule:
    # ... (init and _get_final_signal methods are the same) ...
    def __init__(self):
        logging.info("Initializing Central Orchestration Module...")
        self.chart_gen = generate_chart_image
        self.vlm_analyzer = VLMTechnicalAnalyzer()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.risk_manager = RiskManager()
        self.trade_executor = TradeExecutor()
        logging.info("All agents initialized.")

    def _get_final_signal(self, symbol, daily_analysis, hourly_analysis, fundamental_analysis):
        try:
            daily_sentiment = daily_analysis['technical_sentiment']['sentiment'].lower()
            hourly_sentiment = hourly_analysis['technical_sentiment']['sentiment'].lower()
            hourly_reasoning = hourly_analysis['technical_sentiment']['reasoning']

            logging.info(f"[{symbol}] Daily Bias: '{daily_sentiment}'. 4H Signal: '{hourly_sentiment}'.")

            if 'bullish' in daily_sentiment and 'bullish' in hourly_sentiment:
                return "BUY", f"Daily trend is bullish. 4H chart shows bullish confirmation. Reason: {hourly_reasoning}"
            elif 'bearish' in daily_sentiment and 'bearish' in hourly_sentiment:
                return "SELL", f"Daily trend is bearish. 4H chart shows bearish confirmation. Reason: {hourly_reasoning}"
            
            return "HOLD", "No clear alignment between Daily bias and 4H entry signal."
        
        except (KeyError, TypeError) as e:
            logging.error(f"[{symbol}] Error in decision logic due to missing analysis data: {e}")
            return "HOLD", "Could not determine signal due to incomplete analysis."

    def run_analysis_cycle(self, symbol):
        """
        Executes one full analysis cycle for a single stock symbol.
        """
        logging.info(f"========== STARTING ANALYSIS CYCLE FOR: {symbol} ==========")
        
        # --- FIX: Pass the correct indicator settings to the chart generator ---
        chart_1d_settings = {
            "symbol": symbol,
            "title": f"{symbol} Daily Chart",
            "file_path": f"{symbol}_1D_chart.png",
            "indicator_settings": INDICATOR_SETTINGS_DAILY, # Pass daily settings
            **GENERIC_CHART_SETTINGS["1D"]
        }
        chart_4h_settings = {
            "symbol": symbol,
            "title": f"{symbol} 4-Hour Chart",
            "file_path": f"{symbol}_4H_chart.png",
            "indicator_settings": INDICATOR_SETTINGS_HOURLY, # Pass hourly settings
            **GENERIC_CHART_SETTINGS["4H"]
        }

        # 2. Generate Chart Images and get data
        chart_1d_path, df_1d = self.chart_gen(**chart_1d_settings)
        chart_4h_path, df_4h = self.chart_gen(**chart_4h_settings)

        if not chart_1d_path or not chart_4h_path or df_4h is None:
            logging.error(f"[{symbol}] Failed to generate charts or fetch data. Aborting cycle for this symbol.")
            return

        # ... (The rest of the method is the same) ...
        analysis_1d = self.vlm_analyzer.analyze_chart(chart_1d_path)
        analysis_4h = self.vlm_analyzer.analyze_chart(chart_4h_path)
        
        if not analysis_1d or not analysis_4h:
            logging.error(f"[{symbol}] Failed to get VLM analysis. Aborting cycle for this symbol.")
            return

        fundamental_data = self.fundamental_analyzer.get_analysis()
        final_signal, reasoning = self._get_final_signal(symbol, analysis_1d, analysis_4h, fundamental_data)
        logging.info(f"[{symbol}] FINAL DECISION: {final_signal}. REASON: {reasoning}")

        if final_signal in ["BUY", "SELL"]:
            latest_close_price = df_4h['Close'].iloc[-1]
            logging.info(f"[{symbol}] Latest 4H close price for risk calculation: {latest_close_price:.2f}")
            trade_params = self.risk_manager.calculate_trade_parameters(final_signal, latest_close_price, analysis_4h)
            if trade_params:
                trade_params['symbol'] = symbol
                self.trade_executor.execute_trade(trade_params)
            else:
                logging.warning(f"[{symbol}] Trade signal generated but risk parameters could not be calculated. No trade placed.")
        logging.info(f"========== ANALYSIS CYCLE FOR {symbol} COMPLETE ==========\n")