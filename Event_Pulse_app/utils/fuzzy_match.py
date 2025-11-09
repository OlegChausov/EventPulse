from Event_Pulse_app.models import EventQuery
from Event_Pulse_app.utils.QueryNormalizer import QueryNormalizer
from rapidfuzz import fuzz

def fuzzy_match(query: EventQuery, raw_event: dict, threshold: int = 80) -> bool:
    query_norm = query.preprocessed_name
    event_norm = QueryNormalizer.preprocess(raw_event["title"], raw_event["event_type"])
    score = fuzz.partial_ratio(query_norm, event_norm)
    return score >= threshold
