from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.forms import Textarea
from .models import Producto, Categoria, Perfil_Usuario, Cliente, Tarjeta, Carrito, Producto_Carrito, Factura, \
    Mensaje_Cliente, DetalleFactura, MensajeProducto

from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    is_superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'username', 'is_superuser']


class UserClientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    is_superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'username']


class UserEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    is_superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'is_superuser']


class ProductoForm(forms.ModelForm):
    descripcion = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Producto
        fields = (
            'codigo', 'nombre', 'descripcion', 'descripcion_corta', 'imagen', 'stock', 'pvp', 'pvp_socio',
            'diferencia_en_tarjeta',
            'categoria', 'ean13')

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['stock'].widget.attrs['min'] = 0
        self.fields['pvp'].widget.attrs['min'] = 0
        self.fields['pvp_socio'].widget.attrs['min'] = 0


class CategoriaForm(forms.ModelForm):
    observaciones = forms.CharField(widget=Textarea, required=False)

    class Meta:
        model = Categoria
        fields = ('nombre', 'observaciones')


class ProfileForm(forms.ModelForm):
    telefono1 = forms.CharField(min_length=9, max_length=9)
    telefono2 = forms.CharField(min_length=9, max_length=9)
    portal = forms.IntegerField(min_value=0, max_value=999)
    piso = forms.IntegerField(min_value=0, max_value=999)

    class Meta:
        model = Perfil_Usuario
        fields = ('telefono2', 'telefono1', 'provincia', 'localidad', 'casa', 'piso', 'escalera', 'portal', 'direccion',
                  'tipo_via', 'cp', 'image', 'dni')


class ProfileEditForm(forms.ModelForm):
    telefono1 = forms.CharField(min_length=9, max_length=9)
    telefono2 = forms.CharField(min_length=9, max_length=9)
    portal = forms.IntegerField(min_value=0, max_value=999)
    piso = forms.IntegerField(min_value=0, max_value=999)

    class Meta:
        model = Perfil_Usuario
        fields = ('telefono2', 'telefono1', 'provincia', 'localidad', 'casa', 'piso', 'escalera', 'portal', 'direccion',
                  'tipo_via', 'cp', 'image')


class ClienteAddForm(forms.ModelForm):
    telefono1 = forms.CharField(min_length=9, max_length=9)
    telefono2 = forms.CharField(min_length=9, max_length=9)
    portal = forms.IntegerField(min_value=0, max_value=999)
    piso = forms.IntegerField(min_value=0, max_value=999)

    class Meta:
        model = Cliente
        fields = (
            'email', 'telefono2', 'telefono1', 'provincia', 'localidad', 'casa', 'piso', 'escalera', 'portal',
            'direccion',
            'tipo_via', 'cp', 'apellidos', 'nombre', 'dni', 'image')


class ClienteEditForm(forms.ModelForm):
    telefono1 = forms.CharField(min_length=9, max_length=9)
    telefono2 = forms.CharField(min_length=9, max_length=9)
    portal = forms.IntegerField(min_value=0, max_value=999)
    piso = forms.IntegerField(min_value=0, max_value=999)

    class Meta:
        model = Cliente
        fields = (
            'email', 'telefono2', 'telefono1', 'provincia', 'localidad', 'casa', 'piso', 'escalera', 'portal',
            'direccion',
            'tipo_via', 'cp', 'apellidos', 'nombre', 'image')


class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ('fecha_adquisicion', 'saldo_actual', 'cliente')


class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ('fecha_inicio', 'fecha_confirmacion', 'cliente')


class CarritoProductoForm(forms.ModelForm):
    importe_total = forms.CharField(disabled=True)
    cantidad = forms.IntegerField(min_value=0, required=True)

    class Meta:
        model = Producto_Carrito
        fields = ('cantidad', 'producto', 'carrito', 'importe_total')


class CarritoProductoAddForm(forms.ModelForm):
    class Meta:
        model = Producto_Carrito
        exclude = ('cantidad', 'importe_total', 'producto')


class CarritoProductoAdd2Form(forms.ModelForm):
    class Meta:
        model = Producto_Carrito
        fields = ('producto', 'cantidad')


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ('fecha', 'impuesto')


class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = (
        'prod_codigo', 'prod_categoria', 'prod_descripcion_corta', 'prod_nombre', 'prod_pvp')


class MensajeClienteForm(forms.ModelForm):
    mensaje = forms.CharField(widget=CKEditorUploadingWidget(), required=True)

    class Meta:
        model = Mensaje_Cliente
        fields = ('tipo_mensaje', 'mensaje')


class MensajeEmailForm(forms.ModelForm):
    mensaje = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Mensaje_Cliente
        fields = ('mensaje',)
