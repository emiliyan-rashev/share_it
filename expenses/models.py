from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

UserModel = get_user_model()


class ExpenseType(models.Model):
    name = models.CharField(max_length=15, unique=True)
    position = models.IntegerField(
        help_text="Column position in grouped reports.",
    )
    parent = models.ForeignKey(
        to="expenses.ExpenseType",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def get_main_type(self) -> str:
        if self.parent is None:
            return self.name
        exp_type = self.parent
        while True:
            if exp_type.parent is None:
                break
            exp_type = exp_type.parent
        return exp_type.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "position"],
                name="unique_position",
            ),
            models.UniqueConstraint(
                "position",
                condition=Q(parent__isnull=True),
                name="unique_main_position",
            ),
        ]

    def __str__(self) -> str:
        if self.parent is None:
            return self.name
        return f"{self.name} ({self.get_main_type()})"


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

    def __str__(self):
        return f"{self.related_date} | {self.value} | {self.target}"
