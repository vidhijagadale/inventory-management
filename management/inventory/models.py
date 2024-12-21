from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Vendor(models.Model):
    full_name=models.CharField(max_length=50)
    email_address=models.CharField(max_length=30,unique=True)
    address=models.TextField()
    mobile=models.CharField(max_length=15)
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='1. Vendors'

    def __str__(self):
        return self.full_name
    

class Unit(models.Model):
    tittle=models.CharField(max_length=50)
    short_name=models.CharField(max_length=15)

    class Meta:
        verbose_name_plural='2. Units'

    def __str__(self):
        return self.tittle
    

class Product(models.Model):
    tittle=models.CharField(max_length=50)
    detail=models.TextField()
    photo=models.ImageField(upload_to="product/")
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='3. Products'

    def __str__(self):
        return self.tittle
    
    
class Purchase(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    Vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    qty=models.FloatField()
    price=models.FloatField()
    total_amt=models.FloatField(editable=False,default=0)
    pur_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='4. Purchases'

    def save(self,*args,**kwargs):
        self.total_amt=self.qty*self.price
        super(Purchase,self).save(*args,**kwargs)

        inventory=Inventory.objects.filter(product=self.product).order_by('-id').first()
        if inventory:
            totalBal=inventory.Available_qty+self.qty
        else:
            totalBal=self.qty

        Inventory.objects.create(
            product=self.product,
            purchase=self,
            sale=None,
            pur_qty=self.qty,
            sale_qty=None,
            Available_qty=totalBal
        )

class Customer(models.Model):
    customer_name = models.CharField(max_length=30,)
    customer_mobile = models.CharField(max_length=10)
    customer_email=models.CharField(max_length=30)
    customer_address = models.TextField()

    class Meta:
        verbose_name_plural='7. Customers'

    def __str__(self):
        return self.customer_name


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    qty = models.FloatField()
    price = models.FloatField()
    total_amt = models.FloatField(editable=False)
    sale_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '5. Sales'

    def clean(self):
        # Fetch the latest inventory for the product
        inventory = Inventory.objects.filter(product=self.product).order_by('-id').first()
        if not inventory or inventory.Available_qty < self.qty:
            raise ValidationError(
                f"Cannot complete the sale. Only {inventory.Available_qty if inventory else 0} units are available in stock."
            )

    def save(self, *args, **kwargs):
        # Validate the sale before saving
        self.full_clean()  # Calls the `clean` method for validation

        # Calculate total amount
        self.total_amt = self.qty * self.price

        # Fetch the latest inventory and update stock
        inventory = Inventory.objects.filter(product=self.product).order_by('-id').first()
        totalBal = inventory.Available_qty - self.qty if inventory else -self.qty

        # Save the sale
        super(Sale, self).save(*args, **kwargs)

        # Update inventory
        Inventory.objects.create(
            product=self.product,
            purchase=None,
            sale=self,
            pur_qty=None,
            sale_qty=self.qty,
            Available_qty=totalBal
        )

class Inventory(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    pur_qty=models.FloatField(default=0,null=True)
    sale_qty=models.FloatField(default=0,null=True)
    purchase=models.ForeignKey(Purchase,on_delete=models.CASCADE,default=0,null=True)
    sale=models.ForeignKey(Sale,on_delete=models.CASCADE,default=0,null=True)
    Available_qty=models.FloatField(default=0)
    
    class Meta:
        verbose_name_plural='6. Inventory'

    def product_unit(self):
        return self.product.unit.tittle

    def pur_date(self):
        if self.purchase:
            return self.purchase.pur_date
        
    def sale_date(self):
        if self.sale:
            return self.sale.sale_date



    
