import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- CONFIG ---
WILAYA_NAME = "تلمسان"
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
# IMPORTANT: Replace this with the URL from your new Selenium Railway service
SELENIUM_URL = os.getenv("SELENIUM_URL", "http://your-selenium-service-url:4444/wd/hub")

def send_alert(message):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

# --- CONNECTING TO REMOTE BROWSER ---
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
# High-quality user agent for 2026 platform compatibility
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

print(f"--- Monitoring Tlemcen via Remote Selenium (2026) ---")

def run_monitor():
    # We connect to the external Selenium container here
    driver = webdriver.Remote(command_executor=SELENIUM_URL, options=chrome_options)
    
    try:
        while True:
            try:
                driver.get("https://adhahi.dz/register")
                time.sleep(10) # Wait for Algerian server to respond
                
                content = driver.page_source
                if WILAYA_NAME in content:
                    if "غير متوفر حاليًا" not in content:
                        send_alert(f"🚨 TLEMCEN IS OPEN! GO NOW: https://adhahi.dz/register")
                        time.sleep(1800) # Stop alerts for 30 mins after success
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] Tlemcen: Still Unavailable.")
                else:
                    print("Could not find Tlemcen in the list.")
            
            except Exception as e:
                print(f"Check failed: {e}")
                time.sleep(30)
            
            time.sleep(60) # Wait 1 minute
    finally:
        driver.quit()

if __name__ == "__main__":
    run_monitor()
