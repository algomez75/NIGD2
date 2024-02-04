from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.validators import EmailValidator, RegexValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


#############################Dealers Models#############################
def validate_image_size(value):
    if value.size > 512 * 1024:  # 512KB
        raise ValidationError(_('Image file too large ( > 512KB )'))


def validate_image_extension(value):
    if not value.name.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise ValidationError(
            _('Invalid image format. Only JPEG and PNG are allowed.'))
class Dealer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # Nombre de la empresa
    
    number = models.IntegerField(unique=True, editable=False)

    @staticmethod
    def generate_number():
        last = Dealer.objects.all().order_by('number').last()
        if last:
            return last.number + 1
        return 1010

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_number()
        super(Dealer, self).save(*args, **kwargs)
        
    email = models.EmailField(
        unique=True, null=True, blank=True,  # Garantiza unicidad
        validators=[
            EmailValidator(_('Enter a valid email address.')),  # Validación estándar de formato de correo electrónico
            # Puedes agregar validaciones adicionales si lo deseas, como comprobar el dominio del correo electrónico, etc.
        ]
    )
    phone = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message=_("Enter a valid phone number. Up to 15 digits allowed.")
        )
    ])
    address = models.CharField(max_length=100)
    logotype = models.ImageField(upload_to='dealer_logos/', null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text=_("Discount percentage for the dealer"))
    shipping_address = models.CharField(max_length=100, blank=True, verbose_name='Shipping address')
    method_of_payment = models.CharField(max_length=100, choices=[('debit', 'Debit card'), ('credit', 'Credit card'), ('cash', 'Cash on delivery')], default='debit')
    terms_and_conditions = models.BooleanField(default=False, verbose_name='Terms and conditions')
    # Otros campos adicionales
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    

    
    
################################################Models de marcas#####################################################

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    terms_and_conditions = models.FileField(upload_to='terms_and_conditions', blank=True)
    
    def __str__(self):
        return self.name
    # Otros campos adicionales

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    # Añade más campos según sea necesario para las opciones del producto

    def __str__(self):
        return self.name
    
class Serie(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='series')
    serie = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.serie
    
class Configuration(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='configurations')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='configurations')
    configuration = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.configuration
    
class FrameColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='frame_colors')
    frame_color = models.CharField(max_length=255)
    additional_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return self.frame_color
    
class GlassType(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='glass_types')
    glass_type = models.CharField(max_length=255)
    additional_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return self.glass_type
    
class GlassColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='glass_colors')
    glass_color = models.CharField(max_length=255)
    additional_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return self.glass_color 
    
class GlassConfig(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='glass_configs')
    glass_config = models.CharField(max_length=255)
    additional_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return self.glass_config
    
class GlassCoating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='glass_coatings')
    glass_coating = models.CharField(max_length=255)
    additional_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return self.glass_coating
    
class Privacy(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='privacies')
    privacy = models.CharField(max_length=255)
    additional_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
        
    def __str__(self):
        return self.privacy
    



#####################################################Models de productos#####################################################
    
class Estimate(models.Model):
    estimate_number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    customer_info = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="estimates")
    # Nuevo campo para almacenar el número de orden
    order_number = models.PositiveIntegerField(null=True, blank=True)
    # Otros campos adicionales

    def __str__(self):
        return f"Estimate {self.estimate_number}"

    
    
#-----------------------VALIDATORS----------------------------#
def validate_positive(value):
    if value < 0:
        raise ValidationError(_("Quantity must be greater than zero."), code="invalid")
    
def validate_width(value):
    if value > 216 or value < 60:
        raise ValidationError(_("SIZE AND/OR CONFIGUIRATION NOT ALLOWED IN APPROVAL DOCUMENT."))

    
def validate_height(value):
    if value > 144 or value < 60:
        raise ValidationError(_("Height must be less than or equal to 144."), code="invalid")

