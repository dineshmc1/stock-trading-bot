# /stock_bot/risk_manager.py
import logging
from config import RISK_SETTINGS

class RiskManager:
    # ... (init is the same) ...
    def __init__(self):
        self.settings = RISK_SETTINGS
        logging.info("RiskManager initialized.")

    def calculate_trade_parameters(self, signal, latest_price, technical_analysis):
        try:
            entry_price = latest_price
            stop_loss_price = None

            if signal == "BUY":
                supports = sorted([s['level'] for s in technical_analysis['support_resistance']['support'] if s['level'] < entry_price], reverse=True)
                if not supports:
                    logging.warning(f"BUY signal but no valid support level found below current price {entry_price}. Cannot set SL.")
                    return None
                stop_loss_price = supports[0]
            elif signal == "SELL":
                resistances = sorted([r['level'] for r in technical_analysis['support_resistance']['resistance'] if r['level'] > entry_price])
                if not resistances:
                    logging.warning(f"SELL signal but no valid resistance level found above current price {entry_price}. Cannot set SL.")
                    return None
                stop_loss_price = resistances[0]
            else:
                return None
            
            risk_per_share = abs(entry_price - stop_loss_price)
            if risk_per_share <= 0:
                logging.warning("Invalid risk distance (<= 0) calculated. Cannot place trade.")
                return None

            if signal == "BUY":
                take_profit_price = entry_price + (risk_per_share * self.settings['min_reward_to_risk'])
            else:
                take_profit_price = entry_price - (risk_per_share * self.settings['min_reward_to_risk'])

            risk_amount_per_trade = self.settings['account_equity'] * (self.settings['risk_per_trade_percent'] / 100)
            
            # --- STOCK-SPECIFIC CALCULATION ---
            num_shares_to_trade = risk_amount_per_trade / risk_per_share
            
            trade_params = {
                "signal": signal,
                "entry_price": round(entry_price, 2),
                "stop_loss": round(stop_loss_price, 2),
                "take_profit": round(take_profit_price, 2),
                "position_size_shares": round(num_shares_to_trade, 2), # Now in shares
                "risk_per_trade_usd": round(risk_amount_per_trade, 2)
            }
            logging.info(f"Calculated trade parameters: {trade_params}")
            return trade_params
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Could not calculate trade parameters. VLM output might be malformed or missing S/R levels. Error: {e}", exc_info=True)
            return None