from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from expenses.models import Expense
from expenses.utils import get_expenses_per_month


class ListExpensesByMonth(LoginRequiredMixin, ListView):
    template_name = "expenses/list_by_month.html"
    model = Expense

    def get_context_data(self, *, object_list=None, **kwargs):  # type: ignore
        return get_expenses_per_month(Expense.objects.all())


class DetailsPerMonth(LoginRequiredMixin, ListView):
    template_name = "expenses/details_per_month.html"

    def get_queryset(self):
        return Expense.objects.filter(
            related_date__month=self.kwargs["month"],
            related_date__year=self.kwargs["year"],
        )
