from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Perfil_Usuario)
admin.site.register(Supermercado)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Tarjeta)
admin.site.register(Cliente)
admin.site.register(Carrito)
admin.site.register(Producto_Carrito)
admin.site.register(Mensaje_Cliente)
admin.site.register(Factura)

