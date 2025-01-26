from django.urls import path

from expenses.views import ListExpensesByMonth, DetailsPerMonth

app_name = "expenses"

urlpatterns = [
    path("all", ListExpensesByMonth.as_view(), name="list"),
    path("<int:year>", ListExpensesByMonth.as_view(), name="by-year"),
    path("<int:month>/<int:year>/details", DetailsPerMonth.as_view(), name="details"),
]