class EstimateDetail(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE)
    mark = models.CharField(max_length=255, blank=True, verbose_name='Mark')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True, blank=True)
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE, null=True, blank=True)
    frame_color = models.ForeignKey(FrameColor, on_delete=models.CASCADE, null=True, blank=True)
    glass_type = models.ForeignKey(GlassType, on_delete=models.CASCADE, null=True, blank=True)
    glass_color = models.ForeignKey(GlassColor, on_delete=models.CASCADE, null=True, blank=True)
    glass_config = models.ForeignKey(GlassConfig, on_delete=models.CASCADE, null=True, blank=True)
    glass_coating = models.ForeignKey(GlassCoating, on_delete=models.CASCADE, null=True, blank=True)
    privacy = models.ForeignKey(Privacy, on_delete=models.CASCADE, null=True, blank=True)
    # Campos de tamaños y cantidades
    width = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_width])
    height = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_height])
    quantity = models.PositiveIntegerField(default=1, validators=[validate_positive])
    markup = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(100)], verbose_name="Markup")
    # Campos adicionales
    square_feet = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    tax_range = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Tax")

    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    # Resto de campos

    def calculate_total_price(self):
        base_price_per_square_foot = BasePrice.objects.get(product=self.product).base_price_per_square_foot
        square_feet = self.width * self.height / 144

        # Calculate adjustments
        price_adjustments = PriceAdjustment.objects.filter(
            product=self.product,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id
        )
        total_percentage_adjustment = sum([adjustment.percentage_adjustment for adjustment in price_adjustments])

        # Total price calculation
        self.unit_price = base_price_per_square_foot * square_feet * (1 + total_percentage_adjustment)
        self.total_price = self.unit_price * self.quantity
        self.tax = (self.tax_range / 100) * self.total_price

        super().save()
        
    def calculate_total_quantity(self):
        total_quantity = EstimateDetail.objects.filter(estimate=self.estimate).aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
        total_price = EstimateDetail.objects.filter(estimate=self.estimate).aggregate(total_price=models.Sum('total_price'))['total_price']
        self.total_quantity = total_quantity or 0
        self.total_price = total_price or 0
        self.save()
        return self.total_quantity

    def __str__(self):
        return f"EstimateDetail #{self.id}"
    

###############################ajuste de Precio ##################################
class PriceAdjustment(models.Model):
    name = models.CharField(max_length=255)
    percentage_adjustment = models.DecimalField(max_digits=5, decimal_places=2)
    estimate_detail = models.ForeignKey(EstimateDetail, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_from_db()
        content_type = ContentType.objects.get_for_model(self)
        for product in Product.objects.all():
            price_adjustment = PriceAdjustment.objects.create(
                product=product,
                content_type=content_type,
                object_id=self.id,
                percentage_adjustment=self.percentage_adjustment
            )
            price_adjustment.save()
            
##################################################Models de precios#####################################################

class BasePrice(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    base_price_per_square_foot = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)
    
 




# modelos para crear orders


class Order(models.Model):
    # Otros campos...

    order_number = models.AutoField(verbose_name='PO', primary_key=True)
    estimate = models.ForeignKey(
        Estimate, on_delete=models.CASCADE, null=True, blank=True)
    estimate_detail = models.ForeignKey(
        EstimateDetail, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders_customer')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    STATUS_CHOICES = [
        ('hold', 'Waiting for Approval'),
        ('approved', 'Scheduled'),
        ('in_production', 'Manufacturing'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
        # Otros estados que puedas necesitar
    ]

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='hold')

    changed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True, editable=False)
    notes = models.TextField(blank=True)
    note_history = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Si el Order está siendo creado (y no actualizado), asigna el total_price de EstimateDetail
        if not self.pk and self.estimate_detail:
            self.total_price = self.estimate_detail.total_price
        
        # Llama al método save original
        super().save(*args, **kwargs) 

    # ... (otros campos)

    def clean(self):
        # Validar que el cambio de estado siga el orden requerido
        if self.pk and self.status != 'hold':
            original_order = Order.objects.get(pk=self.pk)

            # Verificar que no puedes cambiar el estado de una orden entregada
            if original_order.status == 'delivered':
                raise ValidationError(
                    "No puedes cambiar el estado de una orden entregada.")

            # Verificar las transiciones permitidas
            allowed_transitions = {
                'hold': ['approved', 'canceled'],
                'approved': ['in_production', 'canceled'],
                'in_production': ['delivered', 'canceled'],
                'delivered': [],
                'canceled': [],
            }

            # Verificar las transiciones no permitidas
            if self.status not in allowed_transitions.get(original_order.status, []):
                raise ValidationError(
                    f"No se permite la transición de {original_order.get_status_display()} a {self.get_status_display()}.")

    def save(self, *args, **kwargs):
        # Guarda la referencia al objeto original antes de realizar modificaciones
        original_order = Order.objects.get(pk=self.pk) if self.pk else None

        # Guarda el historial de notas antes de sobrescribir la nota actual
        if original_order and original_order.status != self.status:
            if not self.note_history:
                self.note_history = original_order.notes
            else:
                self.note_history += f"\n{original_order.notes}"

        # Llama al método save del modelo antes de realizar modificaciones
        super().save(*args, **kwargs)

        # Actualiza la nota con el nuevo estado y el usuario que hizo el cambio
        if original_order and original_order.status != self.status:
            self.notes = f"{original_order.get_status_display()} to {self.get_status_display()} by {self.changed_by}"
            super().save(update_fields=['notes', 'note_history'])

    def __str__(self):
        return f"Order #{self.order_number}"
