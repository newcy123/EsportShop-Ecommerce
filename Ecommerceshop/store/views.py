from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Count, Sum, Q
from .models import User, Customer_contract, Category, Product, CartItem, Cart, OrderItem, Order, PaymentType, OrderStatus, Provinces, Amphures, Districts, PaymentType, Bank
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from store.forms import SignUpForm  # หน้าลงทะเบียน จาก forms.py
# เกี่ยวกับการ login และ ยืนยันความถูกต้องของ username,password
from django.contrib.auth import login as auth_login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, InvalidPage  # หมายเลขหน้า
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings  # api key
import stripe  # ชำระเงิน
from django.contrib import messages  # ทำ alert แจ้งเตื่อน
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
from dateutil.rrule import rrule, MONTHLY
import decimal


def index(request, category_slug=None):  # สร้างหน้าแรก และ หมวดหมู่สินค้า
    if not request.user.is_staff:
        products = None
        category_page = None
        if category_slug != None:  # มีการเลือก หมวดหมู่สินค้า
            # ค้าหาข้อมูล หมวดหมู่ ที่อยู่ใน โมเดล Category

            category_page = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.all().filter(category=category_page, available=True)

        else:
            products = Product.objects.all().filter(available=True)

        # 6/2 =3
        paginator = Paginator(products, 6)  # 6:1 หน้า

        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            product_Page = paginator.page(page)

        except (EmptyPage, InvalidPage):  # กรณีหน้าเปล่าๆ,มีข้อมูลไม่ถูกต้อง
            product_Page = paginator.page(
                paginator.num_pages)  # lock หน้าสูงสุด 3

        return render(request, 'store/home/home.html', {'products': product_Page, 'category': category_page})


def how_to_orders(request):
    return render(request, 'store/home/how_to_orders.html')


def how_to_payment(request):
    return render(request, 'store/home/how_to_payment.html')


def about_us(request):
    return render(request, 'store/home/about_us.html')


def contract_us(request):
    return render(request, 'store/home/contract_us.html')


def productdetail(request, category_slug, product_slug):  # แสดงรายละเอียดสินค้า
    try:
        product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        qty = product.stock
        qty_list = []
        for i in range(qty):
            qty_list.append(i+1)

    except Exception as e:
        raise e
    return render(request, 'store/shop/productdetail.html', {'product': product, 'qty': qty_list})


def _cart_id(request):  # สร้าง seesion , รหัสตะกร้าสินค้า
    cart = request.session.session_key  # เช็ค seesion
    if not cart:
        cart = request.session.create()

    return cart


@login_required(login_url='/login')
def addCart(request, product_id):  # กดปุ่มเพิ่มลงหรือซื้อตอนนี้ตะกร้า -> สินค้าเข้าตะกร้า
    # ส่งรหัสสินค้าติดมาด้วย product_id จาก Product
    # ดึงรหัสสินค้าตาม product_id ที่ส่งมา
    product = Product.objects.get(id=product_id)
    selected_value = int(request.POST['dropdown'])

    # สร้างตะกร้าสินค้า มี 2 กรณี มีอยู่แล้ว กับ พึ่งเคยสร้าง
    # เช็คว่าเคยมีตะกร้าสินค้าหรือไม่

    try:  # เคยสร้างแล้ว
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:  # ยังไม่เคยสร้างแล้ว ให้สร้างขึ่นมาใหม่
        cart = Cart.objects.create(user=request.user)
        cart.save()

    # ซื้อรายการสินค้าซ้ำ cartItem
    try:
        # กดซื้อสินค้าซ้ำ
        # เช็คว่ามีสินค้า ซ้ำ ไหมใน ตะกร้า เดียวกัน
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.qty < cart_item.product.stock:
            cart_item.qty += selected_value
            cart_item.save()

    except CartItem.DoesNotExist:
        # ซ์้อรายการสินค้าครั้งแรก
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            qty=selected_value
        )

        cart_item.save()
    if 'add' in request.POST:
        return redirect(request.META['HTTP_REFERER'])

    return redirect('/cartdetail')


