from account.models import CustomUser
from account.models import Profile


def user_image(request):
    users = CustomUser.objects.get(id=1)
    user_profile = Profile.objects.get(user_id=users)
    return {"object_user": user_profile}
