from django.contrib.auth import get_user_model
from crm.models import UserProfile

User = get_user_model()

username = "Juanjo"
email = "juanjorodriguez682@gmail.com"
password = "usuario1234"

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        "email": email,
    }
)

if created:
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("✅ Superusuario creado: Juanjo / usuario1234")
else:
    print("ℹ️ El superusuario ya existía.")

# Crear UserProfile si no existe
if not hasattr(user, 'userprofile'):
    UserProfile.objects.create(user=user, role='superadmin')
    print("✅ Perfil de usuario creado con rol: superadmin")
else:
    print(f"ℹ️ El perfil de usuario ya existía con rol: {user.userprofile.role}")
