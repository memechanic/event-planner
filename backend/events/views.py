from datetime import timedelta

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models import QuerySet

from .authentication import EventUserJWTAuthentication
from .models import Event, Participant, Vote, Message, DateOption, Task
from .serializers import (
    EventCreateSerializer,
    EventDetailSerializer,
    EventListSerializer,
    VoteSerializer,
    MessageSerializer,
    ParticipantSerializer,
    TaskSerializer,
    EventUserRegisterSerializer,
    EventUserLoginSerializer,
)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def make_jwt_pair(user):
    """Создаёт пару access/refresh JWT-токенов для пользователя EventUser."""
    refresh = RefreshToken()
    refresh['user_id'] = str(user.id)
    refresh['username'] = user.username
    refresh['role'] = user.role
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


# ─── Auth views ──────────────────────────────────────────────────────────────

class EventUserRegisterView(generics.CreateAPIView):
    serializer_class = EventUserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = make_jwt_pair(user)
        return Response({
            **tokens,
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'role': user.role,
            }
        }, status=status.HTTP_201_CREATED)


class EventUserLoginView(generics.GenericAPIView):
    serializer_class = EventUserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        tokens = make_jwt_pair(user)
        return Response({
            **tokens,
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'role': user.role,
            }
        }, status=status.HTTP_200_OK)


