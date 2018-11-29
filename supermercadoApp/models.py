import time
from django.db import models
from django.contrib.auth.models import User
from random import choice
from datetime import datetime

class Perfil_Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=9, unique=True)
    image = models.ImageField(upload_to='admin',default='',blank=True)
    cp = models.CharField(max_length=5)
    TIPO_VIA = (
        ('CALLE', 'CALLE'),
        ('AVENIDA', 'AVENIDA'),
        ('PLAZA', 'PLAZA')
    )
    tipo_via = models.CharField(max_length=10, choices=TIPO_VIA)
    direccion = models.CharField(max_length=200)
    portal = models.IntegerField()
    escalera = models.CharField(max_length=10, null=True, blank=True)
    piso = models.IntegerField()
    casa = models.CharField(max_length=10)
    localidad = models.CharField(max_length=200)
    provincia = models.CharField(max_length=200)
    telefono1 = models.CharField(max_length=9)
    telefono2 = models.CharField(max_length=9, null=True)
    token = models.CharField(('Token'), max_length=15, unique=True, db_index=True, null=True)


    def __str__(self):
        return self.dni + " - " + self.user.first_name + " " + self.user.last_name


    def set_token(self):
        self.token = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(15)])

    def save(self, *args, **kwargs):
        super(Perfil_Usuario, self).save(*args, **kwargs)
        self.set_token()



class Supermercado(models.Model):
    NIF = models.CharField(max_length=9,unique=True)
    responsable = models.CharField(max_length=200)
    direccion = models.CharField(max_length=4000)
    telefono1 = models.CharField(max_length=9)
    tiene_parking = models.BooleanField(default=False)


class Categoria(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    observaciones = models.CharField(max_length=4000,null=True,blank=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    dni = models.CharField(max_length=9, unique=True)
    image = models.ImageField(upload_to='cliente', default='cliente/default.png', blank=True)
    nombre = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=100)
    cp = models.CharField(max_length=5)
    TIPO_VIA = (
        ('CALLE', 'CALLE'),
        ('AVENIDA', 'AVENIDA'),
        ('PLAZA', 'PLAZA')
    )
    tipo_via = models.CharField(max_length=10,choices=TIPO_VIA)
    direccion = models.CharField(max_length=200)
    portal = models.IntegerField()
    escalera = models.CharField(max_length=10, null=True, blank=True, default="")
    piso = models.IntegerField()
    casa = models.CharField(max_length=10, default="")
    localidad = models.CharField(max_length=200)
    provincia = models.CharField(max_length=200)
    telefono1 = models.CharField(max_length=9)
    telefono2 = models.CharField(max_length=9, null=True)
    email = models.EmailField(default="",unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(('Token'), max_length=15, unique=True, db_index=True, null=True)

    def __str__(self):
        return self.dni + " - " + self.nombre + " " + self.apellidos

    def set_token(self):
        self.token = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(15)])

    def save(self, *args, **kwargs):
        super(Cliente, self).save(*args, **kwargs)
        self.set_token()

class Mensaje_Cliente(models.Model):
    cliente = models.ForeignKey(Cliente,null=True, on_delete=models.SET_NULL)
    TIPO_MENSAJE = (
        ('Opinión', 'Opinión'),
        ('Duda', 'Duda'),
        ('Sugerencia', 'Sugerencia'),
        ('Reclamación', 'Reclamación')
    )
    tipo_mensaje = models.CharField(max_length=11, choices=TIPO_MENSAJE, default=TIPO_MENSAJE[0][0])
    mensaje = models.CharField(max_length=1000)
    fecha = models.DateTimeField(default=datetime.now())



class Producto(models.Model):
    codigo = models.CharField(max_length=12,unique=True)
    nombre = models.CharField(max_length=120)
    descripcion = models.CharField(max_length=4000)
    descripcion_corta = models.CharField(max_length=250)
    imagen = models.ImageField(upload_to='productos',default='',blank=True)
    stock = models.IntegerField(default=0)
    pvp = models.FloatField(default=0)
    pvp_socio = models.FloatField(default=0)
    diferencia_en_tarjeta = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)
    ean13 = models.ImageField(upload_to='productos/ean13',default='', blank=True)

    def __str__(self):
        return self.nombre.upper()


