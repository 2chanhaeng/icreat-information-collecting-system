from django.urls import path
from . import views

urlpatterns = [
    path("", views.TrialsView.as_view()),
    path("<pk>/", views.TrialView.as_view()),
]
