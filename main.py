# import requests

# TOKEN = "8944044800:AAGlDsL12KQ5ejKcpbnJoJX7YHIYlWiPwts"
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

# print("Checking Telegram servers for your ID...")
# try:
#     response = requests.get(url).json()
#     if response.get("result"):
#         # Extracts your ID automatically from the latest message
#         chat_id = response["result"][-1]["message"]["chat"]["id"]
#         first_name = response["result"][-1]["message"]["chat"]["first_name"]
#         print(f"\n✅ SUCCESS FOUND!")
#         print(f"Your Name: {first_name}")
#         print(f"YOUR ACTUAL CHAT ID: {chat_id}")
#         print(f"\nCopy that number and put it in your .env file!")
#     else:
#         print("\n❌ System connected, but the database is empty.")
#         print("👉 FIX: Open Telegram on your phone, go to @AskZentroBot, type 'Hello' and send it. Then run this script again!")
# except Exception as e:
#     print(f"Network Error: {e}")
import os
import requests
from dotenv import load_dotenv

# 1. Pull the saved credentials from your secure .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_normal_message(text_content):
    """Sends a standard text payload straight to your phone."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Pack the information package
    payload = {
        "chat_id": CHAT_ID,
        "text": text_content,
        "parse_mode": "Markdown"  # Allows bold words or clean spacing
    }
    
    print("⏳ Transmitting message package to Telegram servers...")
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        
        if result.get("ok"):
            print("📱 Success! Check your phone. The message landed safely.")
        else:
            print(f"❌ Telegram rejected the message. Error details: {result.get('description')}")
            
    except Exception as e:
        print(f"💥 Network Error: Could not connect to the internet. Details: {e}")

if __name__ == "__main__":
    # Define what you want your normal message to say
    message_to_send = (
        "🚀 *Zentro Agent: Connection Verified!*\n\n"
        "Your Python environment, VS Code project workspace, and secure `.env` "
        "variables are completely linked to this chat window. Ready for monitoring!"
    )
    
    send_normal_message(message_to_send)