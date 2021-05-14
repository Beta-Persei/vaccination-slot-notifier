import uuid
from http import HTTPStatus

from django.test import SimpleTestCase
from django.urls import resolve, reverse

from subscribers.views import SubscriberCreateView, unsubscribe_view


class TestSubscriberUrls(SimpleTestCase):
    def test_subscriber_url_resolved(self):
        url = reverse("subscriber-add")
        self.assertEqual(resolve(url).func.view_class, SubscriberCreateView)

    def test_unsubscriber_url_resolved(self):
        url = reverse("subscriber-update", args=[uuid.uuid4()])
        self.assertEqual(resolve(url).func, unsubscribe_view)
