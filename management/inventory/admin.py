from django.contrib import admin

# Register your models here.

from. import models


class VendorAdmin(admin.ModelAdmin):
    list_display=['full_name','email_address','mobile','status']
    search_fields=['full_name','email_address','mobile','status']
admin.site.register(models.Vendor,VendorAdmin)

admin.site.register(models.Unit)

class CustomerAdmin(admin.ModelAdmin):
    list_display=['customer_name','customer_mobile','customer_email']
    search_fields=['customer_name','customer_mobile','customer_email']
admin.site.register(models.Customer,CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['tittle', 'unit', 'inventory_pur_qty', 'inventory_sale_qty', 'inventory_available_qty']
    search_fields = ['tittle', 'unit__tittle']
    
    def inventory_pur_qty(self, obj):
        # Get the latest inventory entry for the product and return the purchase quantity
        inventory = obj.inventory_set.order_by('-id').first()  # Access related inventory using reverse relation
        return inventory.pur_qty if inventory else 0
    inventory_pur_qty.short_description = 'Purchase Qty'

    def inventory_sale_qty(self, obj):
        # Get the latest inventory entry for the product and return the sale quantity
        inventory = obj.inventory_set.order_by('-id').first()  # Access related inventory using reverse relation
        return inventory.sale_qty if inventory else 0
    inventory_sale_qty.short_description = 'Sale Qty'

    def inventory_available_qty(self, obj):
        # Get the latest inventory entry for the product and return the available quantity
        inventory = obj.inventory_set.order_by('-id').first()  # Access related inventory using reverse relation
        return inventory.Available_qty if inventory else 0
    inventory_available_qty.short_description = 'Available Qty'

admin.site.register(models.Product,ProductAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display=['Vendor','product','qty','price','total_amt','pur_date']
    search_fields=['product__tittle']
admin.site.register(models.Purchase,PurchaseAdmin)


class SaleAdmin(admin.ModelAdmin):
    list_display=['id','Customer','product','qty','price','total_amt','sale_date']
    search_fields=['product__tittle','product__unit__tittle']

admin.site.register(models.Sale,SaleAdmin)

class InventoryAdmin(admin.ModelAdmin):
    search_fields=['product__tittle','product__unit__tittle']
    list_display=['product','pur_qty','sale_qty','Available_qty','product_unit','pur_date','sale_date']
admin.site.register(models.Inventory,InventoryAdmin)

