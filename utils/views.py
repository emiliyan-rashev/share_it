from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse


def private_media(request, file_path):
    if settings.DEBUG:
        return HttpResponseRedirect(redirect_to=f"/{settings.MEDIA_FOLDER_NAME}/{file_path}")
    response = HttpResponse()
    response["Content-Type"] = "image/jpeg"
    response['X-Accel-Redirect'] = f"/{settings.MEDIA_FOLDER_NAME}/{file_path}"
    return response
