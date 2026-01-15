from rest_framework import serializers
from .models import Event, DateOption, Participant, Vote, Message


class DateOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateOption
        fields = ('id', 'date')


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'username')


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
            'title',
            'description',
            'created_at',
            'date_options',
            'participants',
            'messages',
        )


class EventCreateSerializer(serializers.ModelSerializer):
    dates = serializers.ListField(
        child=serializers.DateField(),
        write_only=True
    )

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'dates')

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

