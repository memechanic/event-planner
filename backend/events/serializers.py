from rest_framework import serializers
from .models import Event, DateOption, EventUser, Participant, Vote, Message


class DateOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateOption
        fields = ('id', 'date')


class EventUserGetOrCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = ('id', 'username', 'email')
        read_only_fields = ('id',)

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']

        user, created = EventUser.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        # если пользователь уже был — можно обновить username
        if not created and user.username != username:
            user.username = username
            user.save(update_fields=['username'])

        return user


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

