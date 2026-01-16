from django.db import models
import uuid
# Create your models here.


class EventUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_user = models.ForeignKey(
        EventUser,
        on_delete=models.CASCADE,
        related_name='events',
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DateOption(models.Model):
    event = models.ForeignKey(
        Event,
        related_name='date_options',
        on_delete=models.CASCADE
    )

    date = models.DateTimeField()

    def __str__(self):
        return f"{self.event.title} — {self.date}"


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    event = models.ForeignKey(
        Event,
        related_name='participants',
        on_delete=models.CASCADE
    )

    event_user = models.ForeignKey(
        EventUser,
        on_delete=models.CASCADE,
        related_name='event_user',
        )

    class Meta:
        unique_together = ('event', 'event_user')

    def __str__(self) -> str:
        return f"{self.event}:{self.event_user.username}"


class Vote(models.Model):
    participant = models.ForeignKey(
        Participant,
        related_name='votes',
        on_delete=models.CASCADE
    )

    date_option = models.ForeignKey(
        DateOption,
        related_name='votes',
        on_delete=models.CASCADE
    )

    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('participant', 'date_option')

    def __str__(self) -> str:
        return f"{self.participant.event_user.username}: {self.date_option.date}"


class Message(models.Model):
    event = models.ForeignKey(
        Event,
        related_name='messages',
        on_delete=models.CASCADE
    )

    participant = models.ForeignKey(
        Participant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message in {self.event.title}"
