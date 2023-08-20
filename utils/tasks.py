from django.core.management import call_command

from share_it.celery import app


@app.task
def archive_db_and_media() -> None:
    call_command("cleanup_unused_media", "--noinput")
    call_command("mediabackup", "-e")
    call_command("dbbackup", "-e")