class TokenRefreshView(generics.GenericAPIView):
    """Обновляет access-токен по refresh-токену."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_str = request.data.get('refresh')
        if not refresh_str:
            return Response(
                {'detail': 'Refresh-токен обязателен.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(refresh_str)
            return Response({'access': str(refresh.access_token)})
        except Exception:
            return Response(
                {'detail': 'Refresh-токен недействителен или истёк.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# ─── Event views ─────────────────────────────────────────────────────────────

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    authentication_classes = [EventUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event = serializer.save(event_user=self.request.user)
        Participant.objects.create(event=event, event_user=self.request.user)


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.prefetch_related('date_options__votes', 'participants__event_user', 'messages')
    serializer_class = EventDetailSerializer
    lookup_field = 'id'
    authentication_classes = []
    permission_classes = [AllowAny]


class EventListView(generics.ListAPIView):
    serializer_class = EventListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self) -> QuerySet[Event]:  # type: ignore
        return Event.objects.select_related('event_user').order_by('-created_at')


class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    lookup_field = 'id'
    authentication_classes = [EventUserJWTAuthentication]
    permission_classes = [IsAuthenticated]


# ─── Participant / vote / message views ───────────────────────────────────────

class VoteCreateView(generics.GenericAPIView):
    authentication_classes = [EventUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        date_option_id = request.data.get('date_option_id')
        if not date_option_id:
            return Response({'detail': 'date_option_id обязателен.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date_option = DateOption.objects.get(id=date_option_id, event_id=event_id)
        except DateOption.DoesNotExist:
            return Response({'detail': 'Вариант даты не найден.'}, status=status.HTTP_404_NOT_FOUND)

        participant, _ = Participant.objects.get_or_create(
            event_id=event_id,
            event_user=request.user,
        )

        Vote.objects.update_or_create(
            participant=participant,
            date_option=date_option,
        )
        return Response({'status': 'voted'}, status=status.HTTP_200_OK)


class EventMessagesView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_authenticators(self):
        if self.request.method == 'POST':
            return [EventUserJWTAuthentication()]
        return []

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        event_id = self.kwargs['event_id']
        participant = Participant.objects.filter(
            event_id=event_id,
            event_user=self.request.user,
        ).first()
        serializer.save(event_id=event_id, participant=participant)

    def get_queryset(self) -> QuerySet[Message]:  # type: ignore
        event_id = self.kwargs['event_id']
        return Message.objects.filter(event_id=event_id).order_by('created_at')


class EventParticipantView(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer

    def get_authenticators(self):
        if self.request.method == 'POST':
            return [EventUserJWTAuthentication()]
        return []

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        event_id = self.kwargs['event_id']
        serializer.save(event_id=event_id)

    def get_queryset(self) -> QuerySet[Participant]:  # type: ignore
        event_id = self.kwargs['event_id']
        return Participant.objects.filter(event_id=event_id)


class DateOptionCreateView(generics.GenericAPIView):
    authentication_classes = [EventUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        date_str = request.data.get('date')
        if not date_str:
            return Response({'detail': 'Поле date обязательно.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'detail': 'Событие не найдено.'}, status=status.HTTP_404_NOT_FOUND)

        from django.utils.dateparse import parse_datetime
        date = parse_datetime(date_str)
        if not date:
            return Response({'detail': 'Некорректный формат даты.'}, status=status.HTTP_400_BAD_REQUEST)

        option = DateOption.objects.create(event=event, date=date)
        return Response({'id': option.id, 'date': option.date}, status=status.HTTP_201_CREATED)


class JoinEventView(generics.GenericAPIView):
    authentication_classes = [EventUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'detail': 'Событие не найдено.'}, status=status.HTTP_404_NOT_FOUND)

        _, created = Participant.objects.get_or_create(event=event, event_user=request.user)
        return Response({'status': 'joined' if created else 'already_joined'}, status=status.HTTP_200_OK)


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_authenticators(self):
        if self.request.method == 'POST':
            return [EventUserJWTAuthentication()]
        return []

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(event_id=self.kwargs['event_id'], created_by=self.request.user)

    def get_queryset(self) -> QuerySet:  # type: ignore
        return Task.objects.filter(event_id=self.kwargs['event_id']).order_by('created_at')


class TaskUpdateDeleteView(generics.GenericAPIView):
    authentication_classes = [EventUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def _get_task(self, event_id, task_id):
        try:
            return Task.objects.select_related('event', 'assigned_to__event_user').get(
                id=task_id, event_id=event_id
            )
        except Task.DoesNotExist:
            return None

    def patch(self, request, event_id, task_id):
        task = self._get_task(event_id, task_id)
        if not task:
            return Response({'detail': 'Задача не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        is_organizer = str(task.event.event_user_id) == str(user.id)
        is_task_creator = str(task.created_by_id) == str(user.id)
        participant = Participant.objects.filter(event_id=event_id, event_user=user).first()
        is_assigned = participant and task.assigned_to_id and str(task.assigned_to_id) == str(participant.id)

        data = request.data

        if ('title' in data or 'description' in data) and not (is_task_creator or is_organizer):
            return Response({'detail': 'Редактировать задачу может только её создатель или организатор.'},
                            status=status.HTTP_403_FORBIDDEN)

        if 'assigned_to' in data:
            if not is_organizer:
                if task.assigned_to is not None:
                    return Response({'detail': 'Назначать участника может только организатор.'},
                                    status=status.HTTP_403_FORBIDDEN)
                if not participant or str(data['assigned_to']) != str(participant.id):
                    return Response({'detail': 'Вы можете взять задачу только на себя.'},
                                    status=status.HTTP_403_FORBIDDEN)

        if 'is_done' in data and not (is_assigned or is_organizer):
            return Response({'detail': 'Отмечать выполнение может назначенный участник или организатор.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = TaskSerializer(task, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, event_id, task_id):
        task = self._get_task(event_id, task_id)
        if not task:
            return Response({'detail': 'Задача не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        is_organizer = str(task.event.event_user_id) == str(user.id)
        is_task_creator = str(task.created_by_id) == str(user.id)

        if not (is_task_creator or is_organizer):
            return Response({'detail': 'Удалять задачу может только её создатель или организатор.'},
                            status=status.HTTP_403_FORBIDDEN)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserEventsView(generics.ListAPIView):
    serializer_class = EventDetailSerializer
    authentication_classes = [EventUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_authenticate_header(self, request):
        return EventUserJWTAuthentication().authenticate_header(request)

    def get_queryset(self) -> QuerySet[Event]:  # type: ignore
        user_id = self.kwargs['user_id']
        return Event.objects.filter(
            participants__event_user_id=user_id
        ).distinct().prefetch_related('date_options', 'participants__event_user', 'messages')


