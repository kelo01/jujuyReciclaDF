from django import forms
from usuario_dashboard.models import * 

class RegistroReciclajeForm(forms.ModelForm):
    class Meta:
        model = RegistroReciclaje
        fields = ['modulo', 'material', 'cantidad']
        widgets = {
            'modulo': forms.Select(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }



class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre', 'puntos_por_kg']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'puntos_por_kg': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ['nombre', 'ubicacion', 'capacidad_total', 'capacidad_actual']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'capacidad_actual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }