from django.contrib.auth import get_user_model

def authenticate(user=None, passwd=None, *args, **kwargs):
    USER_MODEL = get_user_model()
    try:
        get_learner_users = USER_MODEL.objects.filter(roles=4)
        get_user = get_learner_users.get(username=user)
    except USER_MODEL.DoesNotExist:
        return None
    except:
        return None
    else:
        if get_user.check_password(passwd):
            return get_user
    return None
