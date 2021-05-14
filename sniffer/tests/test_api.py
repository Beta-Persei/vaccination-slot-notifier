from datetime import datetime
from unittest import mock

from django.conf import settings
from django.test import SimpleTestCase

from sniffer.api import get_centers_by_district_id, get_centers_by_pincode


class TestSnifferApi(SimpleTestCase):
    @mock.patch("sniffer.api.requests.get")
    def test_get_centers_by_pincode(self, req_get_func):
        api_response = {
            "centers": [
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
        }

        req_get_func.return_value.status_code = 200
        req_get_func.return_value.json.return_value = api_response

        res = get_centers_by_pincode(111111)

        self.assertTrue(req_get_func.called)
        self.assertEqual(req_get_func.call_args[0][0], settings.PINCODE_SLOT_ENDPOINT)
        self.assertEqual(
            req_get_func.call_args[1]["params"],
            {
                "pincode": 111111,
                "date": datetime.now().strftime("%d-%m-%Y"),
            },
        )
        self.assertEqual(
            req_get_func.call_args[1]["headers"],
            {
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
            },
        )
        self.assertEqual(len(res), len(api_response["centers"]))

    @mock.patch("sniffer.api.requests.get")
    def test_get_centers_by_pincode_invalid(self, req_get_func):
        req_get_func.return_value.status_code = 201

        res = get_centers_by_pincode(111111)

        self.assertTrue(req_get_func.called)
        self.assertTrue(req_get_func.called)
        self.assertEqual(req_get_func.call_args[0][0], settings.PINCODE_SLOT_ENDPOINT)
        self.assertEqual(
            req_get_func.call_args[1]["params"],
            {
                "pincode": 111111,
                "date": datetime.now().strftime("%d-%m-%Y"),
            },
        )
        self.assertEqual(
            req_get_func.call_args[1]["headers"],
            {
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
            },
        )
        self.assertIsNone(res)

    @mock.patch("sniffer.api.requests.get")
    def test_get_centers_by_district_id(self, req_get_func):
        api_response = {
            "centers": [
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
        }

        req_get_func.return_value.status_code = 200
        req_get_func.return_value.json.return_value = api_response

        res = get_centers_by_district_id(10)

        self.assertTrue(req_get_func.called)
        self.assertEqual(req_get_func.call_args[0][0], settings.DISTRICT_SLOT_ENDPOINT)
        self.assertEqual(
            req_get_func.call_args[1]["params"],
            {
                "district_id": 10,
                "date": datetime.now().strftime("%d-%m-%Y"),
            },
        )
        self.assertEqual(
            req_get_func.call_args[1]["headers"],
            {
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
            },
        )
        self.assertEqual(len(res), len(api_response["centers"]))

    @mock.patch("sniffer.api.requests.get")
    def test_get_centers_by_district_id_invalid(self, req_get_func):
        req_get_func.return_value.status_code = 201

        res = get_centers_by_district_id(12)

        self.assertTrue(req_get_func.called)
        self.assertTrue(req_get_func.called)
        self.assertEqual(req_get_func.call_args[0][0], settings.DISTRICT_SLOT_ENDPOINT)
        self.assertEqual(
            req_get_func.call_args[1]["params"],
            {
                "district_id": 12,
                "date": datetime.now().strftime("%d-%m-%Y"),
            },
        )
        self.assertEqual(
            req_get_func.call_args[1]["headers"],
            {
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
            },
        )
        self.assertIsNone(res)
