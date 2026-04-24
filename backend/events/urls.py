from django.urls import path
from .views import (
    EventCreateView,
    EventListView,
    EventDeleteView,
    EventDetailView,
    VoteCreateView,
    EventMessagesView,
    EventParticipantView,
    EventUserRegisterView,
    EventUserLoginView,
    UserEventsView,
    )

urlpatterns = [
    path('events/', EventCreateView.as_view()),
    path('events/list/', EventListView.as_view()),
    path('events/<uuid:id>/', EventDetailView.as_view()),
    path('events/<uuid:id>/delete/', EventDeleteView.as_view()),
    path('events/<uuid:event_id>/messages/', EventMessagesView.as_view()),
    path('events/<uuid:event_id>/participants/', EventParticipantView.as_view()),
    path('events/<uuid:event_id>/votes/', VoteCreateView.as_view()),
    path('auth/register/', EventUserRegisterView.as_view()),
    path('auth/login/', EventUserLoginView.as_view()),
    path('users/<uuid:user_id>/events/', UserEventsView.as_view()),
]