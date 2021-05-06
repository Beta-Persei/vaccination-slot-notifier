## Redis

## Celery worker

celery -A vaccination_slot_notifier worker -l DEBUG

## Celery worker

celery -A vaccination_slot_notifier beat -l DEBUG
