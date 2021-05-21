import uuid
from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from subscribers.forms import SubscriberForm
from subscribers.models import Subscriber


class TestSubscriberViews(TestCase):
    def setUp(self):
        self.subscriber_add_url = reverse("subscriber-add")
        self.test_subscriber = Subscriber.objects.create(
            email="foo@bar.com", pincode=111111
        )
        self.unsubscriber_url = reverse(
            "subscriber-update", args=[self.test_subscriber.id]
        )
        return super().setUp()

    def test_subscriber_create_view_get(self):
        response = self.client.get(self.subscriber_add_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "subscribers/index.html")

    def test_subscriber_create_view_post_valid(self):
        response = self.client.post(
            self.subscriber_add_url,
            {
                "email": "foo2@bar.com",
                "phone_number": "+919999999999",
                "age_limit": 45,
                "pincode": "",
                "state": 1,
                "district_id": 1,
                "search_type": "district",
            },
        )

        obj = Subscriber.objects.latest("created_date")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(obj.email, "foo2@bar.com")
        self.assertEqual(obj.age_limit, 45)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "You will be notified when a vaccinaton slot is available!",
        )

    def test_unsubscriber_view_get(self):
        response = self.client.get(self.unsubscriber_url)
        self.assertRedirects(
            response,
            self.subscriber_add_url,
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(Subscriber.objects.get(id=self.test_subscriber.id).active)

    def test_unsubscriber_view_get_invalid_uuid(self):
        invalid_unsubscriber_url = reverse("subscriber-update", args=[uuid.uuid4()])
        response = self.client.get(invalid_unsubscriber_url)

        self.assertRedirects(
            response,
            self.subscriber_add_url,
            status_code=302,
            target_status_code=200,
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Oops! Something went wrong.",
        )
