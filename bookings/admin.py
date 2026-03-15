from django.contrib import admin
from .models import User, Team, Room, Booking

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'gender', 'team']
    list_filter = ['gender', 'age']
    search_fields = ['name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'room_type', 'capacity']
    list_filter = ['room_type']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'slot', 'room', 'user', 'team', 'created_at']
    list_filter = ['slot', 'room__room_type']
    search_fields = ['user__name', 'team__name']
