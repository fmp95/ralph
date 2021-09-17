from django.urls import path

from ralph.api import api

# API urls.
urlpatterns = [path("", api.urls)]
