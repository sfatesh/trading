import os
import requests
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv

# 1. Load variables from the .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 2. Small-budget Watchlist for your ₹1,000 test
STOCKS = ["TATASTEEL.NS", "ITC.NS", "JIOFIN.NS"]

def send_alert(text):
    """Sends a push notification to your phone via Telegram."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Network error sending Telegram notification: {e}")

def get_signal(ticker):
    """Calculates entry/exit boundaries based on a 20-period Moving Average."""
    try:
        # Fetch fresh 15-minute intervals
        df = yf.download(ticker, period="2d", interval="15m", progress=False)
        if df.empty or len(df) < 20:
            return None
            
        df['MA20'] = df['Close'].rolling(window=20).mean()
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # BUY Trigger: Price crosses ABOVE the moving average line
        if latest['Close'] > latest['MA20'] and prev['Close'] <= prev['MA20']:
            return "BUY", latest['Close']
            
        # SELL Trigger: Price drops BELOW the moving average line
        elif latest['Close'] < latest['MA20'] and prev['Close'] >= prev['MA20']:
            return "SELL", latest['Close']
            
    except Exception as e:
        print(f"Error reading market data for {ticker}: {e}")
    return None, None

# --- MAIN AUTOMATION LOOP ---
if __name__ == "__main__":
    print("🚀 AI Trading Agent initialized inside VS Code.")
    print("⚡ Monitoring Watchlist:", STOCKS)
    print("--- Running in the background ---")
    
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # Indian Market Operational Hours (9:15 AM to 3:30 PM IST)
        if "09:15" <= current_time <= "15:30":
            
            # Forced exit warning at 3:00 PM to close intraday trades safely
            if current_time == "15:00":
                send_alert("⏰ *AI SYSTEM CUT-OFF*: The clock shows 3:00 PM. Please close out any active positions to prevent holding trades overnight.")
            
            # Scan your small-budget list
            for stock in STOCKS:
                signal, execution_price = get_signal(stock)
                clean_name = stock.replace(".NS", "")
                
                if signal == "BUY":
                    send_alert(f"🟢 *AI BUY RECOMMENDATION*\nAsset: {clean_name}\nPrice: ₹{execution_price:.2f}\n*Note:* Momentum is surging up. Target small capital deployment.")
                elif signal == "SELL":
                    send_alert(f"🔴 *AI EXIT ALERTS*\nAsset: {clean_name}\nPrice: ₹{execution_price:.2f}\n*Note:* Trend cracked. Sell your position to lock profits or prevent downside.")
            
            # Wait 15 minutes before executing the next technical analysis scan
            time.sleep(900) 
        else:
            # Market is closed (evening/night/weekend). Sleep cleanly to save CPU energy.
            print(f"Market Closed ({current_time}). Waiting for next opening bell...")
            time.sleep(60)