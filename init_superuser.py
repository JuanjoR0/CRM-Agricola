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
    {"username": "Supervisor1", "email": "ana.lopez@agrocontrol.com", "password": "usuario1234", "role": "supervisor"},
    {"username": "Vendedor1", "email": "mario.gomez@agrocontrol.com", "password": "usuario1234", "role": "vendedor"},
    {"username": "Vendedor2", "email": "laura.ramirez@agrocontrol.com", "password": "usuario1234", "role": "vendedor"},
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
empresa_nombres = [
    "AgroCampos S.A.",
    "Frutas del Sur",
    "Olivares Unidos",
    "VidExport",
    "Aceitunas Martínez",
    "Campo Verde S.L.",
    "Trigo del Valle",
    "Mangos Tropicales"
]
empresas = []
for nombre in empresa_nombres:
    empresa, _ = Company.objects.get_or_create(
        name=nombre,
        defaults={
            "description": f"Compañía agrícola especializada en {nombre.split()[0]}",
            "country": "España",
            "phone": f"955 000 0{random.randint(10,99)}",
            "email": f"contacto@{nombre.replace(' ', '').lower()}.com"
        }
    )
    empresas.append(empresa)
    print(f"✅ Empresa creada: {nombre}")

# -------- CLIENTES --------
clientes_info = [
    {"name": "Finca El Paraíso", "type": "agricultor", "region": "Andalucía", "crop": "aguacate", "email": "paraiso@campo.com"},
    {"name": "Cooperativa San Isidro", "type": "cooperativa", "region": "Murcia", "crop": "aceituna", "email": "sanisidro@coop.com"},
    {"name": "Distribuciones Hortícolas", "type": "distribuidor", "region": "Valencia", "crop": "mango", "email": "ventas@hortidis.com"},
    {"name": "Agrícola Sierra Alta", "type": "agricultor", "region": "Extremadura", "crop": "vid", "email": "sierraalta@agro.com"},
    {"name": "Aceitunera del Sur", "type": "distribuidor", "region": "Andalucía", "crop": "aceituna", "email": "info@aceitunasur.com"},
    {"name": "Finca Las Palmeras", "type": "agricultor", "region": "Canarias", "crop": "mango", "email": "palmeras@finca.com"},
    {"name": "Campo y Sol", "type": "cooperativa", "region": "Murcia", "crop": "aguacate", "email": "sol@coopcampo.com"},
    {"name": "AgroLogística S.L.", "type": "distribuidor", "region": "Madrid", "crop": "trigo", "email": "logistica@agro.com"},
    {"name": "Viñedos del Norte", "type": "agricultor", "region": "La Rioja", "crop": "vid", "email": "vinedosnorte@bodega.com"},
    {"name": "Olivares de la Vega", "type": "cooperativa", "region": "Castilla-La Mancha", "crop": "aceituna", "email": "vega@olivares.com"},
]
clientes = []

for data in clientes_info:
    cliente, _ = Client.objects.get_or_create(
        name=data["name"],
        defaults={
            "client_type": data["type"],
            "region": data["region"],
            "main_crop": data["crop"],
            "email": data["email"],
            "phone": f"611 {random.randint(100000, 999999)}",
            "company": random.choice(empresas),
            "assigned_salesperson": random.choice(usuarios_creados),
        }
    )
    clientes.append(cliente)
    print(f"✅ Cliente creado: {data['name']}")

# -------- INTERACCIONES --------
interacciones_info = [
    ("llamada", "Se realizó llamada para confirmar pedido semanal."),
    ("visita", "Visita técnica para inspección de cultivo de mango."),
    ("email", "Envío de cotización para nueva campaña."),
    ("feria", "Contacto inicial en feria agrícola de Zaragoza."),
    ("llamada", "Consulta sobre disponibilidad de productos bio."),
    ("visita", "Evaluación de terreno para posible colaboración."),
    ("email", "Envío de catálogo actualizado."),
    ("otro", "Reunión online para plan estratégico."),
    ("llamada", "Seguimiento post-venta sobre trato recibido."),
    ("visita", "Demostración de productos en finca experimental."),
]

for i, (tipo, nota) in enumerate(interacciones_info):
    Interaction.objects.create(
        client=random.choice(clientes),
        date=make_aware(datetime.now() - timedelta(days=random.randint(1, 30))),
        interaction_type=tipo,
        note=nota,
        user=random.choice(usuarios_creados),
    )
    print(f"✅ Interacción creada: {i + 1}")
