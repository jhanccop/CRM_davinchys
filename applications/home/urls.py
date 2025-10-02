#
from django.urls import path
from . import views

app_name = "home_app"

urlpatterns = [
    path('',views.HomeView.as_view()),
    path(
        'home/', 
        views.HomeView.as_view(),
        name='home',
    ),
    path(
        'unauthorized-page/', 
        views.unauthorizedView.as_view(),
        name='unauthorized',
    ),
    path(
        'panel/', 
        views.PanelHomeView.as_view(),
        name='index',
    ),
    # ==================== MYSPACE ====================
    path(
        'mi-espacio/',
        views.myEspaceView.as_view(),
        name='bienvenida'),

    # ==================== QUOTE TEST ====================
    path(
        'quote-with-us/', 
        views.QuoteView.as_view(),
        name='quote-with-us',
    ),

    # ==================== tracking ====================
    path(
        'enter-tracking-number/', 
        views.EnterTrackingNumberView.as_view(),
        name='enter-tracking-number',
    ),
    path(
        'list-tracking-number/', 
        views.TrackingListView.as_view(),
        name='list-tracking-number',
    ),
    path(
        'add-tracking-number/', 
        views.TrackingCreateView.as_view(),
        name='add-tracking-number',
    ),
    path(
        'edit-tracking-number/<pk>/', 
        views.TrackingEditView.as_view(),
        name='edit-tracking-number',
    ),
    path(
        'delete-tracking-number/<pk>/', 
        views.TrackingDeleteView.as_view(),
        name='delete-tracking-number',
    ),
    
]