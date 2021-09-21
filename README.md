# เว็บไซต์จัดการข่าวสารเกี่ยวกับวงการ Esport

https://esportshop.pythonanywhere.com/

- ADMIN
```
- ล็อกอินเข้าสู่ระบบในฐานะแอดมิน
- หน้า Dash board
- เพิ่ม,ลบ,แก้ไข สินค้า
- เพิ่ม,ลบ,แก้ไข ลูกค้า
- รายการสั่งซื้อ (ดูรายการสินค้าลูกค้า, จัดการสาถนะการส่งสินค้า, เพิ่มเลขติดตามสินค้า)
```

- Customer
```
- สมัครสมาชิก
- ล็อกอินเข้าสู่ระบบในฐานะลูกค้า
- เลือกสินค้าลงตะกร้า
- จัดการตะกร้าสินค้า
- เพิ่มและเลือกที่อยู่ในการจัดส่ง
- เลือกวิธีการชำระเงิน (บัตรเครดิต และ โอนชำระ)
- แจ้งชำระ (แนบรูปสลิป,ระบุวันที่โอนเงินเข้ามา)
- ประวัติการสั่งซื้อสินค้า (ดูสถานะการส่งสินค้า และ ดูข้อมูลรายการสินค้าที่สั่ง , ปริ้นใบเสร็จ)
```
  
## **เทคโนโลยีที่ใช้พัฒนา**
```
Django Framework
Bootstrap 4
MySQL
```


## **การติดตั้งโปรเจคเริ่มต้น**
```
mkvirtualenv (ชื่อ env)
workon (ชื่อ env ที่มีการสร้าง)
pip install django
pip install mysqlclient
pip install pillow
django-admin startproject ชื่อโปรเจค
python manage.py startapp ชื่อapp
```


## **ติดตั้ง module เสริม เกี่ยวกับ texteditor**
```
pip install django-wysiwyg
pip install django-ckeditor
pip install stripe-django
pip install django-crispy-forms

INSTALLED_APPS = [
    'ckeditor',
    'django_wysiwyg',
    'crispy_forms',
    'stripe'
]
```


## **จัดการ Data base**
  1) ทำการ dump ข้อมูลจากไฟล์ database ลงในฐานข้อมูลให้ครบก่อน
  2) database จะเกี่ยวกับ จังหวัด ,อำเภอ ,ตำบล ,สถานะการชำระเงิน ,ธนาคาร ,สถานะของสินค้า
  3) ใช้คำสั้งนี้ทุกครั้งเมือมีการ update database(models)
  
```
python manage.py makemigrations
python manage.py migrate
```

## **คำสั่งสร้าง Admin**
```
python manage.py createsuperuser
```

## **Run server**
  - เข้า virtaulenv ที่สร้างก่อนรัน server ทุกครั้ง ด้วยคำสั่ง
```
workon (ชื่อ env ที่มีการสร้าง)
python manage.py runserver
```
