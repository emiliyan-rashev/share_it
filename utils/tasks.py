import requests
from django.core.mail import send_mail
from django.core.management import call_command

from share_it.celery import app


@app.task
def archive_db_and_media() -> None:
    call_command("cleanup_unused_media", "--noinput")
    call_command("mediabackup", "-e")
    call_command("dbbackup", "-e")


@app.task
def superdoc_notify(days: int = 30) -> None:
    url = f"https://superdoc.bg/calendar/7041/first/{days}"
    slots = []
    for day in requests.get(url).json()["calendar"]["output"]:
        for slot in day["slots_list"]:
            if slot["nzok"] and slot["bookable"]:
                slots.append(f'{day["date"]} {slot["time"]}')
    if slots:
        send_mail(
            subject=f"Свободни часове за лекар",
            message="\n".join(slots),
            from_email=None,
            recipient_list=['emiliyan.rashev@gmail.com'],
        )
