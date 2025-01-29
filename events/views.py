from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from events.models import Event, Expense
from events.utils import get_events_expenses


class ListEvents(LoginRequiredMixin, ListView):
    template_name = "events/list.html"
    model = Event

    def get_context_data(self, *, object_list=None, **kwargs):  # type: ignore
        queryset = (
            Event.objects.all()
            .prefetch_related(
                "eventexpense_set__expense",
                "eventexpense_set__expense__target",
                "eventexpense_set__expense__paid_by",
            )
            .order_by("start_date")
        )
        if year := self.kwargs.get("year"):
            queryset = queryset.filter(start_date__year=year)
        return get_events_expenses(queryset)


class Details(LoginRequiredMixin, ListView):
    template_name = "events/details.html"

    def get_queryset(self):
        return Expense.objects.filter(eventexpense__event_id=self.kwargs["pk"]).order_by(
            "related_date",
        )
