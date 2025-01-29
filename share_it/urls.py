from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path(
        "",
        RedirectView.as_view(url=reverse_lazy("expenses:by-year", kwargs={"year": 2025})),
        name="home",
    ),
    path("expenses/", include("expenses.urls", namespace="expenses")),
    path("events/", include("events.urls", namespace="events")),
    path("utils/", include("utils.urls", namespace="utils")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
