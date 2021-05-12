from datetime import datetime, timedelta

from constance import config

from subscribers.models import Subscriber
from subscribers.utils import check_and_notify_subscriber
from vaccination_slot_notifier import celery_app


@celery_app.task
def check_available_slots():
    subscriber_list = Subscriber.objects.filter(
        active=True,
        last_mail_sent__lt=datetime.now()
        - timedelta(seconds=config.MAIL_COOLDOWN_SECONDS),
    )
    for subscriber in subscriber_list:
        check_and_notify_subscriber(subscriber)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        config.SNIFFING_INTERVAL_SECONDS, check_available_slots.s()
    )
