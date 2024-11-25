from background_task import background
from datetime import timedelta
import logging


logger = logging.getLogger(__name__)

@background(schedule=timedelta(seconds=10))  # Adjust the schedule to your needs
def delete_unverified_users():
    from users.models import User, Profile
    from django.utils import timezone

    logger.info("Running delete_unverified_users task...")
    time_limit = timezone.now() - timedelta(hours=1)
    unverified_users = User.objects.filter(profile__is_verified=False, profile__created_at__lte=time_limit)
    
    deleted_count, _ = unverified_users.delete()
    print(f"{deleted_count} unverified users deleted.")