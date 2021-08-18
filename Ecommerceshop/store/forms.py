from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm #ผูกข้อมูล Model user กับ form (databinding) ** ยัดข้อมูล user 

class SignUpForm(UserCreationForm): #สร้างข้อมูลของ user
    first_name = forms.CharField(max_length=100,required=True,label="ชื่อจริง")
    last_name = forms.CharField(max_length=100,required=True,label="นามสกุล")
    email = forms.EmailField(max_length=250,help_text="example@gmail.com",required=True)

    class Meta:
        model = User
        fields=('first_name','last_name','username','password1','password2','email')
