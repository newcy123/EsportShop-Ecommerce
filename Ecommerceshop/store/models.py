import os
import uuid
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse 
from ckeditor.fields import RichTextField
import random
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
import time


# Create your models here.
class Geographies(models.Model):
    name = models.CharField(max_length=255)

class Provinces(models.Model):
    code = models.CharField(max_length=4)
    name_th = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    geography = models.ForeignKey(Geographies,on_delete = models.CASCADE)

class Amphures(models.Model):
    code = models.CharField(max_length=4)
    name_th = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    province = models.ForeignKey(Provinces,on_delete = models.CASCADE)

class Districts(models.Model):
    name_th = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    zip_code =models.IntegerField()
    amphure = models.ForeignKey(Amphures,on_delete = models.CASCADE)


class Customer_contract(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    provinces = models.ForeignKey(Provinces,on_delete = models.CASCADE)
    amphures = models.ForeignKey(Amphures,on_delete = models.CASCADE)
    districts = models.ForeignKey(Districts,on_delete = models.CASCADE)
    name=models.CharField(max_length=255,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    email=models.EmailField(max_length=250,blank=True,null=True)
    telephone =models.CharField(max_length=255,blank=True,null=True)
    postcode =models.CharField(max_length=5,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural ="ข้อมูลติดต่อลูกค้า"
        
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True) #ผูกข้อมูลไปกับ path
    # mouse
    # keyboard  
    # http://127.0.0.1:8000/mouse
    # http://127.0.0.1:8000/keyboard

    def __str__(self):
        return self.name

    class Meta :
        ordering=('name',)
        verbose_name_plural = "ข้อมูลประเภทสินค้า"
        verbose_name = 'หมวดหมู่สินค้า'
    
    def get_url(self):
        return reverse('product_category',args=[self.slug])

class Product(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True,allow_unicode=True) #ผูกข้อมูลไปกับ path 
    sub_description = RichTextField(blank=True,null=True)
    description = RichTextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    cost = models.IntegerField()
    category = models.ForeignKey(Category,on_delete = models.CASCADE) #ในกรณีลบ category ออก ต้องลบตัว product ที่มี category นั้นๆออกไปด้วย
    image = models.ImageField(upload_to="product",blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta :
        ordering=('name',)
        verbose_name_plural = "ข้อมูลสินค้า"
        verbose_name = 'สินค้า'

    def get_url(self):
        return reverse('productDetail',args=[self.category.slug,self.slug])
        
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

  
    def __str__(self):
        return self.cart_id

    class Meta:
        db_table ='cart'
        ordering=('created',)
        verbose_name_plural = "ตะกร้า"
        verbose_name = 'รหัสตะกร้า'

class CartItem(models.Model):
    #ในกรณีลบ category ออก ต้องลบตัว product ที่มี category นั้นๆออกไปด้วย
    product = models.ForeignKey(Product,on_delete = models.CASCADE,related_name="cart_item") 
    cart = models.ForeignKey(Cart,on_delete= models.CASCADE)
    qty = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table ='cartItem'
        verbose_name_plural = "รายการสินค้าในตะกร้า"
        verbose_name = 'ข้อมูลสินค้า'
        
    def sub_total(self):
        return self.product.price * self.qty
    

class OrderStatus(models.Model):
   
    STATUS_CHOICES =(
        ("NEW","รอการชำระเงิน"),
        ("PAID","ชำระเงินแล้ว"),
        ("AWAITING SHIPMENT","รอการจัดส่ง"),
        ("DELIVERED","จัดส่งแล้ว")
    )
    
    status_name =models.CharField(max_length=200,choices=STATUS_CHOICES,default='NEW')
    active = models.BooleanField(default=False)
    
    class Meta:
        db_table ='OrderStatus'
        verbose_name_plural = "สถานะสินค้า"
        verbose_name = 'สถานะ'
    
    def __str__(self):
        return self.status_name


class PaymentType(models.Model):
    payment_type=models.CharField(max_length=255,blank=True)
    payment_image = models.ImageField(upload_to="payment",null=True,blank=True)
    active = models.BooleanField(default=False)

    class Meta:
        db_table ='PaymentType'
        verbose_name_plural = "ประเภทการชำระเงิน"
        verbose_name = 'ประเภท'
    
    def __str__(self):
        return self.payment_type

def random_number():
    return "OD0000" + get_random_string(5,allowed_chars='0123456789')


class Bank(models.Model):
    bank_name= models.CharField(max_length=255,blank=True)
    bank_name_account=models.CharField(max_length=255,blank=True)
    bank_number = models.CharField(max_length=255,blank=True)
    bank_telephone= models.CharField(max_length=255,blank=True)
    bank_image = models.ImageField(upload_to="bank",null=True,blank=True)
    active = models.BooleanField(default=False)

    class Meta:
        db_table ='Bank'
        verbose_name_plural = "ธนาคาร"
        verbose_name = 'ชื่อ'
    
    def __str__(self):
        return self.bank_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_contract = models.ForeignKey(Customer_contract, on_delete=models.CASCADE)
    orderstatus = models.ForeignKey(OrderStatus,on_delete = models.CASCADE)
    paymenttype = models.ForeignKey(PaymentType,on_delete = models.CASCADE)
    bank = models.ForeignKey(Bank,on_delete = models.CASCADE,default=1)
    
    order_id = models.CharField(default=random_number,max_length=255,null=False,unique=True,blank=False)
    total=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    costtotal = models.IntegerField()
    charge = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    credit_email = models.EmailField(max_length=250,blank=True,null=True)
    token=models.CharField(max_length=255,blank=True,null=True)
    transfer = models.CharField(max_length=50,blank=True,null=True)
    transfer_image = models.ImageField(upload_to="slip",null=True,default=None,blank=True)
    transfer_date = models.DateField(blank=True,null=True,default=None)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False) 

    class Meta :
        db_table='Order'
        verbose_name_plural = "รายการสั้่งซื้อ"
        

    def total_all(self):
        return self.total + self.costtotal + self.charge
    
  
    def __str__(self):
        return str(self.id)
    

class OrderItem(models.Model):
    product=models.CharField(max_length=250)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='OrderItem'
        verbose_name_plural = "สินค้าในรายการสั้่งซื้อ"
        ordering=('order',)

    def sub_total(self):
        return self.quantity*self.price
    
    def __str__(self):
        return self.product






    

    