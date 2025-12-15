
from datetime import date
import requests
from bs4 import BeautifulSoup
import re


HEADERS = {"User-Agent": "Mozilla/5.0"}


async def get_biletai_lt_concerts(
    start_date: date,
    end_date: date) -> list[dict]:

    start_str = start_date.strftime("%d.%m.%Y")
    end_str = end_date.strftime("%d.%m.%Y")

    # Получаем первую страницу
    url = f"https://www.bilietai.lt/rus/bilietai/visi/category:1002/date:{start_str},{end_str}/order:date,asc/page:1/"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Определяем количество страниц
    last_page = 1
    for a in soup.select("a.pager_page"):
        href = a.get("href", "")
        match = re.search(r"/page:(\d+)/", href)
        if match:
            page_num = int(match.group(1))
            last_page = max(last_page, page_num)

    concerts = []
    seen_concerts = set()

    # Проходим по всем страницам
    for page in range(1, last_page + 1):
        actual_url = f"https://www.bilietai.lt/rus/bilietai/visi/category:1002/date:{start_str},{end_str}/order:date,asc/page:{page}/"
        response = requests.get(actual_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for a_tag in soup.find_all("a", class_="event_short event"):
            title_tag = a_tag.select_one("span.event_short_title")
            title = title_tag.get_text(strip=True) if title_tag else ""
            url = a_tag.get("href", "")

            if title and url and url not in seen_concerts:
                concerts.append({"event_type": "concert", "location": "Vilnius", 'title': title, 'url': url})
                seen_concerts.add(url)

    return concerts


