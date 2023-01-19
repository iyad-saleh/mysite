from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Node, Profile


class Password_Form(PasswordChangeForm):
    old_password = forms.CharField(label="كلمة السرالقديمة ", strip=False, widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                   error_messages={'password_incorrect': "كلمة السر غير صحيحة."})
    new_password1 = forms.CharField(label="كلمة السر الجديدة", strip=False, widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                    error_messages={'password_too_short': 'كلمة السر قصيرة ', 'password_too_similar': 'اختر كلمة غير شبيهة بالاسم'})
    new_password2 = forms.CharField(label="تأكيد كلمة السر", strip=False, widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                    error_messages={'password_too_short': 'كلمة السر قصيرة ', 'password_too_similar': 'اختر كلمة غير شبيهة بالاسم'})

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'ادخل  اسم مميز  احرف عربية او انكليزية  او ارقام من دون فراغات '}), label='اسم المستخدم')

    # email    =forms.EmailField(max_length=100, widget=forms.TextInput(attrs={ "class":"form-control"}), label='البريد الإلكتروني')

    password1 = forms.CharField(label="كلمة السر ", strip=False, widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                error_messages={'password_too_short': 'كلمة السر قصيرة ', 'password_too_similar': 'اختر كلمة غير شبيهة بالاسم'})

    password2 = forms.CharField(label="تأكيد كلمة السر", strip=False,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}),)
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}),  label='الاسم')

    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}), label='الشهرة')
    error_messages = {
        'password_mismatch': "كلمتا السر غير متطابقتان ",
        "username_exists": "هذا الاسم مستخدم "
    }

    class Meta:
        model = User
        fields = ['username', 'password1',
                  'password2', 'first_name', 'last_name']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}), label='اسم المستخدم')
    # email    =forms.EmailField(max_length=100, widget=forms.TextInput(attrs={ "class":"form-control"}), label='البريد الإلكتروني')
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}),  label='الاسم')
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}), label='الشهرة')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class ParentForm(forms.ModelForm):
    parent = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                             "class": "form-control", "placeholder": " ادخل اول حرفين من اسم المستحدم او اسمه الاول "}), label='اسم الصديق')
    user_id = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"type": "hidden", "class": "form-control"}))

    class Meta:
        model = Node
        fields = ['parent', "user_id"]


class ProfileUpdateForm(forms.ModelForm):
    father = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": 'الاب'}), label='اسم الأب')
    mather = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": 'الام'}), label='اسم الأم')
    nationalNumber = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": 'الرقم الوطني من الهوية'}), label='الرقم الوطني')
    entry = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}), label='القيد ')
    town = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}), label='الأمانة')
    date_Grants = forms.DateField(widget=forms.DateInput(

        format=('%Y-%m-%d'), attrs={"class": "form-control", 'type': 'date'}), input_formats=('%Y-%m-%d', ),  label='تاريخ منح الهوية')
    inheritor = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}), label='اسم الوريث')
    tele = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}), label='رقم الهاتف او الموبايل ')

    birth_date = forms.DateField(widget=forms.DateInput(format=(
        '%Y-%m-%d'), attrs={"class": "form-control", 'type': 'date'}), input_formats=('%Y-%m-%d', ), label='تاريخ الميلاد')
    country_birth = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": 'بأي دولة'}), label='مكان الولادة')
    city_birth = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": '  مدينة  الولادة'}), label='المدينة')
    town_birth = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": '  المنطقة  الولادة'}), label='المنطقة')
    country_address = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': ' مقيم حاليا في دولة '}), label='عنوان السكن')
    city_address = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': ' مقيم في مدينة '}), label='المدينة')
    town_address = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'مقيم في منطقة او ناحية '}), label='المنطقة')
    country_Shipping = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'بأي دولة للشحن'}), label='عنوان الشحن')
    city_Shipping = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'بأي مدينة للشحن'}), label='المدينة')
    town_Shipping = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'بأي منطقة للشحن'}), label='المنطقة')
    street_Shipping = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'بأي شارع للشحن'}), label='الشارع')
    # parent   =forms.CharField(max_length=100, widget=forms.TextInput(attrs={ "class":"form-control"}), label='اسم المعرًف')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.Notrequired:
            self.fields[field].required = False

    class Meta:
        model = Profile
        fields = ['father', 'mather', 'tele', 'nationalNumber',
                  'entry', 'town', 'date_Grants', 'inheritor', 'birth_date',
                  'country_birth', 'city_birth', 'town_birth', 'country_address',
                  'city_address', 'town_address', 'country_Shipping',
                  'city_Shipping', 'town_Shipping', 'street_Shipping']  # 'user_permissions',,'parent'
        Notrequired = ('town_address', 'country_Shipping',
                       'city_Shipping', 'town_Shipping', 'street_Shipping')


class NodeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control"}), label='كلمة سر الخزنة')

    class Meta:
        model = Node
        fields = ['password']


class ChooseForm(forms.ModelForm):
    user = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}), label='اسم الصديق')
    user_id = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"type": "hidden", "class": "form-control"}))
    amount = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'type': "number", "class": "form-control"}), label='المبلغ المراد تحويله')
    amount1 = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'type': "number", "class": "form-control"}), label='تأكيد المبلغ  ')

    class Meta:
        model = Node
        fields = ['user', 'amount', 'amount1', 'user_id']


class ChooseRootForm(forms.ModelForm):
    user = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}), label='اسم الصديق')
    user_id = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"type": "hidden", "class": "form-control"}))
    amount = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'type': "number", "class": "form-control"}), label='المبلغ المراد تحويله')
    amount1 = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'type': "number", "class": "form-control"}), label='تأكيد المبلغ  ')

    class Meta:
        model = Node
        fields = ['user', 'amount', 'amount1', 'user_id']
