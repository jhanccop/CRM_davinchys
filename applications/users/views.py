from datetime import date, timedelta

from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from applications.users.mixins import AdminPermisoMixin
from django.http import HttpResponseRedirect

from django.views.generic import (
    View,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView
)

from django.views.generic.edit import (
    FormView
)

from .forms import (
    UserRegisterForm, 
    LoginForm,
    UserUpdateForm,
    UpdatePasswordForm,
    DocumentationsForm,
)
#
from .models import (
    User,
    Documentations
)

from applications.actividades.models import DailyTasks
from applications.movimientos.models import Documents
# 

class UserRegisterView(AdminPermisoMixin,FormView):
    template_name = 'users/register_creative.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users_app:user-lista')

    def form_valid(self, form):
        #
        User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            full_name=form.cleaned_data['full_name'],
            last_name=form.cleaned_data['last_name'],
            position=form.cleaned_data['position'],
            #is_active=form.cleaned_data['is_active'],
        )
        # enviar el codigo al email del user
        return super(UserRegisterView, self).form_valid(form)

class LoginUser(FormView):
    #template_name = 'users/login.html'
    template_name = 'users/login_creative.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:index')

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)

class LogoutView(View):

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

class UserUpdateView(AdminPermisoMixin,UpdateView):
    template_name = "users/update_creative.html"
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users_app:user-lista')

class UserDeleteView(AdminPermisoMixin,DeleteView):
    template_name = "users/delete_creative.html"
    model = User
    success_url = reverse_lazy('users_app:user-lista')

class UpdatePasswordView(LoginRequiredMixin, FormView):
    # template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            email=usuario.email,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)

class UserListView(LoginRequiredMixin,ListView):
    template_name = "users/lista_creative.html"
    context_object_name = 'usuarios'

    def get_queryset(self):
        return User.objects.usuarios_sistema()
    
class UserDetailView(ListView):
    template_name = "users/user-detail.html"
    context_object_name = 'worker'

    def get_queryset(self,**kwargs):
        pk = self.kwargs['pk']
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 7)) + " to " + str(date.today())

        payload = {}
        US = User.objects.usuarios_sistema_id(id = int(pk))
        payload["intervalDate"] = intervalDate
        payload["person"] = US
        payload["docs"] = Documentations.objects.docs_por_id(id = int(pk))
        payload["docsFin"] = Documents.objects.DocumentosPorRUC(ruc = US.ruc)
        payload["tasks"] = DailyTasks.objects.MiListarPorIntervaloHorasExtraAcc(user = US, interval = intervalDate)
        return payload
   
class UserDocumentsCreateView(CreateView):
    template_name = "users/user-documento-crear.html"
    model = Documentations
    form_class = DocumentationsForm

    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        return reverse_lazy('users_app:user-detail', kwargs={'pk':pk})
    
    def get_context_data(self, **kwargs):
        context = super(UserDocumentsCreateView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

class UserDocumentsUpdateView(UpdateView):
    template_name = "users/user-documento-editar.html"
    model = Documentations
    form_class = DocumentationsForm

    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        return reverse_lazy('users_app:user-detail', kwargs={'pk':self.object.idUser.id})

class UserDocumentsDeleteView(DeleteView):
    template_name = "users/user-documento-eliminar.html"
    model = Documentations

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('users_app:user-detail', kwargs={'pk':self.object.idUser.id})



