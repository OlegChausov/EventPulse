from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument("--headless")  # Без окна браузера
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

start_date = datetime.today().date()
end_date = start_date + timedelta(days=180)

driver = webdriver.Chrome(options=options)

base_url = "https://www.eventim.pl/city/warszawa-243/koncerty-62/"
params = f"?sort=DateAsc&dateFrom={start_date}&dateTo={end_date}"

time.sleep(5)  # Дать странице прогрузиться

for page in range(1, 16):
    url = f"{base_url}{params}&page={page}"
    print(f"🔎 Страница {page}: {url}")
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    print(html)
    soup = BeautifulSoup(html, "html.parser")
    no_results = soup.select_one("div.search-result-content.no-results")
    if no_results:
        print('результаты закончились')
        break