@login_required(login_url='/login')
# กดปุ่ม 'เพิ่มลงตะกร้าหน้าแรก'-> สินค้าเข้าตะกร้า
def buy_cartdetail(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:  # ยังไม่เคยสร้างแล้ว ให้สร้างขึ่นมาใหม่
        cart = Cart.objects.create(user=request.user)
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.qty < cart_item.product.stock:
            cart_item.qty += 1
            cart_item.save()

    except CartItem.DoesNotExist:

        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            qty=1
        )

        cart_item.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login')
def cartdetail(request):  # แสดงรายละเอียดสินค้า
    total = 0
    total_all = 0
    count = 0
    stock = 0
    cost = 0

    cart_items = None  # ดึงมาจาก database เพือดึงเอาค่า qty

    try:
        # ดึงก้อนตะกร้าสินค้าที่มี session ตรงกับ id ที่login
        cart = Cart.objects.get(user=request.user)
        # โยน cart (ก้อนตะกร้าสินค้า) ที่ CartItem เพือเช็คว่า มีสินค้าตัวใดบ้างอยู่ใน cart (ก้อนตะกร้าสินค้า) พร้อมเช็ค active = true
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for item in cart_items:

            for i in range(item.qty):
                cost += item.product.cost

            total += item.product.price * item.qty
            total_all += (item.product.price * item.qty) + cost
            count += item.qty
            stock = item.product.stock

        # ---- Logic shoppee
        # big =0
        # small =0
        # pay = 0
        # List =[]
        # big = None
        # small = None

        #         check += 1
        #         cost = item.product.cost
        #         List.append(cost)

        #         for z,j in enumerate(List):

        #             if big is None or j > big:
        #                 big = j

        #             if small is None or j < small:
        #                 small = j

        #     if check == 1:
        #         pay = small

        #     else:
        #         for k in range(item.qty):
        #             big = big + 15
        #             print(big)
        #         pay = big

        #     pay = big
          # if check == 1:
            #   cost = item.product.cost
            # elif item.product.cost == cost:
            #   cost = item.product.cost

    except Exception as e:
        pass

    return render(request, 'store/cart/cartdetail.html',
                  dict(
                      cart_items=cart_items,
                      total=total,
                      total_all=total_all,
                      count=count,
                      cost=cost,

                  ))


@login_required(login_url='/login')
def incress_cart(request, product_id):  # เพิ่มจำนวนสินค้าบนตะกร้า
    product = Product.objects.get(id=product_id)

    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.qty += 1

    if cart_item.qty > cart_item.product.stock:
        cart_item.qty = cart_item.product.stock
    cart_item.save()

    return redirect('/cartdetail')


@login_required(login_url='/login')
def decress_cart(request, product_id):  # ลดจำนวนสินค้าบนตะกร้า
    product = Product.objects.get(id=product_id)

    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.qty <= 1:
        cart_item.delete()
    else:
        cart_item.qty -= 1
        cart_item.save()

    return redirect('/cartdetail')


@login_required(login_url='/login')
def cart_item_delete(request, product_id):  # ลบสินค้าบนตะกร้า

    cart = Cart.objects.get(user=request.user)
    # ดึง id ของสินค้าที่ตรงกับ product_id ที่รับมา
    product = get_object_or_404(Product, id=product_id)
    # ดึงตะกร้าสินค้าที่มี สินค้ากับตะกร้าตรงกัน
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()

    return redirect("/cartdetail")


@login_required(login_url='/login')
def saveorder(request):  # แสดงหน้า Addresschoose

    provinces = Provinces.objects.all()
    payment_type = PaymentType.objects.all()

    cart_items = None  # ดึงมาจาก database เพือดึงเอาค่า qty
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        contract = Customer_contract.objects.all().filter(user=request.user)

    except Exception as e:
        pass

    return render(request, 'store/cart/addresschoose.html',
                  dict(
                      provinces=provinces,
                      payment_type=payment_type,
                      cart_items=cart_items,
                      contract=contract,

                  ))


