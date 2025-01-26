from decimal import Decimal
from typing import TypedDict, Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Sum

from events.models import Event, EventExpense
from expenses.models import ExpenseType
from users.models import User

UserModel = get_user_model()


class EventExpenses(TypedDict):
    per_type: dict[str, Decimal]
    per_user: dict[User, Decimal]


class EventData(TypedDict):
    expense_types_names: list
    events: dict[Event, EventExpenses]
    users: set
    years: Optional[list[int]]


def get_events_expenses(events: QuerySet[Event]) -> EventData:
    users = set(UserModel.objects.all())
    expense_types_names = list(
        ExpenseType.objects.filter(expense__eventexpense__isnull=False)
        .values_list("name", flat=True)
        .distinct()
        .order_by("position"),
    )
    events_data: dict[Event, EventExpenses] = {}
    for event in events.annotate(total=Sum("eventexpense__expense__value")):
        events_data[event] = {
            "per_type": {
                expense_name: Decimal(0) for expense_name in expense_types_names
            },
            "per_user": {user: Decimal(0) for user in users},
        }
        for event_expense in event.eventexpense_set.all():
            name = event_expense.expense.target.name
            value = event_expense.expense.value
            paid_by = event_expense.expense.paid_by
            events_data[event]["per_type"][name] += value
            events_data[event]["per_user"][paid_by] += value

    return {
        "expense_types_names": expense_types_names,
        "users": users,
        "events": events_data,
        "years": list(
            Event.objects.all()
            .distinct("start_date__year")
            .values_list("start_date__year", flat=True)
        )
    }
