from fastapi import APIRouter, Depends

from Event_Pulse_app.parsers.afisha_me import get_afisha_me_films
from Event_Pulse_app.parsers.biletai_lt import get_biletai_lt_concerts
from Event_Pulse_app.parsers.concertful import get_concertful_pl
from Event_Pulse_app.utils.parse_all import run_all_parsers

router = APIRouter()

# @router.get("/test-parse-all")
# async def test_afisha(events=Depends(get_afisha_me_films)):
#     return events
#
# @router.get("/test-parse-all")
# async def test_biletai(events=Depends(get_biletai_lt_concerts)):
#     return events
#
# @router.get("/test-parse-all")
# async def test_concertful(events=Depends(get_concertful_pl)):
#     return events



@router.get("/test-parse-all")
async def test_all(events=Depends(run_all_parsers)):

    return events
