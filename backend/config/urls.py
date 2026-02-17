from django.urls import include, path

urlpatterns = [
    path("api/", include("learning_outcomes.urls")),
]