@login_required(login_url='/login')
def save_order(request):  # บันทึกข้อมูลหน้า Addresschoose
    total = 0
    total_all = 0
    count = 0
    stock = 0
    cost = 0
    charge_amount = 0.0

    # ดึงก้อนตะกร้าสินค้าที่มี username ตรงกับ id ที่login
    cart = Cart.objects.get(user=request.user)
    # โยน cart (ก้อนตะกร้าสินค้า) ที่ CartItem เพือเช็คว่า มีสินค้าตัวใดบ้างอยู่ใน cart (ก้อนตะกร้าสินค้า) พร้อมเช็ค active = true
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    contract = Customer_contract.objects.all().filter(user=request.user)

    for item in cart_items:

        for i in range(item.qty):
            cost += item.product.cost

        total += item.product.price * item.qty
        total_all += (item.product.price * item.qty) + cost
        count += item.qty
        stock = item.product.stock
    if request.method == "POST":
        if not contract:
            messages.error(request, "กรุณาเพิ่มที่อยู่ก่อน")
            return redirect(request.META['HTTP_REFERER'])
        contract = request.POST['contract']
        payment_type = request.POST['payment_type']

    if payment_type == '1':
        charge_amount = ((3 * total_all)/100) + 9
        # charge = ( 2.9 * total_all)/100) + 9.51

    elif payment_type != '1':
        charge_amount = 0

    stripe.api_key = settings.SECRET_KEY
    stripe_total = int((total_all*100)+(charge_amount*100))
    description = "Payment Online"
    data_key = settings.PUBLIC_KEY
    return render(request, 'store/cart/confirm_order.html',
                  dict(
                      contract=contract,
                      payment_type=payment_type,
                      cart_items=cart_items,
                      total=total,
                      total_all=total_all+charge_amount,
                      count=count,
                      cost=cost,
                      charge=charge_amount,
                      stock=stock,
                      data_key=data_key,
                      stripe_total=stripe_total,
                      description=description
                  ))


@login_required(login_url='/login')
def confirm_order(request):  # ยืนยันการสั่งซื้อผ่านธนาคาร
    total = 0
    total_all = 0
    count = 0
    stock = 0
    cost = 0
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for item in cart_items:

            for i in range(item.qty):
                cost += item.product.cost

            total += item.product.price * item.qty
            total_all += (item.product.price * item.qty) + cost
            count += item.qty
            stock = item.product.stock
    except Exception as e:
        pass

    contract = request.POST['contract']
    payment_type = request.POST['payment_type']
    order = Order.objects.create(
        user=request.user,
        customer_contract_id=contract,
        paymenttype_id=payment_type,
        orderstatus_id=1,
        total=total,
        charge=0,
        costtotal=cost,
        transfer_image=None,
    )
    order.save()

    order__id = order.order_id

    for item in cart_items:
        order_Item = OrderItem(
            product=item.product.name,
            quantity=item.qty,
            price=item.product.price,
            order=order
        )
        order_Item.save()
        product = Product.objects.get(id=item.product.id)
        product.stock = int(item.product.stock-order_Item.quantity)
        product.save()
        item.delete()  # clear ตะกร้าสินค้า โดยการลบข้อมูลสินค้าที่ละตัวตามลูป

    request.session['order'] = order__id
    return redirect('/cartdetail/checkout/thankyou')


