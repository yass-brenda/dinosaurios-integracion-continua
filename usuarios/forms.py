from django.forms import ModelForm,CharField,PasswordInput, ValidationError, TextInput
from .models import Cliente
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        exclude = ['usuario']


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput(attrs={'placeholder':'Escribe contraseña'}), label="Contraseña")
    password_re = CharField(widget=PasswordInput(attrs={'placeholder':'Repite contraseña'}), label="Repita contraseña")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email','password','password_re']


    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


    def clean_password(self, *args, **kwargs):
        if self.data['password'] != self.data['password_re']:
            raise ValidationError('Las contraseñas no son iguales', code='passwords_not_equals')
        return self.data['password']

class LoginForm(AuthenticationForm):
    username = CharField(widget=TextInput({'class':'form-control','placeholder':'Nombre de usuario'}))
    password = CharField(widget=PasswordInput({'class':'form-control','placeholder':'Contraseña'}))
    class Meta:
        fields = '__all__'
