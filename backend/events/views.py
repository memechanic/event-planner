from rest_framework import generics, status
from rest_framework.response import Response

from django.db.models import QuerySet

from .models import Event, Vote, Message
from .serializers import EventCreateSerializer, EventDetailSerializer, VoteSerializer, MessageSerializer, ParticipantSerializer


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    lookup_field = 'id'


class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Vote.objects.update_or_create(
            participant = serializer.validated_data['participant'],
            date_option = serializer.validated_data['date_option'],
        )

        return Response({'status': 'voted'}, status=status.HTTP_200_OK)


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer


class EventMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self) -> QuerySet[Message]: #type:ignore Ошибка в типизации DRF
        event_id = self.kwargs['event_id']
        queryset = Message.objects.filter(event_id=event_id).order_by('created_at')
        return queryset
    