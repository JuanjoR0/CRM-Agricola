from django.contrib import admin

from django.contrib import admin
from .models import Company, Client, Interaction, Product

from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'country', 'created_at', 'updated_at', 'phone','email')
    search_fields = ('name', 'country', 'email')
    list_filter = ('country',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_type', 'region', 'main_crop', 'email', 'phone', 'company','assigned_salesperson','created_at', 'updated_at',)
    search_fields = ('name', 'email', 'region', 'main_crop')
    list_filter = ('client_type', 'main_crop', 'region')
    raw_id_fields = ('company', 'assigned_salesperson')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'interaction_type', 'note', 'user')
    search_fields = ('client__name', 'interaction_type', 'note')
    list_filter = ('interaction_type', 'date')
    date_hierarchy = ('date')

@admin.register(Product)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category','created_at','updated_at','unit_of_measurement')
    search_fields = ('name', 'category')
    readonly_fields = ('created_at', 'updated_at')



