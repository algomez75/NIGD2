# tu_aplicacion/views.py
from crudbuilder.views import BaseCrudView
from .models import BasePrice, Dealer, Estimate, EstimateDetail, Order, PriceAdjustment, Product
from .tables import BasePriceTable, DealerTable, EstimateDetailTable, EstimateTable, OrderTable, PriceAdjustmentTable, ProductTable
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

##########################3users Views##########################
class HomeView(TemplateView):
    template_name = 'home.html'

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'

class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('login')

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'registration/profile.html'

#############################Dealers Views#############################
class DealerCrudView(BaseCrudView):
    model = Dealer
    table = DealerTable

#################################Products Views############################
class ProductCrudView(BaseCrudView):
    model = Product
    table = ProductTable

# Agrega vistas adicionales según sea necesario para las otras entidades
######################################Estimates Views############################

class EstimateCrudView(BaseCrudView):
    model = Estimate
    table = EstimateTable
    
# Agrega vistas adicionales según sea necesario para las otras entidades

class EstimateDetailCrudView(BaseCrudView):
    model = EstimateDetail
    table = EstimateDetailTable
    
class BasePriceCrudView(BaseCrudView):
    model = BasePrice
    table = BasePriceTable

class OrderCrudView(BaseCrudView):
    model = Order
    table = OrderTable
    
class PriceAdjustmentCrudView(BaseCrudView):
    model = PriceAdjustment
    table = PriceAdjustmentTable