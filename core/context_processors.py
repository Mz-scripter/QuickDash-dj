from users.models import Profile
from django.conf import settings

def global_context(request):
    is_seller = False

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            is_seller = profile.is_seller
        except Profile.DoesNotExist:
            is_seller = False
    
    allowed_emails = getattr(settings, 'ALLOWED_EMAILS', [])

    return {
        'is_seller': is_seller,
        'allowed_emails': allowed_emails,
    }