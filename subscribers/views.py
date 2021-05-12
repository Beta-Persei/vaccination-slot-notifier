from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from subscribers.forms import SubscriberForm
from subscribers.models import Subscriber
from subscribers.utils import check_and_notify_subscriber, welcome_new_subscriber


class SubscriberCreateView(SuccessMessageMixin, FormView):
    form_class = SubscriberForm

    template_name = "subscribers/index.html"
    success_message = (
        "You will be notified via email whenever a vaccinaton slot is available!"
    )
    success_url = "/"
    extra_context = {"subscriber_count": Subscriber.objects.count()}

    def form_valid(self, form):
        obj = form.save()
        welcome_new_subscriber(obj)
        check_and_notify_subscriber(obj)
        return super().form_valid(form)


def unsubscribe_view(request, pk):
    try:
        obj = Subscriber.objects.get(pk=pk)
        obj.active = False
        obj.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            "You have unsubscribed from slot availability updates.",
        )
    except ObjectDoesNotExist:
        messages.add_message(request, messages.WARNING, "Oops! Something went wrong.")

    return redirect("/")
