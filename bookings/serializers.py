from rest_framework import serializers
from .models import User, Room, Booking, Team
from django.utils import timezone
from django.db.models import Count, Q

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'gender']


class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'members']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_type', 'capacity']


class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    user = UserSerializer()
    team = TeamSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'slot', 'room', 'user', 'team', 'created_at']


# -------------------------------
# Create Booking Input Serializer
# -------------------------------
class CreateBookingSerializer(serializers.Serializer):
    slot = serializers.DateTimeField()
    user_id = serializers.IntegerField(required=False)
    team_id = serializers.IntegerField(required=False)
    room_type = serializers.ChoiceField(choices=['PRIVATE', 'CONFERENCE', 'SHARED'])

    def validate(self, data):
        slot = data['slot']
        room_type = data['room_type']
        user_id = data.get('user_id')
        team_id = data.get('team_id')

        # Ensure only one of user_id or team_id is provided
        if bool(user_id) == bool(team_id):
            raise serializers.ValidationError("Specify either user_id or team_id (not both or neither).")

        # Ensure slot is between 9 AM to 6 PM
        if slot.hour < 9 or slot.hour >= 18:
            raise serializers.ValidationError("Slot must be between 9 AM and 6 PM.")

        # Ensure user/team doesn’t already have a booking for the slot
        existing = Booking.objects.filter(slot=slot)
        if user_id and existing.filter(user_id=user_id).exists():
            raise serializers.ValidationError("User already has a booking for this slot.")
        if team_id and existing.filter(team_id=team_id).exists():
            raise serializers.ValidationError("Team already has a booking for this slot.")

        # Conference room needs 3+ people (excluding children < 10)
        if room_type == 'CONFERENCE':
            team = Team.objects.prefetch_related('members').get(id=team_id)
            members = team.members.all()
            headcount = sum(1 for m in members if m.age >= 10)
            if headcount < 3:
                raise serializers.ValidationError("Conference rooms require a team with at least 3 members (age >= 10).")

        return data
