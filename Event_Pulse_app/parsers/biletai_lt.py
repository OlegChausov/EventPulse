import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from datetime import datetime, timedelta
import re

awaited_list = ['Монеточка', 'Машина времени', 'Валерий Меладзе']

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 📅 Даты
start_date = datetime.today().date()
end_date = start_date + timedelta(days=180)

start_date = datetime.today().date()
end_date = start_date + timedelta(days=180)
start_str = start_date.strftime("%d.%m.%Y")
end_str = end_date.strftime("%d.%m.%Y")

# 🔗 URL первой страницы
url = f"https://www.bilietai.lt/rus/bilietai/visi/category:1002/date:{start_str},{end_str}/order:date,asc/page:1/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 🔍 Найти все ссылки с классом pager_page
last_page = 1
for a in soup.select("a.pager_page"):
    href = a.get("href", "")
    match = re.search(r"/page:(\d+)/", href)
    if match:
        page_num = int(match.group(1))
        last_page = max(last_page, page_num)

concerts = []
seen_concerts = []

for page in range(1, last_page + 1):
    # 📥 Получить HTML
    Actual_url = f"https://www.bilietai.lt/rus/bilietai/visi/category:1002/date:{start_str},{end_str}/order:date,asc/page:{page}/"
    print(Actual_url)
    response = requests.get(Actual_url, headers=HEADERS)
    response.raise_for_status()  # Чтобы не продолжать парсить страницу, если она не загрузилась.
    soup = BeautifulSoup(response.text, "html.parser")

    for a_tag in soup.find_all("a", class_="event_short event"):
        title_tag = a_tag.select_one("span.event_short_title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        url = a_tag.get("href", "")

        if title and url and url not in seen_concerts:
            concerts.append({'title' : title, 'url': url})
            seen_concerts.append(url)

for concert in concerts:
    print(concert)





