
from django import forms
from .models import Client
from django.contrib.auth.models import User
from .models import Interaction

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'client_type', 'region', 'main_crop', 'email', 'phone', 'company', 'assigned_salesperson']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)

        if user and user.userprofile.role == 'vendedor':
            self.fields.pop('assigned_salesperson')  
        else:
            
            self.fields['assigned_salesperson'].queryset = User.objects.filter(userprofile__role='vendedor')

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['client', 'interaction_type', 'date', 'note']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        
        if user and hasattr(user, 'userprofile') and user.userprofile.role == 'vendedor':
            self.fields['client'].queryset = Client.objects.filter(assigned_salesperson=user)