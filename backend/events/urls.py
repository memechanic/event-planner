from django.urls import path
from .views import (
    EventCreateView,
    EventDetailView,
    VoteCreateView,
    EventMessagesView,
    EventParticipantView,
    EventUserGetOrCreateView,
    )

urlpatterns = [
    path('events/', EventCreateView.as_view()),
    path('events/<uuid:id>/', EventDetailView.as_view()),
    path('events/<uuid:event_id>/messages/', EventMessagesView.as_view()),
    path('events/<uuid:event_id>/participants/', EventParticipantView.as_view()),
    path('events/<uuid:event_id>/votes/', VoteCreateView.as_view()),
    path('auth/login/', EventUserGetOrCreateView.as_view()),
]