from .models import Profile

def profile_picture(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return {'profile_picture': profile.foto, 'position': profile.position}
        except Profile.DoesNotExist:
            return {}
    else:
        return {}