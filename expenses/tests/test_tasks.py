from datetime import datetime
from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.test import TestCase

from expenses.models import Expense, ExpenseType
from expenses.tasks import send_previous_month_report

UserModel = get_user_model()


@patch("expenses.tasks.send_mail")
class SendPreviousMonthReportTest(TestCase):
    def setUp(self) -> None:
        user = UserModel.objects.create(email="user1@gmail.com")
        expense_target = ExpenseType.objects.create(name="Expense type 1", position=1)
        Expense.objects.create(
            related_date=datetime(2023, 2, 1).date(),
            value=1,
            target=expense_target,
            paid_by=user,
        )

    def test_send_mail_without_data(self, mock_send_mail: MagicMock) -> None:
        send_previous_month_report()
        mock_send_mail.assert_not_called()

    @patch("expenses.tasks.datetime")
    def test_send_mail_on_first_day_of_month(
        self,
        mock_datetime: MagicMock,
        mock_send_mail: MagicMock,
    ) -> None:
        mock_datetime.now.return_value = datetime(2023, 3, 1)
        send_previous_month_report()
        mock_send_mail.assert_called()

    @patch("expenses.tasks.datetime")
    def test_send_mail_on_last_day_of_month(
        self,
        mock_datetime: MagicMock,
        mock_send_mail: MagicMock,
    ) -> None:
        mock_datetime.now.return_value = datetime(2023, 3, 31)
        send_previous_month_report()
        mock_send_mail.assert_called()
