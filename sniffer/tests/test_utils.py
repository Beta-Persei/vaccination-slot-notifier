from django.test import SimpleTestCase

from sniffer.models import Center
from sniffer.utils import parse_centers


class TestSnifferUtils(SimpleTestCase):
    def test_parse_centers(self):
        center_list = [
            {
                "center_id": 7986,
                "name": "DGD Chhawla PHC",
                "address": "Village And Post Office Chhawla Near Radha Krishan Mandir Chhawla New Delhi - 110071",
                "state_name": "Delhi",
                "district_name": "South West Delhi",
                "block_name": "Not Applicable",
                "pincode": 110071,
                "lat": 28,
                "long": 77,
                "from": "09:00:00",
                "to": "17:00:00",
                "fee_type": "Free",
                "sessions": [
                    {
                        "session_id": "e18b9a85-0c6d-4684-ac5b-21dea3899867",
                        "date": "08-05-2021",
                        "available_capacity": 3,
                        "min_age_limit": 45,
                        "vaccine": "COVISHIELD",
                        "slots": [
                            "09:00AM-11:00AM",
                            "11:00AM-01:00PM",
                            "01:00PM-03:00PM",
                            "03:00PM-05:00PM",
                        ],
                    }
                ],
            },
            {
                "center_id": 693703,
                "name": "SKV DEENDARPUR 1",
                "address": "DEENPUR NEAR JHOR DEENPUR GOLA GAANV ROAD NAJAFGARH SCHOOL ID-1822176",
                "state_name": "Delhi",
                "district_name": "South West Delhi",
                "block_name": "Not Applicable",
                "pincode": 110071,
                "lat": 28,
                "long": 77,
                "from": "09:00:00",
                "to": "17:00:00",
                "fee_type": "Free",
                "sessions": [
                    {
                        "session_id": "0ac8ddcd-da25-477d-88a7-563b1a9877b2",
                        "date": "13-05-2021",
                        "available_capacity": 0,
                        "min_age_limit": 18,
                        "vaccine": "COVISHIELD",
                        "slots": [
                            "09:00AM-11:00AM",
                            "11:00AM-01:00PM",
                            "01:00PM-03:00PM",
                            "03:00PM-05:00PM",
                        ],
                    }
                ],
            },
            {
                "center_id": 605135,
                "name": "DGD Kanganheri",
                "address": "KANGHERI Phc",
                "state_name": "Delhi",
                "district_name": "South West Delhi",
                "block_name": "Not Applicable",
                "pincode": 110071,
                "lat": 28,
                "long": 76,
                "from": "09:00:00",
                "to": "17:00:00",
                "fee_type": "Free",
                "sessions": [
                    {
                        "session_id": "5e283285-b2e1-4d21-9d32-0c1bbb2195f9",
                        "date": "13-05-2021",
                        "available_capacity": 0,
                        "min_age_limit": 45,
                        "vaccine": "COVISHIELD",
                        "slots": [
                            "09:00AM-11:00AM",
                            "11:00AM-01:00PM",
                            "01:00PM-03:00PM",
                            "03:00PM-05:00PM",
                        ],
                    },
                ],
            },
            {
                "center_id": 605135,
                "name": "DGD Kanganheri",
                "address": "KANGHERI Phc",
                "state_name": "Delhi",
                "district_name": "South West Delhi",
                "block_name": "Not Applicable",
                "pincode": 110071,
                "lat": 28,
                "long": 76,
                "from": "09:00:00",
                "to": "17:00:00",
                "fee_type": "Free",
                "sessions": [
                    {
                        "session_id": "5e283285-b2e1-4d21-9d32-0c1bbb2195f9",
                        "date": "13-05-2021",
                        "available_capacity": 5,
                        "min_age_limit": 18,
                        "vaccine": "COVISHIELD",
                        "slots": [
                            "09:00AM-11:00AM",
                            "11:00AM-01:00PM",
                            "01:00PM-03:00PM",
                            "03:00PM-05:00PM",
                        ],
                    },
                ],
            },
        ]

        parsed_center_list = parse_centers(center_list)

        self.assertEqual(len(parsed_center_list), len(center_list))
        self.assertIsInstance(parsed_center_list[0], Center)
