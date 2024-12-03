from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import RegistroForm,LoginForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from .models import UsuarioComun
from .forms import UsuarioPerfilForm, CustomPasswordChangeForm


class RegistroView(View):
    def get(self, request):
        form = RegistroForm()
        return render(request, 'core/registro.html', {'form': form})

    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            if user.rol == 'agente':
                return redirect('inicio_agente')
            else:
                return redirect('inicio_usuario')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
        return render(request, 'core/registro.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'core/login.html', {'form': form})

    def post(self, request):
        user_type = request.POST.get('user_type', 'usuario')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.rol != user_type:
                form.add_error(None, 'El tipo de usuario seleccionado no coincide con tu cuenta. Por favor, selecciona el tipo de usuario correcto.')
                return render(request, 'core/login.html', {'form': form})
            
            login(request, user)
            if user.rol == 'agente':
                return redirect('inicio_agente')
            else:
                return redirect('inicio_usuario')
        return render(request, 'core/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, '¡Has cerrado sesión exitosamente!')
        return redirect('login')




class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = UsuarioComun
    form_class = UsuarioPerfilForm
    template_name = 'usuario_dashboard/editar_perfil.html'
    success_url = reverse_lazy('editar_perfil_user')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)

class ConfiguracionView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'usuario_dashboard/configuracion.html'
    success_url = reverse_lazy('configuracion_user')

    def form_valid(self, form):
        messages.success(self.request, 'Contraseña cambiada correctamente.')
        return super().form_valid(form)


class EditarPerfilAgenteView(LoginRequiredMixin, UpdateView):
    model = UsuarioComun
    form_class = UsuarioPerfilForm
    template_name = 'agente_dashboard/editar_perfil.html'
    success_url = reverse_lazy('editar_perfil_agente')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)

class ConfiguracionAgenteView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'agente_dashboard/configuracion.html'
    success_url = reverse_lazy('configuracion_agente')

    def form_valid(self, form):
        messages.success(self.request, 'Contraseña cambiada correctamente.')
        return super().form_valid(form)

