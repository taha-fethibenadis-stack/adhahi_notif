import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- SETTINGS ---
WILAYA_NAME = "تلمسان"
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = 60 

def send_alert(message):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={'chat_id': CHAT_ID, 'text': message})
    else:
        print("Telegram settings missing!")

# --- BROWSER CONFIG ---
chrome_options = Options()
chrome_options.add_argument("--headless=new") 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

print(f"Monitoring Tlemcen on adhahi.dz 2026...")

try:
    # Setup Service using webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    while True:
        try:
            driver.get("https://adhahi.dz/register")
            time.sleep(5)
            
            content = driver.page_source
            if WILAYA_NAME in content and "غير متوفر حاليًا" not in content:
                print("!!! OPEN !!!")
                send_alert(f"🚨 TLEMCEN IS OPEN! Register now: https://adhahi.dz/register")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Still unavailable in Tlemcen.")
        except Exception as e:
            print(f"Error checking page: {e}")
        
        time.sleep(CHECK_INTERVAL)
finally:
    if 'driver' in locals():
        driver.quit()
