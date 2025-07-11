import csv
from django.contrib.auth.decorators import login_required
from .utils import is_superadmin, is_supervisor, is_salesperson
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import ListView,TemplateView
from .models import Client, Company, Product,Interaction
from crm import models
from django.db.models import Count,Q
from django.http import HttpResponseForbidden,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import ClientForm,InteractionForm

@login_required
def home(request):
    return redirect('client-list')

@login_required
def export_clients_csv(request):
    user = request.user

    
    if not user.is_authenticated:
        return HttpResponse("No autenticado", status=401)

    if not (is_superadmin(user) or is_supervisor(user) or is_salesperson(user)):
        return HttpResponse("No autorizado", status=403)

    
    if is_salesperson(user):
        clients = Client.objects.filter(assigned_salesperson=user)
    else:
        clients = Client.objects.all()

    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Tipo de cliente', 'Zona', 'Cultivo principal', 'Email', 'Teléfono', 'Empresa'])

    for client in clients:
        writer.writerow([
            client.name,
            client.get_client_type_display(),
            client.region,
            client.get_main_crop_display(),
            client.email,
            client.phone,
            client.company.name if client.company else '',
        ])

    return response

@login_required
def export_interactions_csv(request):
    user = request.user

    if not (is_superadmin(user) or is_supervisor(user) or is_salesperson(user)):
        return HttpResponse("No autorizado", status=403)

    if is_salesperson(user):
        interactions = Interaction.objects.filter(user=user)
    else:
        interactions = Interaction.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="interacciones.csv"'

    writer = csv.writer(response)
    writer.writerow(['Cliente', 'Fecha', 'Tipo', 'Nota', 'Vendedor'])

    for i in interactions:
        writer.writerow([
            i.client.name if i.client else '',
            i.date,
            i.get_interaction_type_display(),
            i.note,
            i.user.username,
        ])

    return response

class StatisticsView(TemplateView):
    template_name = 'crm/statistics.html'

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user)):
            return HttpResponseForbidden("No tienes acceso a las estadísticas.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        interaction_type_labels = dict(Interaction.INTERACTION_TYPE_CHOICES)
        client_type_labels = dict(Client.CLIENT_TYPE_CHOICES)
        crop_labels = dict(Client.CROPS)

        
        context['total_clients'] = Client.objects.count()
        context['total_interactions'] = Interaction.objects.count()

        
        raw_clients_by_type = (
            Client.objects
            .values('client_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        context['clients_by_type'] = [
            {
                'client_type': client_type_labels.get(item['client_type'], item['client_type']),
                'count': item['count']
            }
            for item in raw_clients_by_type
        ]

       
        raw_clients_by_crop = (
            Client.objects
            .values('main_crop')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        context['clients_by_crop'] = [
            {
                'main_crop': crop_labels.get(item['main_crop'], item['main_crop']),
                'count': item['count']
            }
            for item in raw_clients_by_crop
        ]

        
        raw_interactions_by_type = (
            Interaction.objects
            .values('interaction_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        context['interactions_by_type'] = [
            {
                'interaction_type': interaction_type_labels.get(item['interaction_type'], item['interaction_type']),
                'count': item['count']
            }
            for item in raw_interactions_by_type
        ]

        
        context['interactions_by_user'] = (
            Interaction.objects
            .values('user__username')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return context

class InteractionListView(LoginRequiredMixin, ListView):
    model = Interaction
    template_name = 'crm/interaction_list.html'
    context_object_name = 'interactions'

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('q')
        
       
        if is_superadmin(user) or is_supervisor(user):
            qs = Interaction.objects.all()
        elif is_salesperson(user):
            qs = Interaction.objects.filter(
                Q(user=user) | Q(client__assigned_salesperson=user)
            )
        else:
            return Interaction.objects.none()

       
        if query:
            qs = qs.filter(
                Q(client__name__icontains=query) |
                Q(note__icontains=query) |
                Q(interaction_type__icontains=query)
            )

        return qs

class InteractionCreateView(LoginRequiredMixin, CreateView):
    model = Interaction
    fields = ['client', 'date', 'interaction_type', 'note']
    template_name = 'crm/interaction_form.html'
    success_url = '/interacciones/'

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user) or is_salesperson(request.user)):
            return HttpResponseForbidden("No tienes permiso para crear interacciones.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        
        if is_salesperson(self.request.user):
            form.fields['client'].queryset = Client.objects.filter(assigned_salesperson=self.request.user)

        return form

    def form_valid(self, form):
       
        form.instance.user = form.cleaned_data['client'].assigned_salesperson
        return super().form_valid(form)

    
class InteractionUpdateView(LoginRequiredMixin, UpdateView):
    model = Interaction
    fields = ['client', 'date', 'interaction_type', 'note']
    template_name = 'crm/interaction_form.html'
    success_url = '/interacciones/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if is_salesperson(request.user) and obj.user != request.user:
            return HttpResponseForbidden("Solo puedes editar tus propias interacciones.")
        if not (is_superadmin(request.user) or is_supervisor(request.user) or is_salesperson(request.user)):
            return HttpResponseForbidden("No tienes permiso para editar.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = self.get_object()

        
        if is_superadmin(self.request.user) or is_supervisor(self.request.user):
            form.fields['client'].queryset = Client.objects.filter(assigned_salesperson=obj.user)
        elif is_salesperson(self.request.user):
            form.fields['client'].queryset = Client.objects.filter(assigned_salesperson=self.request.user)

        return form

    def form_valid(self, form):
       
        form.instance.user = form.cleaned_data['client'].assigned_salesperson
        return super().form_valid(form)


class InteractionDeleteView(LoginRequiredMixin,DeleteView):
    model = Interaction
    template_name = 'crm/interaction_confirm_delete.html'
    success_url = '/interacciones/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if is_salesperson(request.user) and obj.user != request.user:
            return HttpResponseForbidden("No puedes eliminar interacciones que no son tuyas.")
        if not (is_superadmin(request.user) or is_supervisor(request.user) or is_salesperson(request.user)):
            return HttpResponseForbidden("No tienes permiso.")
        return super().dispatch(request, *args, **kwargs)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'crm/product_list.html'
    context_object_name = 'products'

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user)):
            return HttpResponseForbidden("No tienes permiso para ver productos.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Product.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(category__icontains=q)
            )
        return queryset

class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['name', 'category', 'unit_of_measurement']
    template_name = 'crm/product_form.html'
    success_url = '/productos/'

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user)):
            return HttpResponseForbidden("No puedes crear productos.")
        return super().dispatch(request, *args, **kwargs)

class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    fields = ['name', 'category', 'unit_of_measurement']
    template_name = 'crm/product_form.html'
    success_url = '/productos/'

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user)):
            return HttpResponseForbidden("No puedes editar productos.")
        return super().dispatch(request, *args, **kwargs)

