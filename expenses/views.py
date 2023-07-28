from django.views.generic import ListView

from expenses.models import Expense
from expenses.utils import get_expenses_per_month


class ListExpensesByMonth(ListView):
    template_name = "expenses/list_by_month.html"
    model = Expense

    def get_context_data(self, *, object_list=None, **kwargs):  # type: ignore
        return get_expenses_per_month(Expense.objects.all())
