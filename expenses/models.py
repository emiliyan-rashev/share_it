from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class ExpenseType(models.Model):
    name = models.CharField(max_length=15, unique=True)
    position = models.IntegerField(
        unique=True,
        help_text="Column position in grouped reports.",
    )

    def __str__(self) -> str:
        return self.name


class Expense(models.Model):
    related_date = models.DateField(help_text="Date that the expense is accounted to.")
    value = models.DecimalField(max_digits=6, decimal_places=2)
    target = models.ForeignKey(to=ExpenseType, on_delete=models.PROTECT)
    paid_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    comment = models.TextField(
        max_length=200,
        null=True,
        blank=True,
    )
