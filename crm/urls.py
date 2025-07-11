from django.urls import path
from . import views
from .views import (
    ClientListView,ClientCreateView,ClientUpdateView,ClientDeleteView,
    InteractionListView,InteractionCreateView,InteractionUpdateView,InteractionDeleteView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    CompanyListView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView,
    StatisticsView,export_clients_csv
)

urlpatterns = [
    path('', views.home, name='home'),

    path('clientes/', ClientListView.as_view(), name='client-list'),
    path('clientes/nuevo/', ClientCreateView.as_view(), name='client-create'),
    path('clientes/<int:pk>/editar/', ClientUpdateView.as_view(), name='client-update'),
    path('clientes/<int:pk>/eliminar/', ClientDeleteView.as_view(), name='client-delete'),
    path('interacciones/', InteractionListView.as_view(), name='interaction-list'),
    path('interacciones/nueva/', InteractionCreateView.as_view(), name='interaction-create'),
    path('interacciones/<int:pk>/editar/', InteractionUpdateView.as_view(), name='interaction-update'),
    path('interacciones/<int:pk>/eliminar/', InteractionDeleteView.as_view(), name='interaction-delete'),
    path('productos/', ProductListView.as_view(), name='product-list'),
    path('productos/nuevo/', ProductCreateView.as_view(), name='product-create'),
    path('productos/<int:pk>/editar/', ProductUpdateView.as_view(), name='product-update'),
    path('productos/<int:pk>/eliminar/', ProductDeleteView.as_view(), name='product-delete'),
    path('empresas/', CompanyListView.as_view(), name='company-list'),
    path('empresas/nueva/', CompanyCreateView.as_view(), name='company-create'),
    path('empresas/<int:pk>/editar/', CompanyUpdateView.as_view(), name='company-update'),
    path('empresas/<int:pk>/eliminar/', CompanyDeleteView.as_view(), name='company-delete'),

    path('estadisticas/', StatisticsView.as_view(), name='statistics'),
    path('clientes/exportar/', export_clients_csv, name='export-csv'),
    path('exportar-interacciones/', views.export_interactions_csv, name='export-interactions-csv'),
]