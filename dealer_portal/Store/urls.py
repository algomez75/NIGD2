# tu_aplicacion/urls.py
from django.urls import path
from .views import DealerCrudView, HomeView, ProductCrudView, EstimateCrudView, EstimateDetailCrudView, OrderCrudView, PriceAdjustmentCrudView, BasePriceCrudView
from .views import SignUpView, LoginView, LogoutView, ProfileView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    path('dealers/', DealerCrudView.as_view(), name='dealer_crud'),
    path('products/', ProductCrudView.as_view(), name='product_crud'),
    path('estimates/', EstimateCrudView.as_view(), name='estimate_crud'),
    path('estimate-details/', EstimateDetailCrudView.as_view(), name='estimate_detail_crud'),
    path('orders/', OrderCrudView.as_view(), name='order_crud'),
    path('price-adjustments/', PriceAdjustmentCrudView.as_view(), name='price_adjustment_crud'),
    path('base-prices/', BasePriceCrudView.as_view(), name='base_price_crud'),
    # Agrega URL adicionales según sea necesario para las otras entidades
]
