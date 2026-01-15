from django.urls import path
from .views import EventCreateView, EventDetailView, VoteCreateView

urlpatterns = [
    path('events/', EventCreateView.as_view()),
    path('events/<uuid:id>/', EventDetailView.as_view()),
    path('votes/', VoteCreateView.as_view()),
]