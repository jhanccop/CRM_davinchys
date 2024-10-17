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
        'quote-with-us/', 
        views.QuoteView.as_view(),
        name='quote-with-us',
    ),
    path(
        'panel/', 
        views.PanelHomeView.as_view(),
        name='index',
    ),
    
]