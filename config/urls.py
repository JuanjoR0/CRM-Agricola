from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from crm.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('crm.urls')),
    path('', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
