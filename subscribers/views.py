from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ObjectDoesNotExist


from subscribers.forms import SubscriberForm
from subscribers.models import Subscriber
from subscribers.utils import check_and_notify_subscriber


def test(request):
    return render(request,"subscribers/index.html")

class SubscriberCreateView(SuccessMessageMixin, FormView):
    form_class = SubscriberForm
    
    template_name = "subscribers/index.html"
    success_message = "You will be notified via email whenever a vaccinaton slot is available"
    success_url = "/"

    def form_valid(self, form):
        obj = form.save()
        check_and_notify_subscriber(obj)
        return super().form_valid(form)
    

def unsubscribe_view(request, pk):
    try:
        obj = Subscriber.objects.get(pk=pk)
        obj.active = False
        obj.save()

        messages.add_message(request, messages.SUCCESS, 'You have unsubscribed from slot availability updates.')
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Oops! Something went wrong.")

    return redirect("/")

