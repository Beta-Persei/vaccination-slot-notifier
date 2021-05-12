from datetime import datetime

import requests
from django.conf import settings

from sniffer.utils import parse_centers

headers = {
    "authority": "cdn-api.co-vin.in",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
}


def get_centers_by_pincode(pincode):
    query_params = {
        "pincode": pincode,
        "date": datetime.now().strftime("%d-%m-%Y"),
    }

    res = requests.get(
        settings.PINCODE_SLOT_ENDPOINT, params=query_params, headers=headers
    )

    if res.status_code == 200:
        return parse_centers(res.json()["centers"])


def get_centers_by_district_id(district_id):
    query_params = {
        "district_id": district_id,
        "date": datetime.now().strftime("%d-%m-%Y"),
    }
    res = requests.get(
        settings.DISTRICT_SLOT_ENDPOINT, params=query_params, headers=headers
    )

    if res.status_code == 200:
        return parse_centers(res.json()["centers"])


def get_states():
    res = requests.get(settings.STATES_ENDPOINT)
    return parse_centers(res.json()["states"])


def get_districts(state_id):
    res = requests.get(settings.DISTRICTS_ENDPOINT % state_id)
    return parse_centers(res.json()["districts"])
