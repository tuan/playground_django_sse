from django.urls import path
from .views import HomeView, stream

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("stream/", stream, name="stream"),
]
