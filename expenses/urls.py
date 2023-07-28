from django.urls import path

from expenses.views import ListExpensesByMonth

app_name = "expenses"

urlpatterns = [
    path("all", ListExpensesByMonth.as_view(), name="list")
]
