from django.core.management.base import BaseCommand
from bookings.models import Room

class Command(BaseCommand):
    help = 'Creates default rooms: 8 Private, 4 Conference, 3 Shared Desks'

    def handle(self, *args, **kwargs):
        private_count = 8
        conference_count = 4
        shared_count = 3

        Room.objects.filter().delete()  # Optional: clear existing rooms

        for _ in range(private_count):
            Room.objects.create(room_type='PRIVATE', capacity=1)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {private_count} Private Rooms"))

        for _ in range(conference_count):
            Room.objects.create(room_type='CONFERENCE', capacity=10)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {conference_count} Conference Rooms"))

        for _ in range(shared_count):
            Room.objects.create(room_type='SHARED', capacity=4)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {shared_count} Shared Desks"))

        total = private_count + conference_count + shared_count
        self.stdout.write(self.style.SUCCESS(f"🎉 Successfully created {total} rooms in total"))
