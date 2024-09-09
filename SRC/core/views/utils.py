def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_doctor(user):
    return user.is_authenticated and hasattr(user, 'is_doctor') and user.is_doctor