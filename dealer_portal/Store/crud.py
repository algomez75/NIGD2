# tu_aplicacion/crud.py
from crudbuilder.abstract import BaseCrudBuilder
from .models import Dealer, Estimate, EstimateDetail, Order, PriceAdjustment, BasePrice

class DealerCrud(BaseCrudBuilder):
    model = Dealer
    search_fields = ['name', 'email', 'phone']
    tables2_fields = ('name', 'email', 'phone', 'address', 'logotype', 'discount', 'shipping_address', 'method_of_payment', 'terms_and_conditions')

class EstimateCrud(BaseCrudBuilder):
    model = Estimate
    tables2_fields = ('name', 'customer_info', 'created', 'created_by', 'order_number')

class EstimateDetailCrud(BaseCrudBuilder):
    model = EstimateDetail
    tables2_fields = ('mark', 'product', 'serie', 'configuration', 'frame_color', 'glass_type', 'glass_color', 'glass_config', 'glass_coating', 'privacy', 'width', 'height', 'quantity', 'markup', 'square_feet', 'tax_range', 'unit_price', 'total_price')

class OrderCrud(BaseCrudBuilder):
    model = Order
    tables2_fields = ('order_number', 'estimate', 'estimate_detail', 'customer', 'created', 'status', 'changed_by', 'changed_at', 'notes', 'note_history', 'total_price')

class PriceAdjustmentCrud(BaseCrudBuilder):
    model = PriceAdjustment
    tables2_fields = ('name', 'percentage_adjustment', 'estimate_detail')

class BasePriceCrud(BaseCrudBuilder):
    model = BasePrice
    tables2_fields = ('product', 'base_price_per_square_foot')
