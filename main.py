# /stock_bot/main.py

import logging
from orchestrator import CentralOrchestrationModule
from utils import setup_logging
from config import TRADING_SYMBOLS

def main():
    """
    Main function to initialize and run the trading bot's analysis cycle
    for a list of predefined stocks.
    """
    setup_logging()
    
    try:
        logging.info("Starting Multi-Stock Trading Bot...")
        bot_orchestrator = CentralOrchestrationModule()
        
        # Loop through each symbol and run the full analysis
        for symbol in TRADING_SYMBOLS:
            bot_orchestrator.run_analysis_cycle(symbol)
            
        logging.info("Multi-Stock Trading Bot run finished for all symbols.")
        
    except Exception as e:
        logging.critical(f"A critical error occurred in the main execution block: {e}", exc_info=True)

if __name__ == "__main__":
    main()