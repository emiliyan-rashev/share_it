from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.test import TestCase

from expenses.models import ExpenseType, Expense
from expenses.utils import get_expenses_per_month

UserModel = get_user_model()


class GetExpensesPerMonthTest(TestCase):
    def test_get_expenses(self) -> None:
        month_ago = datetime.now() - relativedelta(months=1)
        user_1 = UserModel.objects.create(email="user1@gmail.com")
        user_2 = UserModel.objects.create(email="user2@gmail.com")
        expense_type_1 = ExpenseType.objects.create(name="Expense type 1", position=1)
        expense_type_2 = ExpenseType.objects.create(name="Expense type 2", position=2)
        Expense.objects.create(
            related_date=month_ago,
            value=1,
            target=expense_type_1,
            paid_by=user_1,
        )
        Expense.objects.create(
            related_date=month_ago,
            value=2,
            target=expense_type_1,
            paid_by=user_2,
        )
        Expense.objects.create(
            related_date=month_ago,
            value=3,
            target=expense_type_2,
            paid_by=user_1,
        )
        Expense.objects.create(
            related_date=month_ago,
            value=4,
            target=expense_type_2,
            paid_by=user_2,
        )
        result = get_expenses_per_month(Expense.objects.all())
        self.assertEqual(result["expense_types_names"], [expense_type_1.name, expense_type_2.name])
        self.assertSetEqual(result["users"], {user_1, user_2})
        self.assertDictEqual(
            result["expenses_by_month"],
            {
                (month_ago.month, month_ago.year): {
                    "per_type": {
                        expense_type_1.name: Decimal(3),
                        expense_type_2.name: Decimal(7),
                    },
                    "total": Decimal(10),
                    "per_user": {
                        user_1: {"paid": Decimal(4), "owes": Decimal(1)},
                        user_2: {"paid": Decimal(6), "owes": Decimal(0)},
                    },
                }
            },
        )
