from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Client(models.Model):
    CLIENT_TYPE_CHOICES = [
        ('agricultor', 'Agricultor'),
        ('cooperativa', 'Cooperativa'),
        ('distribuidor', 'Distribuidor'),
    ]

    CROPS = [
        ('mango', 'Mango'),
        ('aceituna', 'Aceituna'),
        ('vid', 'Vid'),
        ('aguacate', 'Aguacate'),
        ('otro', 'Otro'),
    ]

    name = models.CharField(max_length=100)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES)
    region = models.CharField(max_length=100)
    main_crop = models.CharField(max_length=50, choices=CROPS)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_salesperson = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Interaction(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ('llamada', 'Llamada'),
        ('visita', 'Visita'),
        ('email', 'Email'),
        ('feria', 'Feria Agricola'),
        ('otro', 'Otro'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE_CHOICES)
    note = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return f"{self.interaction_type} with {self.client.name} on {self.date}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unit_of_measurement = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('superadmin', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('vendedor', 'Vendedor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"