class MensajeProducto(models.Model):
    mensaje = models.ForeignKey(Mensaje_Cliente,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, null=True, on_delete=models.DO_NOTHING)
    ESTADO_MENSAJE = (
        ('En espera', 'En espera'),
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
    )
    estado_mensaje = models.CharField(max_length=20, choices=ESTADO_MENSAJE, default=ESTADO_MENSAJE[0][0])

class Tarjeta(models.Model):
    num_tarjeta = models.CharField(max_length=50,default='0', unique=True)
    fecha_adquisicion = models.DateTimeField(default=datetime.now())
    saldo_actual = models.FloatField(default=0)
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)

    def set_num_tarjeta(self):
        self.num_tarjeta = int(time.mktime(datetime.today().timetuple())*1000)

    def save(self, *args, **kwargs):
        self.set_num_tarjeta()
        super(Tarjeta, self).save(*args, **kwargs)

class Carrito(models.Model):
    fecha_inicio = models.DateTimeField(default=datetime.now())
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return "Carrito: " + self.id.__str__()  + " | Cliente: " + self.cliente.dni


class Producto_Carrito(models.Model):
    cantidad = models.IntegerField(default=1)
    importe_total = models.FloatField(default=0)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)

    def set_importe_total(self):
        cliente = Cliente.objects.get(pk = self.carrito.cliente.pk)
        try:
            tieneTarjeta = Tarjeta.objects.get(cliente_id=cliente.id)
            producto = Producto.objects.get(pk=self.producto.id)
            if producto.pvp_socio!=0:
                self.importe_total = self.cantidad * producto.pvp_socio
            else:
                self.importe_total = self.cantidad * producto.pvp
        except:
            producto = Producto.objects.get(pk=self.producto.id)
            self.importe_total = self.cantidad * producto.pvp

    def updateImporteTotalProduct(self, *args, **kwargs):
        productoCarrito = Producto_Carrito.objects.get(producto=self.producto, carrito=self.carrito)
        productoCarrito.set_importe_total()
        super(Producto_Carrito, productoCarrito).save(*args, **kwargs)

    def updateProductoCarrito(self, *args, **kwargs):
        self.set_importe_total()
        super(Producto_Carrito, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.set_importe_total()
        try:
            productoCarrito = Producto_Carrito.objects.get(producto=self.producto, carrito=self.carrito)
            if (productoCarrito):
                productoCarrito.cantidad = productoCarrito.cantidad + self.cantidad
                productoCarrito.importe_total = productoCarrito.importe_total + self.importe_total
                super(Producto_Carrito, productoCarrito).save(*args, **kwargs)
        except:
            super(Producto_Carrito, self).save(*args, **kwargs)


class Factura(models.Model):
    codigo = models.CharField(max_length=40)
    cli_dni = models.CharField(max_length=9)
    cli_nombre = models.CharField(max_length=80)
    cli_apellidos = models.CharField(max_length=100)
    cli_cp = models.CharField(max_length=5)
    cli_tipo_via = models.CharField(max_length=50)
    cli_direccion = models.CharField(max_length=200)
    cli_portal = models.IntegerField()
    cli_escalera = models.CharField(max_length=10, null=True)
    cli_piso = models.IntegerField()
    cli_casa = models.CharField(max_length=10, null=True)
    cli_localidad = models.CharField(max_length=200)
    cli_provincia = models.CharField(max_length=200)
    cli_telefono1 = models.CharField(max_length=9)
    cli_telefono2 = models.CharField(max_length=9, null=True)
    cli_email = models.EmailField(default="")
    fecha = models.DateTimeField(default=datetime.now())
    subtotal = models.FloatField()
    impuesto = models.FloatField()
    importe_total = models.FloatField()
    cli_socio = models.IntegerField(default=0)
    cli_descuento = models.FloatField(default=0)


class DetalleFactura(models.Model):
    prod_codigo = models.CharField(max_length=12)
    prod_nombre = models.CharField(max_length=120)
    prod_descripcion_corta = models.CharField(max_length=250)
    prod_pvp = models.FloatField(default=0)
    prod_categoria = models.IntegerField()
    prod_cantidad = models.IntegerField()
    prod_iva = models.FloatField()
    prod_total = models.FloatField()
    factura = models.ForeignKey(Factura,on_delete=models.DO_NOTHING)




