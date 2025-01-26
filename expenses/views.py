from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from expenses.models import Expense
from expenses.utils import get_expenses_per_month


class ListExpensesByMonth(LoginRequiredMixin, ListView):
    template_name = "expenses/list_by_month.html"
    model = Expense

    def get_context_data(self, *, object_list=None, **kwargs):  # type: ignore
        queryset = Expense.objects.all()
        if year := self.kwargs.get("year"):
            queryset = queryset.filter(related_date__year=year)
        return get_expenses_per_month(queryset)


class DetailsPerMonth(LoginRequiredMixin, ListView):
    template_name = "expenses/details_per_month.html"
    extra_context = {"should_display_main_type": True}

    def get_queryset(self):
        return Expense.objects.filter(
            related_date__month=self.kwargs["month"],
            related_date__year=self.kwargs["year"],
        ).order_by("related_date")
