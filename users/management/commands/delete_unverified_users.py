from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from users.models import Profile


class Command(BaseCommand):
    help = "Delete unverified accounts older than 1 hour"

    def handle(self, *args, **kwargs):
        expiration_time = now() - timedelta(hours=1)
        unverified_profiles = Profile.objects.filter(
            is_verified=False, created_at__lt=expiration_time
        )

        for profile in unverified_profiles:
            self.stdout.write(f"Deleting unverified user: {profile.user.email}")
            profile.user.delete()
            