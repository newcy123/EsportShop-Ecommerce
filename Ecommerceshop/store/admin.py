from django.contrib import admin
from .models import Customer_contract,Category,Product,CartItem,Cart,OrderItem,Order,PaymentType,OrderStatus,Bank
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','stock','update','created']
    list_editable=['price','stock']
    list_per_page = 3


class OrderAdmin(admin.ModelAdmin):
    list_display=['id','total','paymenttype','orderstatus']

class OrderItemAdmin(admin.ModelAdmin):
    list_display=['order','product','quantity','price']

class BankAdmin(admin.ModelAdmin):
    list_display=['bank_name','bank_name_account','bank_number','bank_telephone']

class PaymentTypeAdmin(admin.ModelAdmin):
    list_display=['payment_type','active']
    

class OrderStatusAdmin(admin.ModelAdmin):
    list_display=['status_name','active']
    


admin.site.register(Customer_contract)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Bank,BankAdmin)
admin.site.register(PaymentType,PaymentTypeAdmin)
admin.site.register(OrderStatus,OrderStatusAdmin)