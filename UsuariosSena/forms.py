from django import forms
from .models import (
    UsuariosSena,
    Prestamo,
    EntregaConsumible,
)
from django.forms import ModelForm


class UsuariosSenaForm(forms.ModelForm):
    class Meta:
        model = UsuariosSena
        fields = "__all__"


class UserLoginForm(forms.Form):
    numeroIdentificacion = forms.CharField(label="numeroIdentificacion")
    password = forms.CharField(widget=forms.PasswordInput, label="password")


class PrestamosForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = "__all__"


class EntregaConsumibleForm(forms.ModelForm):
    class Meta:
        model = EntregaConsumible
        fields = "__all__"
