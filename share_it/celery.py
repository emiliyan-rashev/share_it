import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "share_it.settings")

app = Celery("share_it")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "archive-db": {
        "task": "expenses.tasks.archive_db",
        "schedule": crontab(hour="0", minute="0"),
    },
    "send-previous-month-report": {
        "task": "expenses.tasks.send_previous_month_report",
        "schedule": crontab(hour="0", minute="0", day_of_month="1"),
    },
}
