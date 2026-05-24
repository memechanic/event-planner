import re

from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers

from .models import Event, DateOption, EventUser, Participant, Vote, Message


# ─── Date options ────────────────────────────────────────────────────────────

class DateOptionSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(source='votes.count', read_only=True)

    class Meta:
        model = DateOption
        fields = ('id', 'date', 'vote_count')


# ─── Auth ────────────────────────────────────────────────────────────────────

class EventUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=8, max_length=24,
        style={'input_type': 'password'},
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = EventUser
        fields = ('id', 'username', 'email', 'password', 'password2')
        read_only_fields = ('id',)

    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                'Пароль должен содержать хотя бы одну заглавную букву.'
            )
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                'Пароль должен содержать хотя бы одну строчную букву.'
            )
        if not re.search(r'[!@#$%^&*()\-_=+\[\]{};:\'",.<>?/\\|`~]', value):
            raise serializers.ValidationError(
                'Пароль должен содержать хотя бы один специальный символ.'
            )
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError(
                {'password2': 'Пароли не совпадают.'}
            )
        if EventUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {'email': 'Пользователь с таким email уже существует.'}
            )
        if EventUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {'username': 'Это имя уже занято другим пользователем.'}
            )
        # Хэшируем пароль перед сохранением
        attrs['password'] = make_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        return EventUser.objects.create(**validated_data)


class EventUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128, style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs['username'].strip()
        password = attrs['password']

        user = EventUser.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError(
                {'username': 'Пользователь с таким именем не найден.'}
            )
        if not check_password(password, user.password):
            raise serializers.ValidationError(
                {'password': 'Неверный пароль.'}
            )

        attrs['user'] = user
        return attrs


# ─── Participants & Messages ──────────────────────────────────────────────────

class ParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='event_user.username', read_only=True)

    class Meta:
        model = Participant
        fields = ('id', 'event_user', 'username')


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(
        source='participant.event_user.username',
        read_only=True,
    )

    class Meta:
        model = Message
        fields = ('id', 'sender_username', 'text', 'created_at')


# ─── Events ──────────────────────────────────────────────────────────────────

class EventDetailSerializer(serializers.ModelSerializer):
    date_options = DateOptionSerializer(many=True, read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'event_user',
            'title',
            'description',
            'created_at',
            'date_options',
            'participants',
            'messages',
        )


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'event_user',
            'title',
            'description',
            'created_at',
        )


class EventCreateSerializer(serializers.ModelSerializer):
    dates = serializers.ListField(
        child=serializers.DateTimeField(),
        write_only=True,
    )

    class Meta:
        model = Event
        fields = ('id', 'event_user', 'title', 'description', 'dates')

    def create(self, validated_data):
        dates = validated_data.pop('dates')
        event = Event.objects.create(**validated_data)
        DateOption.objects.bulk_create([
            DateOption(event=event, date=date)
            for date in dates
        ])
        return event


# ─── Votes ───────────────────────────────────────────────────────────────────

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('participant', 'date_option')
