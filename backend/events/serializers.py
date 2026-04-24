from rest_framework import serializers
from .models import Event, DateOption, EventUser, Participant, Vote, Message


class DateOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateOption
        fields = ('id', 'date')


class EventUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = ('id', 'username', 'email')
        read_only_fields = ('id',)

    def validate(self, attrs):
        email = attrs['email']
        username = attrs['username']

        if EventUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'email': 'Пользователь с таким email уже существует.'
            })

        if EventUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                'username': 'Это имя уже занято другим пользователем.'
            })

        return attrs

    def create(self, validated_data):
        return EventUser.objects.create(**validated_data)


class EventUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)

    def validate(self, attrs):
        email = attrs['email']
        username = attrs['username']
        user = EventUser.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError({
                'email': 'Пользователь с таким email не найден.'
            })

        if user.username != username:
            raise serializers.ValidationError({
                'username': 'Неверное имя пользователя для указанного email.'
            })

        attrs['user'] = user
        return attrs


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'event_user')


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(
        source = 'participant.username',
        read_only = True
    )

    class Meta:
        model = Message
        fields = ('id', 'sender_username', 'text', 'created_at')


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
        write_only=True
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


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('participant', 'date_option')

