import uuid
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(models.Model): 
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True) 
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')  # Add role field
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='members')
    password = models.CharField(max_length=128,null=True, blank=True) 

    def __str__(self):
        return self.name

    @property
    def is_admin(self):
        return self.role == 'ADMIN'
    
    @property
    def is_authenticated(self):
        return True



class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('PRIVATE', 'Private Room'),
        ('CONFERENCE', 'Conference Room'),
        ('SHARED', 'Shared Desk'),
    ]

    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.room_type} (ID: {self.id})'


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    slot = models.DateTimeField()  # Booking for specific hourly slot

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='bookings')
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE, related_name='bookings')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'slot')  # Prevent double booking

    def __str__(self):
        return f'Booking {self.id} - Room {self.room.id} @ {self.slot}'
