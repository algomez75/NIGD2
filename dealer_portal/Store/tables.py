# tu_aplicacion/tables.py
from crudbuilder.tables import BaseTable, Column

class DealerTable(BaseTable):
    name = Column('Name')
    email = Column('Email')
    phone = Column('Phone')
    address = Column('Address')
    logotype = Column('Logotype')

class ProductTable(BaseTable):
    name = Column('Name')
    brand = Column('Brand')
    
class BrandTable(BaseTable):
    name = Column('Name')
    terms_and_conditions = Column('Terms and conditions')
    
class EstimateTable(BaseTable):
    name = Column('Name')
    customer_info = Column('Customer info')
    created = Column('Created')
    created_by = Column('Created by')
    order_number = Column('Order number')
    
class EstimateDetailTable(BaseTable):
    estimate = Column('Estimate')
    product = Column('Product')
    price = Column('Price')
    quantity = Column('Quantity')
    total_price = Column('Total price')
    
class OrderTable(BaseTable):
    order_number = Column('Order number')
    estimate = Column('Estimate')
    estimate_detail = Column('Estimate detail')
    customer = Column('Customer')
    created = Column('Created')
    status = Column('Status')
    changed_by = Column('Changed by')
    changed_at = Column('Changed at')
    notes = Column('Notes')
    note_history = Column('Note history')
    total_price = Column('Total price')
    
class PriceAdjustmentTable(BaseTable):
    product = Column('Product')
    percentage_adjustment = Column('Percentage adjustment')
    content_type = Column('Content type')
    object_id = Column('Object id')
    # Otros campos adicionales
    
class BasePriceTable(BaseTable):
    product = Column('Product')
    base_price_per_square_foot = Column('Base price per square foot')
    content_type = Column('Content type')
    object_id = Column('Object id')
    # Otros campos adicionales
    

# Agrega tablas adicionales según sea necesario para las otras entidades
