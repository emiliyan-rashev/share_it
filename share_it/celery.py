import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "share_it.settings")

app = Celery("share_it")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "archive-db-and-media": {
        "task": "utils.tasks.archive_db_and_media",
        "schedule": crontab(hour="0", minute="10"),
    },
    "send-previous-month-report": {
        "task": "expenses.tasks.send_previous_month_report",
        "schedule": crontab(hour="0", minute="0", day_of_month="1"),
    },
    "alert-superdoc-new-hours": {
        "task": "utils.tasks.superdoc_notify",
        "schedule": crontab(minute="*/5"),
    },
}
