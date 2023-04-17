from .models import *
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# class RequestForm(ModelForm):
#     class Meta:
#         model = Request
#         fields = '__all__'
#         exclude = ['user', 'created']

class UniqueTextForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user', 'created_at', 'transaction_id', 'complete', 'price', 'type','rawfile']

class UniqueFileForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user', 'created_at', 'transaction_id', 'complete', 'price', 'type','rawtext']

# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username',  'email', 'avatar', 'bio' , 'name', ]


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)




class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)
class ContactForm(ModelForm):
    class Meta:
        model = Contact_us
        fields = '__all__'
        exclude = ['email', 'created_at', 'user']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

