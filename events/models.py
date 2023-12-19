from typing import Optional

from django.contrib.auth import get_user_model
from django.db import models

from expenses.models import Expense

UserModel = get_user_model()


class Event(models.Model):
    name = models.CharField(max_length=100)
    comments = models.CharField(max_length=1000, blank=True, null=True)
    leave = models.IntegerField(default=0, help_text="Paid leave needed.")
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def duration(self) -> Optional[int]:
        """Event duration in days."""
        if self.start_date == self.end_date:
            return None
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return self.name


class EventExpense(models.Model):
    expense = models.OneToOneField(to=Expense, on_delete=models.PROTECT)
    event = models.ForeignKey(to=Event, on_delete=models.PROTECT)
