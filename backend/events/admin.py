from django.contrib import admin
from .models import Event, DateOption, EventUser, Participant, Vote, Message


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)


@admin.register(DateOption)
class DateOprionAdmin(admin.ModelAdmin):
    list_display = ('event', 'date')
    list_filter = ('event',)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('event_user', 'event')
    list_filter = ('event',)


@admin.register(EventUser)
class EventUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username',)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('participant', 'date_option', 'voted_at')
    list_filter = ('date_option',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('event', 'participant', 'created_at')
    list_filter = ('event',)
