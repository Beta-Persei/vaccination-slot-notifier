from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from subscribers.forms import SubscriberForm
from subscribers.models import Subscriber


class SubscriberCreateView(SuccessMessageMixin, FormView):
    form_class = SubscriberForm

    template_name = "subscribers/index.html"
    success_message = (
        "You will be notified when a vaccinaton slot is available!"
    )
    success_url = "/"

    def form_valid(self, form):
        obj = form.save()
        obj.send_welcome_mail()
        obj.check_and_notify_slots()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscriber_count"] = Subscriber.objects.count()
        return context


def unsubscribe_view(request, pk):
    try:
        obj = Subscriber.objects.get(pk=pk)
        obj.active = False
        obj.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            "You have unsubscribed from vaccinaton slot updates.",
        )
    except ObjectDoesNotExist:
        messages.add_message(request, messages.WARNING, "Oops! Something went wrong.")

    return redirect("/")
