from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [

    # หน้าเกี่ยวกับ admin
    path('admins/dashboard/', views.dashboard),
    path('admins/members/', views.member),
    path('admins/members/update/', views.update_member, name="edit_member"),
    path('admins/members/delete/', views.delete_member, name="delete_member"),
    path('admins/search_member/', views.search_member, name="search_member"),
    path('admins/search_product/', views.search_product, name="search_product"),
    path('admins/productall/', views.product_manager, name="product_manager"),
    path('admins/addproduct/', views.product),
    path('admins/product/update/', views.update_product, name="update_product"),
    path('admins/product/delete/', views.delete_product, name="delete_product"),
    path('admins/categorys/', views.category),
    path('admins/add/categorys/', views.add_category, name="add_category"),
    path('admins/add/product/', views.add_product, name="add_product"),

    # ประวัติการสั่งซื้อ admin/customer
    path('admins/orderlist/', views.orderList, name="orderlist"),
    path('orderlist/orderstatus/<str:order_id>',
         views.status_change, name="status_change"),
    path('orderlist/updatetracking/<str:order_id>',
         views.update_tracking, name="updatetracking"),


    # Login/register
    path('signup/', views.signup),
    path('signup_post', views.signup_post, name="signup_post"),
    path('login/', views.login, name="login"),
    path('logincheck', views.logincheck, name="logincheck"),
    path('logout', views.logoff, name="logoff"),
    path('search/', views.search, name='search'),
    path('search/order', views.search_order_id, name='search_order_id'),
    path('cartdetail/checkout/thankyou/', views.thankyou, name="thankyou"),


    # path ด้านล่างเกี่ยวกับสิ่งลูกค้ากระทำทั้งหมด
    # หน้าแรก user
    path('', views.index, name="home"),
    path('orders/', views.how_to_orders),
    path('payment/', views.how_to_payment),
    path('aboutus/', views.about_us),
    path('contractus/', views.contract_us),


    # ประเภทสินค้า
    path('category/<slug:category_slug>', views.index, name='product_category'),

    # รายละเอียดสินค้า
    path('product/<slug:category_slug>/<slug:product_slug>',
         views.productdetail, name="productDetail"),

    # ตะกร้าสินค้า
    path('cart/add/<int:product_id>/', views.addCart,
         name="addCart"),
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


    # หน้ายืนยันการสั่งซื้อสำหรับลูกค้า
    path('cartdetail/addresschoose/save/confirm',
         views.confirm_order, name="confirm_order"),
    path('cartdetail/addresschoose/save/confirm_credit',
         views.confirm_order_credit, name="confirm_order_credit"),


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
