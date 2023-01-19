from django import forms
from django.contrib.auth.models import User
from .models import  Carousel, Featuretts , Marketing
from django.contrib.auth.forms import AuthenticationForm 
'''
title
content
is_active
image

'''


class UserloginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autofocus': True, "class":"form-control"}),
                                                                       label='الاسم')
    password = forms.CharField(
        label="كلمة السر ",
        strip=False,
        widget=forms.PasswordInput(attrs={ "class":"form-control"}),
    )

    error_messages = {
        'invalid_login': "الرجاء التأكد من اسم المستخدم او كلمة السر  " ,
        'inactive': "هذا الحساب غير فعال .",
    }
    class Meta:
        model = User
        fields = ['username', 'password']#'u




class CarouselCreateForm(forms.ModelForm):
    title  = forms.CharField( max_length=100, widget=forms.TextInput( attrs={
                                         'placeholder': 'اختر عناون مناسب للدعاية' , "class":"form-control"}
                                          ), label='عنوان الدعاية المتحركة', )
    content  = forms.CharField(  widget=forms.Textarea( attrs={
                                         'placeholder': 'ادخل  تفاصيل   للدعاية',"class":"form-control" }
                                          ), label='التفاصيل', )
    # is_active  = forms.BooleanField( required = False, widget=forms.CheckboxInput( attrs={ "class":"form-control form-check-input"
    #                                      }
    #                                       ), label='عرض الدعاية', )
    image  =forms.ImageField(label='اختر صورة',required=True, error_messages = {'invalid':"ملف غير صالح"}, widget=forms.FileInput)
   
    class Meta:
        model =Carousel
        fields = ['title', 'content', 'image']
 

class FeaturettsCreateForm(forms.ModelForm):
    title  = forms.CharField( max_length=100, widget=forms.TextInput( attrs={
                                         'placeholder': 'اختر عناون مناسب للدعاية' , "class":"form-control"}
                                          ), label='عنوان الدعاية المتحركة', )
    content  = forms.CharField(  widget=forms.Textarea( attrs={
                                         'placeholder': 'ادخل  تفاصيل   للدعاية',"class":"form-control" }
                                          ), label='التفاصيل', )
    # is_active  = forms.BooleanField(required = False,  widget=forms.CheckboxInput( attrs={ "class":"form-control form-check-input"
    #                                      }
    #                                       ), label='عرض الدعاية', )
    image  =forms.ImageField(label='اختر صورة',required=True, error_messages = {'invalid':"ملف غير صالح"}, widget=forms.FileInput)
   
    class Meta:
        model =Featuretts
        fields = ['title', 'content',   'image']
 


class MarketingCreateForm(forms.ModelForm):
    title  = forms.CharField( max_length=100, widget=forms.TextInput( attrs={
                                         'placeholder': 'اختر عناون مناسب للدعاية' , "class":"form-control"}
                                          ), label='عنوان الدعاية المتحركة', )
    content  = forms.CharField(  widget=forms.Textarea( attrs={
                                         'placeholder': 'ادخل  تفاصيل   للدعاية',"class":"form-control" }
                                          ), label='التفاصيل', )
    # is_active  = forms.BooleanField( required = False, widget=forms.CheckboxInput( attrs={ "class":"form-control form-check-input"
    #                                      }
    #                                       ), label='عرض الدعاية', )
    image  =forms.ImageField(label='اختر صورة',required=True, error_messages = {'invalid':"ملف غير صالح"}, widget=forms.FileInput)
   
    class Meta:
        model =Marketing
        fields = ['title', 'content',   'image']
 