class ProductDeleteView(LoginRequiredMixin,DeleteView):
    model = Product
    template_name = 'crm/product_confirm_delete.html'
    success_url = '/productos/'

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user)):
            return HttpResponseForbidden("No puedes eliminar productos.")
        return super().dispatch(request, *args, **kwargs)
    

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'crm/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('q')

        
        if is_superadmin(user) or is_supervisor(user):
            qs = Client.objects.all()
        elif is_salesperson(user):
            qs = Client.objects.filter(assigned_salesperson=user)
        else:
            return Client.objects.none()

        
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(company__name__icontains=query)
            )

        return qs
    
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    success_url = '/clientes/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs

    def form_valid(self, form):
        if is_salesperson(self.request.user):
            form.instance.assigned_salesperson = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user) or is_salesperson(request.user)):
            return HttpResponseForbidden("No tienes permiso para crear clientes.")
        return super().dispatch(request, *args, **kwargs)
    
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    success_url = '/clientes/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs

    
class ClientDeleteView(LoginRequiredMixin,DeleteView):
    model = Client
    template_name = 'crm/client_confirm_delete.html'
    success_url = '/clientes/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if is_salesperson(request.user) and obj.assigned_salesperson != request.user:
            return HttpResponseForbidden("No puedes eliminar clientes que no son tuyos.")
        if not (is_superadmin(request.user) or is_supervisor(request.user) or is_salesperson(request.user)):
            return HttpResponseForbidden("No tienes permiso para eliminar clientes.")
        return super().dispatch(request, *args, **kwargs)
    

class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'crm/company_list.html'
    context_object_name = 'companies'

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user)):
            return HttpResponseForbidden("No tienes permiso para ver empresas.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = Company.objects.all()

        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(country__icontains=query)
            )

        return qs

class CompanyCreateView(LoginRequiredMixin,CreateView):
    model = Company
    fields = ['name', 'description', 'country', 'email', 'phone']
    template_name = 'crm/company_form.html'
    success_url = '/empresas/'

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user)):
            return HttpResponseForbidden("No tienes permiso para crear empresas.")
        return super().dispatch(request, *args, **kwargs)

class CompanyUpdateView(LoginRequiredMixin,UpdateView):
    model = Company
    fields = ['name', 'description', 'country', 'email', 'phone']
    template_name = 'crm/company_form.html'
    success_url = '/empresas/'

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user)):
            return HttpResponseForbidden("No puedes editar esta empresa.")
        return super().dispatch(request, *args, **kwargs)

class CompanyDeleteView(LoginRequiredMixin,DeleteView):
    model = Company
    template_name = 'crm/company_confirm_delete.html'
    success_url = '/empresas/'

    def dispatch(self, request, *args, **kwargs):
        if not (is_superadmin(request.user) or is_supervisor(request.user)):
            return HttpResponseForbidden("No puedes eliminar empresas.")
        return super().dispatch(request, *args, **kwargs)