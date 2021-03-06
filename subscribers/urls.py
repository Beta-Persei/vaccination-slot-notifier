from django.urls import include, path

from subscribers.views import SubscriberCreateView, unsubscribe_view

urlpatterns = [
    path("", SubscriberCreateView.as_view(), name="subscriber-add"),
    path("unsubscribe/<uuid:pk>/", unsubscribe_view, name="subscriber-update"),
]
