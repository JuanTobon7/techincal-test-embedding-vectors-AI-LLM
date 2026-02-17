from django.urls import path

from .views import SuggestRAEView

urlpatterns = [
    path("sugerir-rae/", SuggestRAEView.as_view(), name="sugerir-rae"),
]

