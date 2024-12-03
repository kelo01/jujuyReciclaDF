from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UsuarioComun
from django.contrib.auth.forms import PasswordChangeForm

class UsuarioPerfilForm(forms.ModelForm):
    class Meta:
        model = UsuarioComun
        fields = ['username', 'email', 'dni', 'telefono', 'direccion', 'edad']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    dni = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI'})
    )
    telefono = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'})
    )
    direccion = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'})
    )
    edad = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad'})
    )
    rol = forms.ChoiceField(
        choices=UsuarioComun.ROL_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    zona_asignada = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zona asignada'})
    )
    
    class Meta:
        model = UsuarioComun
        fields = ['username', 'email', 'password1', 'password2', 'dni', 'telefono', 'direccion', 'edad', 'rol', 'zona_asignada']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad and edad < 18:
            raise forms.ValidationError("Debe tener al menos 18 años para registrarse.")
        return edad

    def clean_zona_asignada(self):
        rol = self.cleaned_data.get('rol')
        zona_asignada = self.cleaned_data.get('zona_asignada')
        if rol == 'agente' and not zona_asignada:
            raise forms.ValidationError("La zona asignada es obligatoria para los agentes.")
        return zona_asignada

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden.")

        return cleaned_data