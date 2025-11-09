from Event_Pulse_app.config import PARSERS
import asyncio

# PARSERS = [
#     {"name": "afisha_me", "func": get_afisha_me_films, "type": "film", "region": "BY"},
#     {"name": "biletail_lt", "func": get_biletai_lt_concerts, "type": "concert", "region": "LT"},
#     {"name": "concertful", "func": get_concertful_pl, "type": "concert", "region": "PL"},
# ]

async def global_parsing() -> list[dict]:
    results = await asyncio.gather(*[parser["func"]() for parser in PARSERS])
    all_events = [event for sublist in results for event in sublist]
    return all_events







# matched_events = []
#
# existing_urls = {event.url for event in await db.execute(select(Event.url))}
#
# for raw_event in raw_events:
#     for query in event_queries:
#         if fuzzy_match(query, raw_event):
#             if raw_event["url"] not in existing_urls:
#                 matched_events.append((query, raw_event))
#                 existing_urls.add(raw_event["url"])  # чтобы не добавлять повторно
#             break  # достаточно одного совпадения
