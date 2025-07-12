import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model
from crm.models import UserProfile, Product, Company, Client, Interaction

User = get_user_model()

# -------- SUPERADMIN JUANJO --------
username = "Juanjo"
email = "juanjorodriguez682@gmail.com"
password = "usuario1234"

user, created = User.objects.get_or_create(
    username=username,
    defaults={"email": email},
)

if created:
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("✅ Superusuario creado: Juanjo / usuario1234")
else:
    print("ℹ️ El superusuario ya existía.")

if not hasattr(user, 'userprofile'):
    UserProfile.objects.create(user=user, role='superadmin')
    print("✅ Perfil de usuario creado con rol: superadmin")
else:
    print(f"ℹ️ El perfil de usuario ya existía con rol: {user.userprofile.role}")

# -------- OTROS USUARIOS --------
usuarios = [
    {"username": "Supervisor1", "email": "supervisor1@example.com", "password": "supervisor123", "role": "supervisor"},
    {"username": "Vendedor1", "email": "vendedor1@example.com", "password": "vendedor123", "role": "vendedor"},
    {"username": "Vendedor2", "email": "vendedor2@example.com", "password": "vendedor123", "role": "vendedor"},
]

usuarios_creados = []

for u in usuarios:
    user, creado = User.objects.get_or_create(username=u["username"], defaults={"email": u["email"]})
    if creado:
        user.set_password(u["password"])
        user.save()
        print(f"✅ Usuario creado: {user.username}")
    else:
        print(f"ℹ️ Usuario ya existía: {user.username}")
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user, role=u["role"])
        print(f"✅ Perfil creado con rol: {u['role']}")
    usuarios_creados.append(user)

# -------- PRODUCTOS (FRUTAS) --------
frutas = ["Aguacate", "Uva", "Trigo", "Aceituna", "Mango"]
for fruta in frutas:
    obj, creado = Product.objects.get_or_create(name=fruta, defaults={
        "category": "Fruta",
        "unit_of_measurement": "kg"
    })
    if creado:
        print(f"✅ Producto creado: {fruta}")
    else:
        print(f"ℹ️ Producto ya existía: {fruta}")

# -------- EMPRESAS --------
empresas = []
for i in range(1, 9):
    empresa, _ = Company.objects.get_or_create(
        name=f"Empresa {i}",
        defaults={
            "description": f"Descripción de Empresa {i}",
            "country": "España",
            "phone": f"+34 600 000 00{i}",
            "email": f"empresa{i}@correo.com"
        }
    )
    empresas.append(empresa)
    print(f"✅ Empresa creada: Empresa {i}")

# -------- CLIENTES --------
cliente_tipos = ['agricultor', 'cooperativa', 'distribuidor']
cultivos = ['mango', 'aceituna', 'vid', 'aguacate', 'otro']
clientes = []

for i in range(1, 11):
    cliente, _ = Client.objects.get_or_create(
        name=f"Cliente {i}",
        defaults={
            "client_type": random.choice(cliente_tipos),
            "region": f"Región {i}",
            "main_crop": random.choice(cultivos),
            "email": f"cliente{i}@correo.com",
            "phone": f"+34 611 111 11{i}",
            "company": random.choice(empresas),
            "assigned_salesperson": random.choice(usuarios_creados),
        }
    )
    clientes.append(cliente)
    print(f"✅ Cliente creado: Cliente {i}")

# -------- INTERACCIONES --------
interaccion_tipos = ['llamada', 'visita', 'email', 'feria', 'otro']

for i in range(10):
    Interaction.objects.create(
        client=random.choice(clientes),
        date=make_aware(datetime.now() - timedelta(days=random.randint(1, 30))),
        interaction_type=random.choice(interaccion_tipos),
        note=f"Interacción número {i+1}",
        user=random.choice(usuarios_creados),
    )
    print(f"✅ Interacción creada: {i+1}")
