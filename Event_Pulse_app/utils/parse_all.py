import asyncio
from datetime import date
from Event_Pulse_app.parsers.afisha_me import get_afisha_me_films
from Event_Pulse_app.parsers.biletai_lt import get_biletai_lt_concerts
from Event_Pulse_app.parsers.concertful import get_concertful_pl
from Event_Pulse_app.utils.time_functions import default_start_date, default_end_date



async def run_all_parsers() -> list[dict]:
    start_date: date = default_start_date()
    end_date: date = default_end_date(start_date)

    parsers = {
        "afisha.me": lambda: get_afisha_me_films(start_date, end_date),
        "biletai.lt": lambda: get_biletai_lt_concerts(start_date, end_date),
        "concertful.pl": lambda: get_concertful_pl(start_date)
    }

    tasks = [asyncio.create_task(func()) for func in parsers.values()]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_events = []
    for name, result in zip(parsers.keys(), results):
        if isinstance(result, Exception):
            print(f"❌ Парсер '{name}' упал: {type(result).__name__}: {result}")
            continue
        print(f"✅ Парсер '{name}' вернул {len(result)} событий")
        all_events.extend(result)

    return all_events
