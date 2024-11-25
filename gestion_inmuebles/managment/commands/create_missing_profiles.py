from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gestion_inmuebles.models import Profile


class Command(BaseCommand):
    help = "Creates missing user profiles"

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(profile__isnull=True)
        for user in users_without_profile:
            Profile.objects.create(user=user)
            self.stdout.write(
                self.style.SUCCESS(f"Created profile for user: {user.username}")
            )

        self.stdout.write(self.style.SUCCESS("Successfully created missing profiles"))
