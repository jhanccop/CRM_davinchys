#
from django.urls import path

from . import views

app_name = "users_app"

urlpatterns = [
    path(
        'user/login/', 
        views.LoginUser.as_view(),
        name='user-login',
    ),
    path(
        'users/register/', 
        views.UserRegisterView.as_view(),
        name='user-register',
    ),
    path(
        'users/logout/', 
        views.LogoutView.as_view(),
        name='user-logout',
    ),
    path(
        'users/update-password/<pk>/', 
        views.UpdatePasswordView.as_view(),
        name='user-update_password',
    ),
    path(
        'users/update/<pk>/', 
        views.UserUpdateView.as_view(),
        name='user-update',
    ),
    path(
        'users/delete/<pk>/', 
        views.UserDeleteView.as_view(),
        name='user-delete',
    ),
    path(
        'users/lista/', 
        views.UserListView.as_view(),
        name='user-lista',
    ),
    path(
        'users/detail/<pk>/', 
        views.UserDetailView.as_view(),
        name='user-detail',
    ),
    path(
        'users/documentos-crear/<pk>/', 
        views.UserDocumentsCreateView.as_view(),
        name='user-documento-crear',
    ),
    path(
        'users/documentos-editar/<pk>/', 
        views.UserDocumentsUpdateView.as_view(),
        name='user-documentos-editar',
    ),
    path(
        'users/documentos-eliminar/<pk>/', 
        views.UserDocumentsDeleteView.as_view(),
        name='user-documentos-eliminar',
    ),
]