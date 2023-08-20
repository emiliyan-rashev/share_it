from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from expenses.models import Expense
from expenses.utils import get_expenses_per_month
from share_it.celery import app
from django.core.mail import send_mail

UserModel = get_user_model()


@app.task
def send_previous_month_report() -> None:
    recipient_list = list(UserModel.objects.values_list("email", flat=True))
    month_ago = datetime.now() - relativedelta(months=1)
    expenses = (
        Expense.objects.filter(
            related_date__month=month_ago.month, related_date__year=month_ago.year
        )
        .order_by("related_date")
        .select_related(
            "target",
            "paid_by",
        )
    )
    if not expenses:
        return
    context = dict(get_expenses_per_month(expenses))
    context["expenses"] = expenses
    html = render_to_string("expenses/expense_report.html", context)
    send_mail(
        subject=f"Разходи за {month_ago.strftime('%m/%Y')}",
        message="",
        html_message=html,
        from_email=None,
        recipient_list=recipient_list,
    )
