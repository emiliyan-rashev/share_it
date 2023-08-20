from django.urls import path

from utils.views import private_media

app_name = "utils"

urlpatterns: list = [
    path("private-media/<path:file_path>", private_media, name="private-media"),
]
