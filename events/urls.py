from django.urls import path

from events.views import ListEvents, Details

app_name = "events"

urlpatterns = [
    path("all", ListEvents.as_view(), name="list"),
    path("<int:pk>/details", Details.as_view(), name="details"),
]
