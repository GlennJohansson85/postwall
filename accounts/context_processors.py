from .models import Profile


def profile_context(request):
    profile_picture_url = None
    if request.user.is_authenticated:
        try:
            profile_picture_url = request.user.profile_picture.url if request.user.profile_picture else None
        except Profile.DoesNotExist:
            pass
    return {'profile_picture_url': profile_picture_url}
