import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# --- CONFIGURATION (Uses Railway Environment Variables) ---
# Set these in your Railway Dashboard -> Variables
WILAYA_NAME = "تلمسان"  # Tlemcen
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = 60  # Check every 60 seconds to avoid being blocked

def send_telegram_msg(message):
    if not TOKEN or not CHAT_ID:
        print("Telegram credentials missing!")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram failed: {e}")

# --- SELENIUM SETUP ---
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # 2026 headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

print(f"Monitoring Tlemcen on adhahi.dz 2026...")

try:
    while True:
        try:
            driver.get("https://adhahi.dz/register")
            time.sleep(5)  # Let dynamic list load
            
            page_source = driver.page_source
            status_text = "غير متوفر حاليًا"  # "Currently unavailable"

            # Logic: If Tlemcen is listed and DOES NOT have 'unavailable' next to it
            if WILAYA_NAME in page_source:
                if status_text not in page_source:
                    msg = f"🚨 TLEMCEN IS OPEN! Go to adhahi.dz NOW!"
                    print(msg)
                    send_telegram_msg(msg)
                    # Optional: Add time.sleep(1800) here to stop alerts for 30 mins
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] Tlemcen: Still Unavailable.")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Tlemcen not found in list yet.")

        except Exception as e:
            print(f"Loop error: {e}")
            
        time.sleep(CHECK_INTERVAL)
finally:
    driver.quit()
