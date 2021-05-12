from django.contrib import admin

from subscribers.models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_filter = ('email', 'phone_number', 'pincode', 'district_id', 'age_limit', 'active')
    actions_selection_counter = True
