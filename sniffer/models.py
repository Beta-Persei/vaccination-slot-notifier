from enum import Enum
from uuid import UUID
from typing import List
from datetime import datetime


class Vaccine(Enum):
    COVISHIELD = "COVISHIELD"
    COVAXIN = "COVAXIN"


class Slots:
    name: str
    address: str
    state_name: str
    district_name: str
    block_name: str
    pincode: int
    fee_type: str
    date: str
    available_capacity: int
    min_age_limit: int
    vaccine: Vaccine
    slots: List[str]

    @classmethod
    def from_center_session(cls, center, session):
        obj = cls()
        obj.date = session.date.strftime("%d-%m-%Y")
        obj.available_capacity = session.available_capacity
        obj.min_age_limit = session.min_age_limit
        obj.vaccine = session.vaccine
        obj.slots = session.slots
        obj.name = center.name
        obj.address = center.address
        obj.state_name = center.state_name
        obj.district_name = center.district_name
        obj.block_name = center.block_name
        obj.pincode = center.pincode
        obj.fee_type = center.fee_type
        return obj


class Session:
    session_id: UUID
    date: str
    available_capacity: int
    min_age_limit: int
    vaccine: Vaccine
    slots: List[str]

    def __init__(
        self,
        session_id: UUID,
        date: str,
        available_capacity: int,
        min_age_limit: int,
        vaccine: Vaccine,
        slots: List[str],
    ):
        self.session_id = session_id
        self.date = datetime.strptime(date, "%d-%m-%Y")
        self.available_capacity = available_capacity
        self.min_age_limit = min_age_limit
        self.vaccine = vaccine
        self.slots = slots


class Center:
    center_id: int
    name: str
    address: str
    state_name: str
    district_name: str
    block_name: str
    pincode: int
    lat: int
    long: int
    center_from: datetime
    to: datetime
    fee_type: str
    sessions: List[Session]

    @classmethod
    def from_json(cls, json):
        obj = cls()
        obj.center_id = json["center_id"]
        obj.name = json["name"]
        obj.address = json["address"]
        obj.state_name = json["state_name"]
        obj.district_name = json["district_name"]
        obj.block_name = json["block_name"]
        obj.pincode = json["pincode"]
        obj.lat = json["lat"]
        obj.long = json["long"]
        obj.center_from = datetime.strptime(json["from"], "%H:%M:%S")
        obj.to = datetime.strptime(json["to"], "%H:%M:%S")
        obj.fee_type = json["fee_type"]
        obj.sessions = [Session(**x) for x in json["sessions"]]
        return obj


class State:
    state_id: int
    state_name: str

    def __init__(self, state_id: UUID, state_name: str):
        self.state_id = state_id
        self.state_name = state_name

    @classmethod
    def from_json(cls, json):
        obj = cls(json["state_id"], json["state_name"])
        return obj


class District:
    district_id: int
    district_name: str

    def __init__(self, district_id: UUID, district_name: str):
        self.district_id = district_id
        self.district_name = district_name

    @classmethod
    def from_json(cls, json):
        obj = cls(json["district_id"], json["district_name"])
        return obj
