import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

awaited_list = ['TheatreHD: Венская опера. Времена года', 'Заклятие 4: Последний обряд', 'Каруза',
                'Оперный фестиваль в Мачерате: Аида']

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 📅 Даты
start_date = datetime.today().date()
end_date = start_date + timedelta(days=365)

# 🔗 Сформировать URL
URL = f"https://afisha.me/day/film/{start_date}/{end_date}/"

# 📥 Получить HTML
response = requests.get(URL, headers=HEADERS)
response.raise_for_status()  # Чтобы не продолжать парсить страницу, если она не загрузилась.
soup = BeautifulSoup(response.text, "html.parser")

# 🎯 Найти только нужные ссылки
film_links = []
seen_urls = set()

for a_tag in soup.find_all("a", class_="name"):
    href = a_tag.get("href", "")
    if href.startswith("https://afisha.me/film/") and href not in seen_urls:
        title = a_tag.get_text(strip=True)
        film_links.append({
            "title": title,
            "url": href
        })
        seen_urls.add(href)

# 📤 Вывод
for film in film_links:
    if film['title'] in awaited_list:
        print(film)