@login_required(login_url='/login')
def confirm_order_credit(request):  # ยืนยันการสั่งซื้อผ่านบัตรเครดิต

    total = 0
    total_all = 0
    count = 0
    stock = 0
    cost = 0
    charge_amount = 0.0
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for item in cart_items:

            for i in range(item.qty):
                cost += item.product.cost

            total += item.product.price * item.qty
            total_all += (item.product.price * item.qty) + cost
            count += item.qty
            stock = item.product.stock
        charge_amount = ((3 * total_all)/100) + 9
    except Exception as e:
        pass
    contract = request.POST['contract']
    payment_type = request.POST['payment_type']
    stripe.api_key = settings.SECRET_KEY
    stripe_total = int((total_all * 100) + (charge_amount*100))
    description = "Payment Online"
    data_key = settings.PUBLIC_KEY

    try:
        token = request.POST['stripeToken']
        email = request.POST['stripeEmail']
        customer = stripe.Customer.create(
            email=email,
            source=token
        )
        charge = stripe.Charge.create(
            amount=stripe_total,
            currency='thb',
            description=description,
            customer=customer.id
        )
        # บันทึกข้อมูลใบสั่งซื้อ

        order = Order.objects.create(
            user=request.user,
            customer_contract_id=contract,
            paymenttype_id=payment_type,
            credit_email=email,
            orderstatus_id=2,
            charge=charge_amount,
            total=total,
            costtotal=cost,
            transfer_image=None,
            token=token
        )
        order.save()
        order__id = order.order_id
        for item in cart_items:
            order_Item = OrderItem(
                product=item.product.name,
                quantity=item.qty,
                price=item.product.price,
                order=order
            )
            order_Item.save()
            product = Product.objects.get(id=item.product.id)
            product.stock = int(item.product.stock-order_Item.quantity)
            product.save()
            item.delete()  # clear ตะกร้าสินค้า โดยการลบข้อมูลสินค้าที่ละตัวตามลูป
        request.session['order'] = order__id
        return redirect('/cartdetail/checkout/thankyou')

    except stripe.error.CardError as e:
        return False, e


# หน้าขอบคุณ
@login_required(login_url='/login')
def thankyou(request):

    order_id = request.session['order']
    order_num = Order.objects.get(order_id=order_id)
    return render(request, 'store/cart/thankyou.html', {'order': order_num})


# ลงทะเบียน
def signup(request):  # แสดงหน้าลงทะเบียน
    form = SignUpForm()
    return render(request, 'store/account/signup.html', {'form': form})


def signup_post(request):  # หน้าบันทึกข้อมูล
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # 1 บันทึกข้อมูล table user จากการ signup
            form.save()

            # 2 บันทึกข้อมูล user ลงไปที่ group customer
            # ดึงข้อมูล username จากการกรอกใน signup หลังจากมีการ save แล้ว
            username = form.cleaned_data.get("username")

            # ดึงข้อมูล user จากฐานข้อมูล
            Signup = User.objects.get(username=username)

            # ยัดข้อมูล user ลงไปใน group customer

            customer_group = Group.objects.get(name="Customer")
            customer_group.user_set.add(Signup)
            messages.success(request, "ลงทะเบียนสำเร็จ")

    else:
        form = SignUpForm()

    return render(request, 'store/account/signup.html', {'form': form})


def login(request):  # แสดงหน้า login
    form = AuthenticationForm()
    return render(request, 'store/account/login.html', {'form': form})


