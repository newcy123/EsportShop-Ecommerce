"""Ecommerceshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    # หน้าแรก user
    path('', views.index, name="home"),
    path('orders/', views.how_to_orders),
    path('payment/', views.how_to_payment),
    path('aboutus/', views.about_us),
    path('contractus/', views.contract_us),

    # หน้าแรก admin/dashboard
    path('admins/dashboard/', views.dashboard, name="chart"),
    path('admins/members/', views.member),
    path('admins/members/update/', views.update_member, name="edit_member"),
    path('admins/members/delete/', views.delete_member, name="delete_member"),
    path('admins/search_member/', views.search_member, name="search_member"),
    path('admins/search_product/', views.search_product, name="search_product"),
    path('admins/productall/', views.product_manager, name="product_manager"),
    path('admins/addproduct/', views.product),
    path('admins/product/update/', views.update_product, name="update_product"),
    path('admins/categorys/', views.category),
    path('admins/add/categorys/', views.add_category, name="add_category"),
    path('admins/add/product/', views.add_product, name="add_product"),

    # ประเภทสินค้า
    path('category/<slug:category_slug>', views.index, name='product_category'),

    # รายละเอียดสินค้า
    path('product/<slug:category_slug>/<slug:product_slug>',
         views.productdetail, name="productDetail"),

    # ตะกร้าสินค้า
    path('cart/add/<int:product_id>/', views.addCart,
         name="addCart"),  # ส่งproduct_id ไป
    path('cart/buy/<int:product_id>/',
         views.buy_cartdetail, name="buy_cartdetail"),
    path('cart/incress_cart/<int:product_id>/',
         views.incress_cart, name="update_cart"),
    path('cart/decress_cart/<int:product_id>/',
         views.decress_cart, name="decress_cart"),
    path('cartdetail', views.cartdetail),
    path('cart/remove/<int:product_id>',
         views.cart_item_delete, name="cart_item_delete"),


    # หน้า addresschoose
    path('cart/address/', views.save_address, name="save_address"),
    path('cart/address/update/', views.update_address, name="update_address"),
    path('cart/address/delete/<int:address_id>/',
         views.delete_address, name="delete_address"),
    path('cartdetail/addresschoose/', views.saveorder, name="saveorder"),
    path('cartdetail/addresschoose/save/', views.save_order, name="save_order"),


    # หน้า ยืนยันการสั่งซื้อ
    path('cartdetail/addresschoose/save/confirm',
         views.confirm_order, name="confirm_order"),
    path('cartdetail/addresschoose/save/confirm_credit',
         views.confirm_order_credit, name="confirm_order_credit"),


    # Login/register
    path('signup/', views.signup),
    path('signup_post', views.signup_post, name="signup_post"),
    path('login/', views.login, name="login"),
    path('logincheck', views.logincheck, name="logincheck"),
    path('logout', views.logoff, name="logoff"),
    path('search/', views.search, name='search'),
    path('search/order', views.search_order_id, name='search_order_id'),
    path('cartdetail/checkout/thankyou/', views.thankyou, name="thankyou"),


    # ประวัติการสั่งซื้อ admin/customer
    path('admins/orderlist/', views.orderList, name="orderlist"),
    path('orderlist/orderstatus/<str:order_id>',
         views.status_change, name="status_change"),
    path('orderlist/updatetracking/<str:order_id>',
         views.update_tracking, name="updatetracking"),


    # ดูประวัติการสั่งซ์้อ
    path('my-account/orderhistory/', views.orderHistory, name="orderhistory"),
    path('my-account/orderhistory/vieworder/<str:order_id>',
         views.viewOrder, name="vieworder"),
    path('my-account/orderhistory/uploadslip/<str:order_id>',
         views.order_approve, name="order_approve"),


    # จังหวัด อำเภอ ตำบล
    path('ajax/load-amphures/', views.load_amphures, name='ajax_load_amphures'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),



]


if settings.DEBUG:
    # /media/product
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # /static/
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    # /static/media/product/iphone/jpg
handler404 = 'store.views.handler404'
handler500 = 'store.views.handler500'
