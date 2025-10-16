from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from playwright.sync_api import sync_playwright

start_date = datetime.today().date()
end_date = start_date + timedelta(days=180)

base_url = "https://www.eventim.pl/search/?affiliate=PLE"
params = "&category=concert&city=Warszawa"



base_url = "https://www.eventim.pl/city/warszawa-243/koncerty-62/"
params = f"?sort=DateAsc&dateFrom={start_date}&dateTo={end_date}"

url = f"{base_url}{params}&page=7"


from playwright.sync_api import sync_playwright
import time
import os

def get_dom(url: str, headless: bool = True, save_html: bool = True, page_id: str = "page") -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-http2",
                "--disable-features=NetworkService",
                "--start-maximized"
            ]
        )
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )

        try:
            page.goto(url, timeout=30000)
            page.wait_for_load_state("networkidle")
            html = page.content()

            if save_html:
                os.makedirs("html_dumps", exist_ok=True)
                with open(f"html_dumps/{page_id}.html", "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"✅ HTML сохранён: html_dumps/{page_id}.html")

            return html

        except Exception as e:
            print(f"🛑 Ошибка при загрузке {url}: {e}")
            page.screenshot(path=f"html_dumps/{page_id}_error.png")
            print(f"📸 Скриншот сохранён: html_dumps/{page_id}_error.png")
            return ""

        finally:
            browser.close()

html = get_dom(url)

print("no-results" in html)








