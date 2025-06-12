from django.core.management.base import BaseCommand
from django.db import transaction
from bookings.models import User, Team, Room

class Command(BaseCommand):
    help = 'Create default users (admin and regular user)'


    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Create default team
                team, team_created = Team.objects.get_or_create(
                    name="Development Team"
                )
                
                if team_created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created team: {team.name}')
                    )
                else:
                    self.stdout.write(f'Team "{team.name}" already exists')

                # Create admin user
                admin_user, admin_created = User.objects.get_or_create(
                    email="admin@example.com",
                    defaults={
                        'name': 'Admin User',
                        'age': 30,
                        'gender': 'Other',
                        'role': 'ADMIN',
                        'team': team,
                        'password': 'admin123'
                    }
                )
                
                if admin_created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created admin user: {admin_user.email}')
                    )
                else:
                    self.stdout.write(f'Admin user "{admin_user.email}" already exists')

                # Create regular user
                regular_user, user_created = User.objects.get_or_create(
                    email="user@example.com",
                    defaults={
                        'name': 'Regular User',
                        'age': 25,
                        'gender': 'Male',
                        'role': 'USER',
                        'team': team,
                        'password': 'user123'
                    }
                )
                
                if user_created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created regular user: {regular_user.email}')
                    )
                else:
                    self.stdout.write(f'Regular user "{regular_user.email}" already exists')


        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating default users: {str(e)}')
            )