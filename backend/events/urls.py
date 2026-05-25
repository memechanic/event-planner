from django.urls import path
from .views import (
    EventCreateView,
    EventListView,
    EventDeleteView,
    EventDetailView,
    VoteCreateView,
    DateOptionCreateView,
    JoinEventView,
    EventMessagesView,
    EventParticipantView,
    EventUserRegisterView,
    EventUserLoginView,
    TokenRefreshView,
    UserEventsView,
)

urlpatterns = [
    # Auth
    path('auth/register/', EventUserRegisterView.as_view()),
    path('auth/login/', EventUserLoginView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),

    # Events
    path('events/', EventCreateView.as_view()),
    path('events/list/', EventListView.as_view()),
    path('events/<uuid:id>/', EventDetailView.as_view()),
    path('events/<uuid:id>/delete/', EventDeleteView.as_view()),
    path('events/<uuid:event_id>/messages/', EventMessagesView.as_view()),
    path('events/<uuid:event_id>/participants/', EventParticipantView.as_view()),
    path('events/<uuid:event_id>/votes/', VoteCreateView.as_view()),
    path('events/<uuid:event_id>/dates/', DateOptionCreateView.as_view()),

    path('events/<uuid:event_id>/join/', JoinEventView.as_view()),

    # Users
    path('users/<uuid:user_id>/events/', UserEventsView.as_view()),
]