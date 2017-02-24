from UserApp.models import *
''''''
def token_authentication(token, mobile):
    try:
        user=User.objects.get(user_mobile=mobile)
    except User.DoesNotExists as ex:
        return False

    if token == user.token and mobile == user.user_mobile:
        return True
    else:
        return False