def logincheck(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user.is_staff:
                auth_login(request, user)
                # return render(request,'st')
                return redirect("admins/dashboard/")

            if user is not None:
                auth_login(request, user)
                return redirect("/")

            else:
                messages.error(request, "username หรือ password ไม่ถูกต้อง")
                return redirect("/login")

    else:
        form = AuthenticationForm()
    return render(request, 'store/account/login.html', {'form': form})


def logoff(request):  # logoff
    logout(request)
    return redirect("/login")


def search(request):  # ค้นหาสินค้า
    serach = request.GET['product']
    serach_product = Product.objects.filter(name__icontains=serach)
    if not serach_product:

        messages.error(request, "ไม่พบชื่อสินค้าที่ค้นหา")

    return render(request, 'store/home.html', {'products': serach_product})


# รายการสั่งซ์้อ
@login_required(login_url='/login')
def search_order_id(request):
    if request.user.is_authenticated:
        orderId = request.GET['order_id']

        if request.user.is_staff:
            order_id = Order.objects.filter(order_id=orderId)
            if not order_id:
                messages.error(request, "ไม่พบรหัสสั่งซื้อที่ค้นหา")
            return render(request, 'store/orderlist.html', {'orders': order_id})

        elif not request.user.is_staff:
            order_id = Order.objects.filter(
                user=request.user, order_id=orderId)
            if not order_id:
                messages.error(request, "ไม่พบรหัสสั่งซื้อที่ค้นหา")
            return render(request, 'store/orderhistory.html', {'orders': order_id})


@login_required(login_url='/login')
def orderList(request):  # สำหรับ admin
    if request.user.is_authenticated:
        if request.user.is_staff:
            order_list = Order.objects.all()
            if not order_list:
                messages.error(request, "ไม่พบรายการสั่งซื้อของลูกค้า")

            paginator = Paginator(order_list, 10)

            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                order_Page = paginator.page(page)

            except (EmptyPage, InvalidPage):  # กรณีหน้าเปล่าๆ,มีข้อมูลไม่ถูกต้อง
                order_Page = paginator.page(
                    paginator.num_pages)  # lock หน้าสูงสุด 3
    return render(request, 'store/admin/orderlist.html', dict(orders=order_Page))


@login_required(login_url='/login')
def orderHistory(request):  # สำหรับ user
    if request.user.is_authenticated:

        order_list = Order.objects.filter(user=request.user)
        if not order_list:
            messages.error(request, "ไม่พบรายการสั่งซื้อ")
        paginator = Paginator(order_list, 10)

        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            order_Page = paginator.page(page)

        except (EmptyPage, InvalidPage):  # กรณีหน้าเปล่าๆ,มีข้อมูลไม่ถูกต้อง
            order_Page = paginator.page(
                paginator.num_pages)  # lock หน้าสูงสุด 3

    return render(request, 'store/orders/orderhistory.html', dict(orders=order_Page))


@login_required(login_url='/login')
def viewOrder(request, order_id):  # ดูรายละเอียดสินค้า/ปริ้นสินค้า
    order_list = None
    if request.user.is_authenticated:
        order_list = Order.objects.get(order_id=order_id)
        order__list = order_list.id
        order_item = OrderItem.objects.filter(order=order__list)
    return render(request, 'store/orders/orderdetail.html', {
        'order': order_list,
        'order_item': order_item
    })


@login_required(login_url='/login')
def order_approve(request, order_id):  # แจ้งชำระ/อัพโหลดสลิป
    count = 0
    cost = 0
    total_all = 0
    banks = Bank.objects.all()

    if request.user.is_authenticated:

        email = str(request.user.email)
        order_list = Order.objects.get(order_id=order_id)
        order__list = order_list.id
        order_item = OrderItem.objects.filter(order=order__list)

        for items in order_item:
            count += items.quantity
            total_all += (items.price * items.quantity) + items.order.costtotal

        if request.method == "POST":
            bank_id = request.POST['bank_id']
            transfer_date = request.POST['datepicker']

            try:
                image = request.FILES['transfer_image']

            except KeyError:
                image = None

            order = Order.objects.get(pk=order__list)
            order.orderstatus_id = 2
            order.bank_id = bank_id
            order.transfer_date = transfer_date

            if image is not None:
                order.transfer_image = image
            order.save()
            messages.success(request, "แจ้งชำระสำเร็จ")
            return redirect('/my-account/orderhistory/')

    return render(request, 'store/orders/paymentapprove.html', {
        'order': order_list, 'order_item': order_item, 'count': count, 'cost': cost, 'total_all': total_all,
        'banks': banks
    })


@login_required(login_url='/login')
def update_tracking(request, order_id):  # ใส่ที่เลขติตตาม
    count = 0
    cost = 0
    total_all = 0

    order_list = Order.objects.get(order_id=order_id)
    order__list = order_list.id
    order_item = OrderItem.objects.filter(order=order__list)

    for items in order_item:
        count += items.quantity
        total_all += (items.price * items.quantity) + items.order.costtotal

        if request.method == "POST":
            ems = request.POST['ems']

            order = Order.objects.get(pk=order__list)
            order.orderstatus_id = 4
            order.transfer = ems
            order.save()
            messages.success(request, 'แจ้งเลขพัสดุเสร็จเรียบร้อย')
            return redirect(request.META['HTTP_REFERER'])

    return render(request, 'store/admin/updatetracking.html', {
        'order': order_list, 'order_item': order_item, 'count': count, 'cost': cost, 'total_all': total_all
    })


# เกี่ยวกับจัดการที่อยู่
@login_required(login_url='/login')
def save_address(request):
    if 'save' in request.POST:
        name = request.POST['name']
        email = request.POST['email']
        telephone = request.POST['telephone']
        address = request.POST['address']
        provinces = request.POST['province_id']
        amphures = request.POST['amphure_id']
        districts = request.POST['district_id']
        postcode = request.POST['zip_code']

        contract = Customer_contract.objects.create(
            user=request.user,
            name=name,
            email=email,
            telephone=telephone,
            address=address,
            provinces_id=provinces,
            amphures_id=amphures,
            districts_id=districts,
            postcode=postcode,

        )

        contract.save()
        messages.success(request, 'เพิ่มที่อยู่สำเร็จ')

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login')
def update_address(request):
    id = request.POST['id']
    name = request.POST['name']
    email = request.POST['email']
    telephone = request.POST['telephone']
    address_user = request.POST['address_user']
    provinces = request.POST['province_id']
    amphures = request.POST['amphure_id']
    districts = request.POST['district_id']
    postcode = request.POST['zip_code']

    address = Customer_contract.objects.get(pk=id)

    address.name = name
    address.email = email
    address.telephone = telephone
    address.address = address_user
    address.provinces_id = provinces
    address.amphures_id = amphures
    address.districts_id = districts
    address.postcode = postcode
    address.save()
    messages.success(request, 'แก้ไขที่อยู่สำเร็จ')

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login')
def delete_address(request, address_id):

    address = Customer_contract.objects.get(pk=address_id)
    address.delete()
    messages.success(request, 'ลบที่อยู่สำเร็จ')

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login')
def status_change(request, order_id):
    order_list = Order.objects.get(order_id=order_id)
    order__list = order_list.id

    order = Order.objects.get(pk=order__list)
    order.orderstatus_id = 3
    messages.success(request, 'ยืนยันการชำระเรียบร้อย')
    order.save()

    return redirect(request.META['HTTP_REFERER'])


# เกี่ยวกับตำบล,อำเภอ,จังหวัด
def load_amphures(request):
    provinces = request.GET.get('provinces_id')
    amphures = list(Amphures.objects.filter(
        province_id=provinces).order_by('-name_th').values())
    return JsonResponse({'data': amphures})


def load_districts(request):
    amphures = request.GET.get('amphures_id')
    districts = list(Districts.objects.filter(amphure_id=amphures).values())
    return JsonResponse({'data': districts})


@login_required(login_url='/login')
@permission_required('is_staff')
def dashboard(request):

    order_count = 0
    total = Order.objects.filter(
        orderstatus_id__gte=0).aggregate(sum=Sum('total'))['sum']  # gte คือ >=  nte คือ <=
    product = Product.objects.all().count()
    order_count = Order.objects.all().count()
    order_list = Order.objects.all()
    order_item = OrderItem.objects.all().values('product', 'price').annotate(
        sum_all=Sum('quantity')
    ).order_by('product')

    payload = {
        'orders': order_list,
        'products': product,
        'order_item': order_item,
        'order_count': order_count,
        'total': total,
    }

    return render(request, 'store/admin/dashboard2.html', {
        'payload': payload,
    }
    )


@login_required(login_url='/login')
@permission_required('is_staff')
def category(request):

    return render(request, 'store/admin/addcategory.html')


@permission_required('is_staff')
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        slug = request.POST['slug']

        category = Category.objects.create(
            name=name,
            slug=slug

        )
        category.save()
        messages.success(request, "เพิ่มข้อมูลสำเร็จ")
    return render(request, 'store/admin/addcategory.html')


@login_required(login_url='/login')
@permission_required('is_staff')
def product_manager(request):
    product = Product.objects.all()

    paginator = Paginator(product, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        product_Page = paginator.page(page)

    except (EmptyPage, InvalidPage):
        product_Page = paginator.page(
            paginator.num_pages)

    return render(request, 'store/admin/productmanager.html',
                  dict(products=product_Page))


@login_required(login_url='/login')
@permission_required('is_staff')
def search_product(request):
    serach = request.GET['product']
    serach_product = Product.objects.filter(name__icontains=serach)
    if not serach_product:

        messages.error(request, "ไม่พบชื่อสินค้าที่ค้นหา")

    return render(request, 'store/admin/productmanager.html', {'products': serach_product})


@login_required(login_url='/login')
@permission_required('is_staff')
def product(request):
    category = Category.objects.all()

    return render(request, 'store/admin/addproduct.html',

                  dict(categorys=category)

                  )


@permission_required('is_staff')
def add_product(request):
    name = request.POST['name']
    slug = request.POST['slug']
    sub_description = request.POST['sub_description']
    description = request.POST['description']
    price = request.POST['price']
    cost = request.POST['cost']
    image = request.FILES['image']
    stock = request.POST['stock']
    category = request.POST['category']

    product = Product.objects.create(
        name=name,
        slug=slug,
        sub_description=sub_description,
        description=description,
        price=price,
        cost=cost,
        stock=stock,
        image=image,
        available=True,
        category_id=category

    )
    product.save()
    messages.success(request, "เพิ่มข้อมูลสำเร็จ")
    return render(request, 'store/admin/addproduct.html'

                  )


@permission_required('is_staff')
def update_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        slug = request.POST['slug']
        sub_description = request.POST['sub_description']
        description = request.POST['description']
        price = request.POST['price']
        cost = request.POST['cost']

        try:
            image = request.FILES['image']
        except KeyError:
            image = None

        stock = request.POST['stock']
        category = request.POST['category']
        product = Product.objects.get(pk=id)
        product.name = name
        product.slug = slug
        product.sub_description = sub_description
        product.price = price
        product.stock = stock
        product.cost = cost

        if image is not None:
            product.image = image

        product.category_id = category

        product.save()
        messages.success(request, "แก้ไขสำเร็จ")

        return redirect('/admins/productall/')

    else:
        products = request.GET['product']
        product = Product.objects.filter(name=products)
        return render(request, 'store/admin/editproduct.html', {
            'products': product,
            'categorys': categories})


@permission_required('is_staff')
def delete_product(request):
    id = request.POST['id']
    product = Product.objects.get(pk=id)
    product.delete()
    messages.success(request, "ลบข้อมูลสำเร็จ")
    return redirect("/admins/productall/")


@login_required(login_url='/login')
@permission_required('is_staff')
def member(request):
    user = User.objects.filter(is_staff=0)

    paginator = Paginator(user, 5)  # 6:1 หน้า

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        user_page = paginator.page(page)

    except (EmptyPage, InvalidPage):
        user_page = paginator.page(
            paginator.num_pages)

    return render(request, 'store/admin/member.html', {
        'members': user_page
    })


@permission_required('is_staff')
def update_member(request):

    if request.method == 'POST':
        id = request.POST['id']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        status = request.POST['status']

        user = User.objects.get(pk=id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.is_active = status

        user.save()
        messages.success(request, "แก้ไขสำเร็จ")

        return redirect('/admins/members/')

    else:
        username = request.GET['username']
        name = User.objects.filter(username=username)
        return render(request, 'store/admin/editmember.html', {
            'members': name
        })


@permission_required('is_staff')
def delete_member(request):
    id = request.POST['id']
    print(id)
    user = User.objects.get(pk=id)
    user.delete()
    messages.success(request, "ลบข้อมูลสำเร็จ")
    return redirect("/admins/members/")


@login_required(login_url='/login')
@permission_required('is_staff')
def search_member(request):

    serach = request.GET['member']
    serach_member = User.objects.filter(
        first_name__icontains=serach, is_staff=0)
    if not serach_member:

        messages.error(request, "ไม่พบชื่อของลูกค้า กรุณาตรวจสอบอีกครั้ง !! ")

    return render(request, 'store/admin/member.html', {
        'members': serach_member
    })


# 404 and 500
def handler404(request, exception):
    return render(request, 'store/404error.html')  # 7


def handler500(request):
    return render(request, 'store/404error.html')  # 7
