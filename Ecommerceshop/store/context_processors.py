from .models import Category,Cart,CartItem
from store.views import _cart_id

def menu_links(request): 
    link = Category.objects.all()
    return dict(link=link)

def count_cart(request): #เพิ่มจำนวนสินค้าในตะกร้า
    item_count =0
    user = request.user
    #if 'admin' in request.path:
     #   return {}
    if user.is_authenticated:
        try:
            cart = Cart.objects.filter(user =request.user)
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            print(cart_items)
            for item in cart_items:
                item_count += item.qty
        
        except CartItem.DoesNotExist:
                item_count = 0

    return dict(item_count=item_count)

    