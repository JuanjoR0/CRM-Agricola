def is_superadmin(user):
    return user.is_superuser or (hasattr(user, 'userprofile') and user.userprofile.role == 'superadmin')

def is_supervisor(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'supervisor'

def is_salesperson(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'vendedor'
