from django.urls import path
from .views import EventCreateView, EventDetailView, VoteCreateView, EventMessagesView, MessageCreateView

urlpatterns = [
    path('events/', EventCreateView.as_view()),
    path('events/<uuid:id>/', EventDetailView.as_view()),
    path('votes/', VoteCreateView.as_view()),
    path('events/<uuid:event_id>/messages/', EventMessagesView.as_view()),
    path('messages/', MessageCreateView.as_view()),
]