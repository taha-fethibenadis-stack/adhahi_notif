import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIG ---
WILAYA_NAME = "برج باجي مختار"
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = 60 

def send_alert(message):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, data={'chat_id': CHAT_ID, 'text': message}, timeout=10)
        except Exception as e:
            print(f"Telegram failed: {e}")

# --- BROWSER CONFIG ---
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
# Set a real user agent so the site doesn't block the "headless" browser
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

print(f"--- Monitoring Tlemcen on adhahi.dz (2026) ---")

try:
    # This automatically downloads the correct driver for the Chrome version we installed
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    while True:
        try:
            driver.get("https://adhahi.dz/register")
            time.sleep(7) # Increased wait time for slow Algerian servers
            
            content = driver.page_source
            
            # Check for Tlemcen and the absence of 'Unavailable'
            if WILAYA_NAME in content:
                if "غير متوفر حاليًا" not in content:
                    print("!!! TLEMCEN IS AVAILABLE !!!")
                    send_alert(f"🚨 TLEMCEN IS OPEN! GO NOW: https://adhahi.dz/register")
                    # Stop alert spam for 10 minutes after success
                    time.sleep(600) 
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] Tlemcen: Still Unavailable.")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Tlemcen not found in list.")
                
        except Exception as e:
            print(f"Error during check: {e}")
            time.sleep(10) # Short wait before retry on error
        
        time.sleep(CHECK_INTERVAL)

finally:
    if 'driver' in locals():
        driver.quit()
