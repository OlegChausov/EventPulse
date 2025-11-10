import asyncio
from datetime import date
from Event_Pulse_app.parsers.afisha_me import get_afisha_me_films, default_start_date, default_end_date
from Event_Pulse_app.parsers.biletai_lt import get_biletai_lt_concerts
from Event_Pulse_app.parsers.concertful import get_concertful_pl

async def run_all_parsers() -> list[dict]:
    # Используем централизованные функции для дат
    start_date: date = default_start_date()
    end_date: date = default_end_date(start_date)

    # Переопределяем парсеры с фиксированными параметрами
    afisha = get_afisha_me_films(start_date=start_date, end_date=end_date)
    biletai = get_biletai_lt_concerts(start_date=start_date, end_date=end_date)
    concertful = get_concertful_pl(start_date=start_date)

    # Запускаем все асинхронно
    results = await asyncio.gather(afisha, biletai, concertful, return_exceptions=True)

    # Объединяем и фильтруем ошибки
    all_events = []
    for res in results:
        if isinstance(res, Exception):
            # Можно логировать ошибку
            continue
        all_events.extend(res)

    return all_events
