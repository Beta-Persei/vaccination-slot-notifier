from datetime import datetime, timedelta

from celery.schedules import crontab
from constance import config

from subscribers.models import Subscriber
from vaccination_slot_notifier import celery_app


@celery_app.task
def check_available_slots():
    subscriber_list = Subscriber.objects.filter(
        active=True,
        last_mail_sent__lt=datetime.now()
        - timedelta(seconds=config.MAIL_COOLDOWN_SECONDS),
    )
    for subscriber in subscriber_list:
        subscriber.check_and_notify_slots()


@celery_app.task
def refresh_sms_count():
    Subscriber.objects.update(daily_sms_count=0)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        config.SNIFFING_INTERVAL_SECONDS, check_available_slots.s()
    )

    sender.add_periodic_task(
        crontab(
            hour=0,
            minute=0,
        ),
        refresh_sms_count.s(),
    )
