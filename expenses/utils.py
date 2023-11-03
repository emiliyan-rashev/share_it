from decimal import Decimal
from typing import TypedDict, Tuple, Type

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from expenses.models import ExpenseType, Expense
from users.models import User

UserModel = get_user_model()


class ExpensesPerUser(TypedDict):
    paid: Decimal
    owes: Decimal


class ExpensesByMonth(TypedDict):
    per_type: dict[str, Decimal]
    per_user: dict[User, ExpensesPerUser]
    total: Decimal | int


class ExpensesPerMonthData(TypedDict):
    expense_types_names: list
    expenses_by_month: dict[Tuple[int, int], ExpensesByMonth]
    users: set


def get_expenses_per_month(expenses: QuerySet[Expense]) -> ExpensesPerMonthData:
    expenses_by_month: dict[Tuple[int, int], ExpensesByMonth] = {}
    expense_types_names = list(
        ExpenseType.objects.values_list("name", flat=True).order_by("position")
    )
    users = set(UserModel.objects.all())
    for expense in expenses.select_related("target", "paid_by").order_by(
        "related_date"
    ):
        date = (expense.related_date.month, expense.related_date.year)
        expenses_by_month.setdefault(
            date,
            {
                "per_type": {
                    expense_name: Decimal(0) for expense_name in expense_types_names
                },
                "per_user": {user: {"paid": Decimal(0), "owes": Decimal(0)} for user in users},
                "total": Decimal(0),
            },
        )
        expenses_by_month[date]["per_type"][expense.target.name] += expense.value
        expenses_by_month[date]["per_user"][expense.paid_by]["paid"] += expense.value
    for month_data in expenses_by_month.values():
        total = sum(month_data["per_type"].values())
        total_per_user = Decimal(sum(month_data["per_type"].values()) / len(users))
        month_data["total"] = total
        for user_data in month_data["per_user"].values():
            if user_data["paid"] < total_per_user:
                user_data["owes"] = total_per_user - user_data["paid"]

    return {
        "expense_types_names": expense_types_names,
        "expenses_by_month": expenses_by_month,
        "users": users,
    }
