from rest_framework import generics, status
from rest_framework.response import Response

from .models import Event, Vote
from .serializers import EventCreateSerializer, EventDetailSerializer, VoteSerializer


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
        serializer.is_valid(raise_exceptrion=True)

        Vote.objects.update_or_create(
            participant = serializer.validated_data['participant'],
            date_option = serializer.validated_data['date_option'],
        )

        return Response({'status': 'voted'}, status=status.HTTP_200_OK)

