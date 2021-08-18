# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Amphures(models.Model):
    code = models.CharField(max_length=4)
    name_th = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    province_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'amphures'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart_id = models.CharField(max_length=255)
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cart'


class Cartitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    qty = models.IntegerField()
    active = models.IntegerField()
    cart = models.ForeignKey(Cart, models.DO_NOTHING)
    product = models.ForeignKey('StoreProduct', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cartitem'


class Districts(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    zip_code = models.IntegerField()
    name_th = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    amphure_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'districts'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Geographies(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'geographies'


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=32)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.CharField(max_length=250)
    token = models.CharField(max_length=255, blank=True, null=True)
    transfer = models.CharField(max_length=50, blank=True, null=True)
    transfer_image = models.CharField(max_length=100)
    transfer_date = models.DateField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    orderstatus = models.ForeignKey('Orderstatus', models.DO_NOTHING)
    paymenttype = models.ForeignKey('Paymenttype', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'order'


class Orderitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    order = models.ForeignKey(Order, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'orderitem'


class Orderstatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    status_name = models.CharField(max_length=200)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'orderstatus'


class Paymenttype(models.Model):
    id = models.BigAutoField(primary_key=True)
    payment_type = models.CharField(max_length=255)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'paymenttype'


class Provinces(models.Model):
    code = models.CharField(max_length=2)
    name_th = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    geography_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'provinces'


class StoreCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    slug = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'store_category'


class StoreProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    slug = models.CharField(unique=True, max_length=100)
    sub_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.IntegerField()
    image = models.CharField(max_length=100)
    stock = models.IntegerField()
    available = models.IntegerField()
    created = models.DateTimeField()
    update = models.DateTimeField()
    category = models.ForeignKey(StoreCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_product'
