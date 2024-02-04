from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... otras URLs
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Nota: puedes necesitar crear un template 'login.html' para el login si aún no lo tienes.
]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.initial_page, name='initial_page'),
]
