import time,json
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from .forms import *
from .models import Mensaje_Cliente,MensajeProducto
from django.contrib.auth import login, logout
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Supermercado.settings import PRODUCTOS_POR_PAGINA
from django.core.mail import EmailMessage


########    INICIO CLIENTE     #########
def view_index(request):
    try:
        cliente = Cliente.objects.get(pk=request.session['id_cli'])
        request.session['cli_nombre'] = cliente.nombre
        request.session['cli_apellidos'] = cliente.apellidos
        request.session['cli_imageprofile'] = str(cliente.image)
        request.session['cli_navbar_active'] = "inicio"
        productosInteres = Producto.objects.raw("select * from supermercadoApp_producto where pvp_socio > 0 order by RAND() LIMIT 4 ")
        opiniones = MensajeProducto.objects.raw("select * from supermercadoApp_mensajeproducto where estado_mensaje like 'Aceptado' LIMIT 8")
        categorias = Categoria.objects.all()
        context = {"categorias": categorias,"opiniones":opiniones,"productosInteres":productosInteres}
        return render(request, 'supermercado/public/index.html', context)
    except:
        categorias = Categoria.objects.all()
        productosInteres = Producto.objects.raw("select * from supermercadoApp_producto order by RAND() LIMIT 4 ")
        opiniones = MensajeProducto.objects.raw("select * from supermercadoApp_mensajeproducto where estado_mensaje like 'Aceptado' LIMIT 8")
        context = {"categorias": categorias, "opiniones": opiniones,"productosInteres":productosInteres}
        request.session['cli_navbar_active'] = "inicio"
        return render(request, "supermercado/public/index.html", context)


def logout_cli(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


########    REGISTRO Y EDICION CLIENTE     #########
def view_register(request):
    try:
        var = request.session['id_cli']
        request.session['cli_navbar_active'] = "inicio"
        categorias = Categoria.objects.all()
        context = {"categorias": categorias}
        return render(request, "supermercado/public/index.html",context)
    except:
        categorias = Categoria.objects.all()
        form = LoginForm()
        context = {"form": form,"categorias": categorias}
        request.session['cli_navbar_active'] = "inicio"
        return render(request, "supermercado/public/customer-register.html", context)


def view_cliente_menu(request):
    try:
        var = request.session['id_cli']
        cliente = Cliente.objects.get(pk = var)
        facturas = Factura.objects.filter(cli_dni=cliente.dni)
        request.session['cli_navbar_active'] = "carrito"
        categorias = Categoria.objects.all()
        context = {"categorias": categorias,"facturas":facturas}
        return render(request, "supermercado/public/cliente-menu.html",context)
    except:
        categorias = Categoria.objects.all()
        form = LoginForm()
        context = {"form": form,"categorias": categorias}
        request.session['cli_navbar_active'] = "inicio"
        return render(request, "supermercado/public/customer-register.html", context)

def view_cliente_register(request):
    try:
        var = request.session['id_cli']
        request.session['cli_navbar_active'] = "inicio"
        categorias = Categoria.objects.all()
        context = {"categorias": categorias}
        return render(request, "supermercado/public/index.html", context)
    except:
        form = ClienteAddForm(prefix='cliente')
        formUser = UserClientForm(prefix='register')
        request.session['cli_navbar_active'] = "inicio"
        categorias = Categoria.objects.all()
        context = {"form": form, "formUser": formUser, "categorias": categorias}
        return render(request, "supermercado/public/cliente-register.html", context)


def view_cliente_edit(request):
    try:
        id_usuario = request.session['id_usr']
        id_cliente = request.session['id_cli']
        try:
            tarjeta = Tarjeta.objects.get(cliente_id=id_cliente)
            request.session['cli_navbar_active'] = "inicio"
            user = User.objects.get(pk=id_usuario)
            cliente = Cliente.objects.get(user_id=user.id)
            form = ClienteEditForm(prefix='cliente', instance=cliente)
            formUser = UserEditForm(prefix='register', instance=user)
            categorias = Categoria.objects.all()
            context = {"form": form, "formUser": formUser, "categorias": categorias,"tarjeta":tarjeta}
            return render(request, 'supermercado/public/cliente-edit.html', context)
        except:
            tarjeta = None
            request.session['cli_navbar_active'] = "inicio"
            user = User.objects.get(pk=id_usuario)
            cliente = Cliente.objects.get(user_id=user.id)
            form = ClienteEditForm(prefix='cliente', instance=cliente)
            formUser = UserEditForm(prefix='register', instance=user)
            categorias = Categoria.objects.all()
            context = {"form": form, "formUser": formUser, "categorias": categorias,"tarjeta":tarjeta}
            return render(request, 'supermercado/public/cliente-edit.html', context)
    except:
        request.session['cli_navbar_active'] = "inicio"
        categorias = Categoria.objects.all()
        context = {"categorias": categorias}
        return render(request, 'supermercado/public/index.html', context)


def add_cliente(request):
    clienteForm = ClienteAddForm(request.POST, request.FILES, prefix='cliente')
    register = UserForm(request.POST, prefix='register')
    if register.is_valid() and clienteForm.is_valid():
        if Cliente.objects.filter(dni__iexact=clienteForm.cleaned_data['email']):
            register.add_error('email', 'El email ya existe')
            context = {"form": clienteForm, "formUser": register}
            return render(request, 'supermercado/public/cliente-register.html', context)
        user = register.save()
        cliente = clienteForm.save(commit=False)
        cliente.user = user
        cliente.save()
        user = User.objects.get(cliente__dni=clienteForm.cleaned_data['dni'])
        user.set_password(register.cleaned_data['password'])
        user.is_staff = False
        user.save()
        request.session['isA'] = 0
        request.session['id_usr'] = user.id
        request.session['id_cli'] = cliente.id
        request.session['cli_nombre'] = cliente.nombre
        request.session['cli_apellidos'] = cliente.apellidos
        request.session['cli_imageprofile'] = str(cliente.image)
        login(request, user)
        carrito = Carrito(fecha_inicio=datetime.now(), cliente_id=cliente.id)
        carrito.save()
        categorias = Categoria.objects.all()
        context = {"categorias": categorias}
        return render(request, 'supermercado/public/index.html', context)
    else:
        categorias = Categoria.objects.all()
        context = {"form": clienteForm, "formUser": register,"categorias": categorias}
        return render(request, 'supermercado/public/cliente-register.html', context)


def edit_cliente(request):
    if request.method == "POST":
        id_usuario = request.session['id_usr']
        clienteForm = ClienteEditForm(request.POST, request.FILES, prefix='cliente')
        formUser = UserEditForm(request.POST, prefix='register')
        user = User.objects.get(pk=id_usuario)
        if formUser.__getitem__('password').value() is not "":
            user.set_password(formUser.__getitem__('password').value())
        user.save()
        cliente = Cliente.objects.get(user=user)
        cliente.nombre = clienteForm.__getitem__('nombre').value()
        cliente.apellidos = clienteForm.__getitem__('apellidos').value()
        cliente.cp = clienteForm.__getitem__('cp').value()
        cliente.tipo_via = clienteForm.__getitem__('tipo_via').value()
        cliente.direccion = clienteForm.__getitem__('direccion').value()
        cliente.portal = clienteForm.__getitem__('portal').value()
        cliente.escalera = clienteForm.__getitem__('escalera').value()
        cliente.piso = clienteForm.__getitem__('piso').value()
        cliente.casa = clienteForm.__getitem__('casa').value()
        cliente.localidad = clienteForm.__getitem__('localidad').value()
        cliente.provincia = clienteForm.__getitem__('provincia').value()
        if clienteForm.__getitem__('telefono1').value().__len__() < 9:
            messages.error(request, 'El número de teléfono 1 no tiene 9 dígitos')
            context = {"form": clienteForm, "formUser": formUser, "id_usuario": id_usuario, "id_cliente": cliente.id,
                       "cliente": cliente}
            return render(request, 'supermercado/public/cliente-edit.html', context)
        if clienteForm.__getitem__('telefono2').value().__len__() < 9:
            messages.error(request, 'El número de teléfono 2 no tiene 9 dígitos')
            context = {"form": clienteForm, "formUser": formUser, "id_usuario": id_usuario, "id_cliente": cliente.id,
                       "cliente": cliente}
            return render(request, 'supermercado/public/cliente-edit.html', context)
        cliente.telefono1 = clienteForm.__getitem__('telefono1').value()
        cliente.telefono2 = clienteForm.__getitem__('telefono2').value()
        email = clienteForm.__getitem__('email').value()
        try:
            usuario = Cliente.objects.get(email=email)
            if (cliente.email == email):
                cliente.email = email
            else:
                categorias = Categoria.objects.all()
                messages.error(request, 'El email ya existe')
                context = {"form": clienteForm, "formUser": formUser, "id_usuario": id_usuario,
                           "id_cliente": cliente.id,
                           "cliente": cliente,"categorias": categorias}
                return render(request, 'supermercado/public/cliente-edit.html', context)
        except ObjectDoesNotExist:
            cliente.email = email
        cliente.email = clienteForm.__getitem__('email').value()
        if clienteForm.__getitem__('image').value() == False:
            cliente.image.delete()
            cliente.image = ""
        elif str(clienteForm.__getitem__('image').value()) != "cliente/default.png":
            cliente.image.delete()
            cliente.image = clienteForm.__getitem__('image').value()
        cliente.save()
        request.session['cli_imageprofile'] = str(cliente.image)
        return HttpResponseRedirect(reverse("cli_menu"))


########    CARRITO COMPRA CLIENTE     #########

def view_carrito_compra(request):
    try:
        cliente = Cliente.objects.get(pk=request.session['id_cli'])
        # Comprobamos si tiene algun carrito
        try:
            carritos = Carrito.objects.filter(cliente=cliente)
            existeCarritoSinConfirmar = False
            for carrito in carritos:
                if carrito.fecha_confirmacion is None:
                    existeCarritoSinConfirmar = True
            if existeCarritoSinConfirmar:  # si existe, le mostramos el carrito
                try:
                    productos_carrito = Producto_Carrito.objects.filter(carrito=carrito)
                    productoExcluir = '0'
                    for producto in productos_carrito:
                        productoExcluir = productoExcluir + ',' + (str(producto.producto.codigo))

                    suma = 0
                    for producto in productos_carrito:
                        suma = suma + producto.importe_total
                    tasa = 10
                    totalCompra = suma + ((suma * tasa) / 100)
                    productosInteres = Producto.objects.raw(
                        "select * from supermercadoApp_producto where codigo not in (" + productoExcluir + ") order by RAND() LIMIT 3 ")
                    try:
                        tarjetaCliente = Tarjeta.objects.get(cliente=cliente)
                        categorias = Categoria.objects.all()
                        context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa,
                                   "totalCompra": totalCompra,
                                   "productosInteres": productosInteres, "tarjeta": tarjetaCliente,"categorias": categorias}
                        request.session['cli_navbar_active'] = "carrito"
                        return render(request, 'supermercado/public/compras-carrito.html', context)
                    except:
                        categorias = Categoria.objects.all()
                        context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa,
                                   "totalCompra": totalCompra,
                                   "productosInteres": productosInteres,"categorias": categorias}
                        request.session['cli_navbar_active'] = "carrito"
                        return render(request, 'supermercado/public/compras-carrito.html', context)
                except:
                    request.session['cli_navbar_active'] = "tienda"
                    return HttpResponseRedirect(reverse('cli_tienda'))
            else:  # sino, se le crea uno y se va al index
                carrito = Carrito(fecha_inicio=datetime.now(), cliente_id=cliente.id)
                carrito.save()
                categorias = Categoria.objects.all()
                context = {"categorias": categorias}
                return render(request, 'supermercado/public/index.html', context)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse("index"))
    except:
        form = LoginForm()
        categorias = Categoria.objects.all()
        context = {"form": form,"categorias": categorias}
        request.session['cli_navbar_active'] = "inicio"
        return render(request, "supermercado/public/customer-register.html", context)


def update_producto_carrito(request, id_producto_carrito, id_carrito):
    cliente = Cliente.objects.get(pk=request.session['id_cli'])
    carrito = Carrito.objects.get(pk = id_carrito)
    producto_carrito = Producto_Carrito.objects.get(pk = id_producto_carrito)
    producto = Producto.objects.get(pk=producto_carrito.producto.id)
    producto_origen = Producto.objects.get(pk=producto.id)
    if producto_origen.stock > int(request.POST['cantidad']):
        if producto_carrito.cantidad < int(request.POST['cantidad']):
            producto_origen.stock = producto_origen.stock - (int(request.POST['cantidad']) - producto_carrito.cantidad)
        elif producto_carrito.cantidad > int(request.POST['cantidad']):
            producto_origen.stock = producto_origen.stock + (producto_carrito.cantidad - int(request.POST['cantidad']))
        producto_origen.save()
        producto_carrito.cantidad = int(request.POST['cantidad'])
        producto_carrito.updateProductoCarrito()
        productos_carrito = Producto_Carrito.objects.filter(carrito=carrito)
        productoExcluir = '0'
        for producto in productos_carrito:
            productoExcluir = productoExcluir + ',' + (str(producto.producto.codigo))

        suma = 0
        for producto in productos_carrito:
            suma = suma + producto.importe_total
        tasa = 10
        totalCompra = suma + ((suma * tasa) / 100)
        productosInteres = Producto.objects.raw(
            "select * from supermercadoApp_producto where codigo not in (" + productoExcluir + ") order by RAND() LIMIT 3")
        try:
            tarjetaCliente = Tarjeta.objects.get(cliente=cliente)
            categorias = Categoria.objects.all()
            context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa,
                       "totalCompra": totalCompra,
                       "productosInteres": productosInteres, "tarjeta": tarjetaCliente, "categorias": categorias}
            request.session['cli_navbar_active'] = "carrito"
            return render(request, 'supermercado/public/compras-carrito.html', context)
        except:
            categorias = Categoria.objects.all()
            context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa,
                       "totalCompra": totalCompra,
                       "productosInteres": productosInteres, "categorias": categorias}
            request.session['cli_navbar_active'] = "carrito"
            return render(request, 'supermercado/public/compras-carrito.html', context)
    if producto_origen.stock < int(request.POST['cantidad']):
        productos_carrito = Producto_Carrito.objects.filter(carrito=carrito)
        productoExcluir = '0'
        for producto in productos_carrito:
            productoExcluir = productoExcluir + ',' + (str(producto.producto.codigo))

        suma = 0
        for producto in productos_carrito:
            suma = suma + producto.importe_total
        tasa = 10
        totalCompra = suma + ((suma * tasa) / 100)
        productosInteres = Producto.objects.raw(
            "select * from supermercadoApp_producto where codigo not in (" + productoExcluir + ") order by RAND() LIMIT 3")
        try:
            tarjetaCliente = Tarjeta.objects.get(cliente=cliente)
            categorias = Categoria.objects.all()
            context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa,
                       "totalCompra": totalCompra,
                       "productosInteres": productosInteres, "tarjeta": tarjetaCliente, "categorias": categorias}
            request.session['cli_navbar_active'] = "carrito"
            messages.error(request,'La cantidad indicada no es posible. Actualmente no disponemos tanto stock. Disculpa las molestias.')
            return render(request, 'supermercado/public/compras-carrito.html', context)
        except:
            categorias = Categoria.objects.all()
            context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa,
                       "totalCompra": totalCompra,
                       "productosInteres": productosInteres, "categorias": categorias}
            request.session['cli_navbar_active'] = "carrito"
            messages.error(request, 'La cantidad indicada no es posible. Actualmente no disponemos tanto stock. Disculpa las molestias.')
            return render(request, 'supermercado/public/compras-carrito.html', context)
    if int(request.POST['cantidad']) == 0:
        productos_carrito = Producto_Carrito.objects.filter(carrito=carrito)
        productoExcluir = '0'
        for producto in productos_carrito:
            productoExcluir = productoExcluir + ',' + (str(producto.producto.codigo))

        suma = 0
        for producto in productos_carrito:
            suma = suma + producto.importe_total
        tasa = 10
        totalCompra = suma + ((suma * tasa) / 100)
        productosInteres = Producto.objects.raw(
            "select * from supermercadoApp_producto where codigo not in (" + productoExcluir + ") order by RAND() LIMIT 3")
        try:
            tarjetaCliente = Tarjeta.objects.get(cliente=cliente)
            categorias = Categoria.objects.all()
            context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa,
                       "totalCompra": totalCompra,
                       "productosInteres": productosInteres, "tarjeta": tarjetaCliente, "categorias": categorias}
            request.session['cli_navbar_active'] = "carrito"
            return render(request, 'supermercado/public/compras-carrito.html', context)
        except:
            categorias = Categoria.objects.all()
            context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa,
                       "totalCompra": totalCompra,
                       "productosInteres": productosInteres, "categorias": categorias}
            request.session['cli_navbar_active'] = "carrito"
            return render(request, 'supermercado/public/compras-carrito.html', context)


def delete_producto_carrito(request, id_producto_carrito):
    request.session['cli_navbar_active'] = "carrito"
    producto_carrito = Producto_Carrito.objects.get(pk=id_producto_carrito)
    producto = Producto.objects.get(pk=producto_carrito.producto.id)
    producto.stock = producto.stock + producto_carrito.cantidad
    producto.save()
    producto_carrito.delete()
    request.session['cli_carrito_cantidad'] = int(request.session['cli_carrito_cantidad']) - 1
    return HttpResponseRedirect(reverse("cli_carrito"))


########    TIENDA COMPRAS CLIENTE     #########
def view_tienda(request):
    todos_los_productos = Producto.objects.all()
    pagina = request.GET.get('pagina', 1)
    paginator = Paginator(todos_los_productos, PRODUCTOS_POR_PAGINA)
    try:
        productosPaginar = paginator.page(pagina)
    except PageNotAnInteger:
        productosPaginar = paginator.page(1)
    except EmptyPage:
        productosPaginar = paginator.page(paginator.num_pages)
    categoriaEscogida = None
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    context = {"categorias": categorias, "productos": productos, "productosPaginar":productosPaginar,"categoriaEscogida":categoriaEscogida}
    request.session['cli_navbar_active'] = "tienda"
    return render(request, "supermercado/public/tienda-categorias-left.html", context)


def tienda_autocompletaBusqueda(request):
    datos = request.GET
    contenido = datos.get('term')
    if contenido:
        productos = Producto.objects.filter(nombre__contains=contenido)
    else:
        productos = Producto.objects.all()

    resultados = []
    for producto in productos:
        item_json = {}
        # Valor por defecto si no se implementa la opción de renderizado en jQuery
        item_json['label'] = producto.nombre
        item_json['nombre'] = producto.nombre
        item_json['descripcion_corta'] = producto.descripcion_corta
        item_json['imagen'] = str(producto.imagen)
        item_json['ident'] = producto.id
        resultados.append(item_json)

    datos = json.dumps(resultados)
    mimetype = 'application/json'
    return HttpResponse(datos, mimetype)


def view_tienda_by_categoria(request,id_categoria):
    todos_los_productos = Producto.objects.filter(categoria_id=id_categoria)
    pagina = request.GET.get('pagina', 1)
    paginator = Paginator(todos_los_productos, PRODUCTOS_POR_PAGINA)
    try:
        productosPaginar = paginator.page(pagina)
    except PageNotAnInteger:
        productosPaginar = paginator.page(1)
    except EmptyPage:
        productosPaginar = paginator.page(paginator.num_pages)
    categoriaEscogida = Categoria.objects.get(pk = id_categoria)
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    context = {"categorias": categorias, "productos": productos,"productosPaginar":productosPaginar,"categoriaEscogida":categoriaEscogida}
    request.session['cli_navbar_active'] = "tienda"
    return render(request, "supermercado/public/tienda-categorias-left.html", context)


def view_producto_detalle(request,id_producto):
    productoDetalle = Producto.objects.get(pk = id_producto)
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    mensajesAceptados = MensajeProducto.objects.filter(estado_mensaje='Aceptado')
    mensajes = Mensaje_Cliente.objects.all()
    productosInteres = Producto.objects.raw(
        "select * from supermercadoApp_producto where codigo not in (" + productoDetalle.codigo + ") order by RAND() LIMIT 3")
    form = MensajeClienteForm()
    context = {"categorias": categorias, "productos": productos,"productoDetalle":productoDetalle,"productosInteres": productosInteres,"form":form,"mensajes":mensajes,"mensajesAceptados":mensajesAceptados}
    request.session['cli_navbar_active'] = "tienda"
    return render(request, "supermercado/public/producto-detalle.html", context)

def add_producto_carrito(request, id_producto):
    try:
        cliente = Cliente.objects.get(pk=request.session['id_cli'])
        if int(request.POST['cantidad']) == 0:
            messages.error(request, 'La cantidad indicada no es posible. Debe introducir minimo valor: 1')
            return HttpResponseRedirect(reverse('cli_producto_detalle', args=(id_producto,)))
        comprobarProducto = Producto.objects.get(pk=id_producto)
        if comprobarProducto.stock > 0 and int(request.POST['cantidad']) < comprobarProducto.stock:
                cliente = Cliente.objects.get(pk=request.session['id_cli'])
                carrito = Carrito.objects.get(pk = request.session['cli_carrito'])
                producto = Producto.objects.get(pk=id_producto)
                productosCarrito = Producto_Carrito.objects.filter(carrito_id=request.session['cli_carrito'])
                estaProducto = False
                for productocarrito in productosCarrito:
                    if productocarrito.producto.nombre == producto.nombre:
                        estaProducto = True
                        break
                if estaProducto == False:
                    request.session['cli_carrito_cantidad'] = int(request.session['cli_carrito_cantidad']) + 1
                producto_carrito = Producto_Carrito(producto=producto,
                                                    carrito_id=carrito.id,
                                                    cantidad=int(request.POST['cantidad']))
                producto_carrito.save()
                producto = Producto.objects.get(pk=id_producto)
                producto.stock = producto.stock - int(request.POST['cantidad'])
                producto.save()
                messages.success(request, 'Producto añadido correctamente')
                return HttpResponseRedirect(reverse('cli_producto_detalle', args=(id_producto,)))
        else:
            messages.error(request, 'Actualmente no disponemos tanto stock. Disculpa las molestias.')
            return HttpResponseRedirect(reverse('cli_producto_detalle', args=(id_producto,)))
    except:
        messages.info(request, 'Por favor, para poder comprar tienes que crearte una cuenta, no te llevará más de 1 minuto!')
        return HttpResponseRedirect(reverse('register'))


########    MENSAJES CLIENTE     #########

def cli_add_mensaje(request, id_producto):
    try:
        cliente = Cliente.objects.get(pk=request.session['id_cli'])
        form = MensajeClienteForm(request.POST)
        if form.is_valid():
            mensaje = Mensaje_Cliente(tipo_mensaje=form.__getitem__('tipo_mensaje').value(),
                            mensaje = form.cleaned_data['mensaje'],
                            fecha=datetime.now(),
                            cliente_id=cliente.id
                            )
            mensaje.save()
            MensajeProducto(mensaje_id=mensaje.id,producto_id=id_producto,estado_mensaje="En espera").save()
            productoDetalle = Producto.objects.get(pk=id_producto)
            productos = Producto.objects.all()
            categorias = Categoria.objects.all()
            productosInteres = Producto.objects.raw(
                "select * from supermercadoApp_producto where codigo not in (" + productoDetalle.codigo + ") order by RAND() LIMIT 3")
            form = MensajeClienteForm()
            context = {"categorias": categorias, "productos": productos, "productoDetalle": productoDetalle,
                       "productosInteres": productosInteres, "form": form}
            request.session['cli_navbar_active'] = "tienda"
            messages.info(request,"Tu mensaje se ha enviado con éxito. Muchas gracias!")
            return HttpResponseRedirect(reverse('cli_producto_detalle', args=(id_producto,)))
        else:
            productoDetalle = Producto.objects.get(pk=id_producto)
            productos = Producto.objects.all()
            categorias = Categoria.objects.all()
            productosInteres = Producto.objects.raw(
                "select * from supermercadoApp_producto where codigo not in (" + productoDetalle.codigo + ") order by RAND() LIMIT 3")
            form = MensajeClienteForm()
            context = {"categorias": categorias, "productos": productos, "productoDetalle": productoDetalle,
                       "productosInteres": productosInteres, "form": form}
            request.session['cli_navbar_active'] = "tienda"
            messages.info(request, 'Ha habido algún error. Por favor, intentalo más tarde.')
            return render(request, "supermercado/public/producto-detalle.html", context)
    except:
        productoDetalle = Producto.objects.get(pk=id_producto)
        productos = Producto.objects.all()
        categorias = Categoria.objects.all()
        productosInteres = Producto.objects.raw(
            "select * from supermercadoApp_producto where codigo not in (" + productoDetalle.codigo + ") order by RAND() LIMIT 3")
        form = MensajeClienteForm()
        context = {"categorias": categorias, "productos": productos, "productoDetalle": productoDetalle,
                   "productosInteres": productosInteres, "form": form}
        request.session['cli_navbar_active'] = "tienda"
        messages.info(request,'Para escribir una opinión tienes que iniciar sesión o crearte una cuenta')
        return render(request, "supermercado/public/producto-detalle.html", context)


########    TARJETA SOCIO CLIENTE     #########

def view_tarjetaSocio(request):
    comprobarTarjeta = None
    categorias = Categoria.objects.all()
    try:
        cli = request.session['cli_id']
        try:
            comprobarTarjeta = Tarjeta.objects.get(cliente_id=cli)
            request.session['cli_navbar_active'] = "inicio"
            context = {"tarjeta":comprobarTarjeta,"categorias": categorias}
            return render(request, 'supermercado/public/tarjeta-socio.html', context)
        except ObjectDoesNotExist:
            context = {"tarjeta": comprobarTarjeta,"categorias": categorias}
            request.session['cli_navbar_active'] = "inicio"
            return render(request, 'supermercado/public/tarjeta-socio.html', context)
    except:
        context = {"tarjeta":comprobarTarjeta,"categorias": categorias}
        request.session['cli_navbar_active'] = "inicio"
        return render(request, 'supermercado/public/tarjeta-socio.html',context)


def addTarjetaToCliente(request):
    try:
        cliente = Cliente.objects.get(pk=request.session['id_cli'])
        tarjeta = Tarjeta(fecha_adquisicion=datetime.now(), saldo_actual=0)
        cliente = Cliente.objects.get(pk=cliente.id)
        user = User.objects.get(cliente__dni=cliente.dni)
        id_usuario = user.id
        try:
            comprobarTarjeta = Tarjeta.objects.get(cliente_id=cliente.id)
            if comprobarTarjeta:
                messages.info(request,
                               "Ya dispones de una tarjeta socio. Aprovechala para tus compras ;-)")
                return HttpResponseRedirect(reverse('cli_view_edit'))
            else:
                tarjeta.cliente = cliente
                tarjeta.save()
                updateProductsCarritoCliente(request.session['cli_carrito'])
                messages.info(request, "Enhorabuena! Ya tienes asignada tu tarjeta socio! Puedes acceder a los datos de tu tarjeta en la seccion Tarjeta Socio.")
                return HttpResponseRedirect(reverse('cli_view_edit'))
        except ObjectDoesNotExist:
            tarjeta.cliente = cliente
            tarjeta.save()
            updateProductsCarritoCliente(request.session['cli_carrito'])
            messages.info(request,
                             "Enhorabuena! Ya tienes asignada tu tarjeta socio! Puedes acceder a los datos de tu tarjeta en la seccion Tarjeta Socio.")
            return HttpResponseRedirect(reverse('cli_view_edit'))
    except:
        messages.info(request,
                      'Por favor, para poder disponer de una tarjeta socio tienes que crearte una cuenta, no te llevará más de 1 minuto!')
        return HttpResponseRedirect(reverse('cli_view_edit'))


def updateProductsCarritoCliente(id_carrito):
    productos = Producto_Carrito.objects.filter(carrito_id=id_carrito)
    for producto in productos:
        producto.updateImporteTotalProduct()


########    PROCEDER PAGO CLIENTE     #########

def view_procederCompra(request):
    try:
        cliente = Cliente.objects.get(pk=request.session['id_cli'])
        # Comprobamos si tiene algun carrito
        try:
            carrito = Carrito.objects.get(pk = int(request.session['cli_carrito']))
            saldoDescontado = 0.0
            request.session['saldo_descontar'] = 0
            if int(request.POST['descontar']) == 1:
                request.session['cli_descontar'] = 1
                try:
                    tarjeta = Tarjeta.objects.get(cliente_id=carrito.cliente.id)
                    productos_carrito = Producto_Carrito.objects.filter(carrito=carrito)
                    suma = 0.0
                    for producto in productos_carrito:
                        suma = suma + producto.importe_total
                    tasa = 10.0
                    if suma > tarjeta.saldo_actual:
                        saldoDescontado = tarjeta.saldo_actual
                    else:
                        saldoDescontado = suma
                    request.session['saldo_descontar'] = saldoDescontado
                    totalCompra = suma - saldoDescontado
                    if totalCompra > 0:
                        totalCompra = totalCompra + ((totalCompra * tasa) / 100)
                    categorias = Categoria.objects.all()
                    context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa, "tarjeta":tarjeta,
                               "totalCompra": totalCompra, "subtotal":suma - saldoDescontado,
                               "categorias": categorias}
                    request.session['total_compra'] = totalCompra
                    request.session['cli_navbar_active'] = "carrito"
                    return render(request, 'supermercado/public/proceder-pago.html', context)
                except:
                    categorias = Categoria.objects.all()
                    context = {"categorias": categorias}
                    request.session['cli_navbar_active'] = "carrito"
                    return render(request, "supermercado/public/tienda-categorias-left.html", context)
            else:
                request.session['cli_descontar'] = 0
                try:
                    tarjeta = Tarjeta.objects.get(cliente_id=carrito.cliente.id)
                    productos_carrito = Producto_Carrito.objects.filter(carrito=carrito)
                    suma = 0
                    for producto in productos_carrito:
                        suma = suma + producto.importe_total
                    tasa = 10
                    totalCompra = suma + ((suma * tasa) / 100)
                    categorias = Categoria.objects.all()
                    context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa, "tarjeta":tarjeta, "subtotal":suma - saldoDescontado,
                               "totalCompra": totalCompra,
                               "categorias": categorias}
                    request.session['cli_navbar_active'] = "carrito"
                    return render(request, 'supermercado/public/proceder-pago.html', context)
                except:
                    tarjeta = None
                    productos_carrito = Producto_Carrito.objects.filter(carrito=carrito)
                    suma = 0
                    for producto in productos_carrito:
                        suma = suma + producto.importe_total
                    tasa = 10
                    totalCompra = suma + ((suma * tasa) / 100)
                    categorias = Categoria.objects.all()
                    context = {"carrito": productos_carrito, "sumatotal": suma, "tasa": tasa, "tarjeta": tarjeta,
                               "subtotal": suma - saldoDescontado,
                               "totalCompra": totalCompra,
                               "categorias": categorias}
                    request.session['cli_navbar_active'] = "carrito"
                    return render(request, 'supermercado/public/proceder-pago.html', context)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse("index"))
    except:
        form = LoginForm()
        categorias = Categoria.objects.all()
        context = {"form": form,"categorias": categorias}
        request.session['cli_navbar_active'] = "inicio"
        return render(request, "supermercado/public/customer-register.html", context)


def checkout(request):
    if request.method == "POST":
        token = request.POST["stripeToken"]
        if token:
            request.session['cli_navbar_active'] = "inicio"
            carrito = Carrito.objects.get(pk=int(request.session['cli_carrito']))
            carrito.fecha_confirmacion = datetime.now()
            carrito.save()
            cliente = Cliente.objects.get(pk=carrito.cliente.id)
            # Calculo el subtotal
            productos_carrito = Producto_Carrito.objects.filter(carrito=carrito)
            subtotal = 0
            # Si la factura es a titular de un cliente con tarjeta socio, tambien se comprueba los productos que tiene en el carrito
            # y en caso de que haya productos con "diferencia en tarjeta", se le añade a su saldo de la tarjeta.
            saldo_tarjeta = 0
            comprobar_cliente_tarjeta_socio = None
            if request.session['cli_descontar'] == 1:
                socio = 1
            else:
                socio = 0
            try:
                comprobar_cliente_tarjeta_socio = Tarjeta.objects.get(cliente_id=carrito.cliente.id)
                for producto in productos_carrito:
                    subtotal = subtotal + producto.importe_total
                    if producto.producto.diferencia_en_tarjeta:
                        saldo_aux = (producto.producto.pvp - producto.producto.pvp_socio) * producto.cantidad
                        saldo_tarjeta = saldo_tarjeta + saldo_aux
                saldo_descontar = int(request.session['saldo_descontar'])
                comprobar_cliente_tarjeta_socio.saldo_actual = comprobar_cliente_tarjeta_socio.saldo_actual - saldo_descontar
                comprobar_cliente_tarjeta_socio.saldo_actual = comprobar_cliente_tarjeta_socio.saldo_actual + saldo_tarjeta
                comprobar_cliente_tarjeta_socio.save()  # Guardamos el nuevo saldo del cliente
                # Relleno el resto de campos
                fecha = datetime.now()
                impuesto = 10
                importe_total = subtotal + ((subtotal * impuesto) / 100)
                # Inserto la factura
                factura = Factura(codigo=int(time.mktime(datetime.today().timetuple()) * 1000),
                                  cli_dni=cliente.dni,
                                  cli_nombre=cliente.nombre,
                                  cli_apellidos=cliente.apellidos,
                                  cli_cp=cliente.cp,
                                  cli_tipo_via=cliente.tipo_via,
                                  cli_direccion=cliente.direccion,
                                  cli_portal=cliente.portal,
                                  cli_escalera=cliente.escalera,
                                  cli_piso=cliente.piso,
                                  cli_casa=cliente.casa,
                                  cli_localidad=cliente.localidad,
                                  cli_provincia=cliente.provincia,
                                  cli_telefono1=cliente.telefono1,
                                  cli_telefono2=cliente.telefono2,
                                  cli_email=cliente.email,
                                  fecha=fecha,
                                  subtotal=subtotal,
                                  impuesto=impuesto,
                                  importe_total=float(request.session['total_compra']),
                                  cli_socio=1,
                                  cli_descuento=float(request.session['saldo_descontar'])
                                  )
                factura.save()  # Guardamos la factura
                # GENERAMOS LOS DETALLES DE LA FACTURA
                for producto in productos_carrito:
                    if producto.producto.pvp_socio > 0:
                        precio = producto.producto.pvp_socio
                    else:
                        precio = producto.producto.pvp
                    DetalleFactura(prod_codigo=producto.producto.codigo,
                                   prod_nombre=producto.producto.nombre,
                                   prod_descripcion_corta=producto.producto.descripcion_corta,
                                   prod_pvp=precio,
                                   prod_categoria=producto.producto.categoria.id,
                                   prod_cantidad=producto.cantidad,
                                   prod_total=producto.importe_total,
                                   prod_iva=10,
                                   factura_id=factura.id
                                   ).save()
            except:
                for producto in productos_carrito:
                    subtotal = subtotal + producto.importe_total
                # Relleno el resto de campos
                fecha = datetime.now()
                impuesto = 10
                importe_total = subtotal + ((subtotal * impuesto) / 100)
                # Inserto la factura
                factura = Factura(codigo=int(time.mktime(datetime.today().timetuple()) * 1000),
                                  cli_dni=cliente.dni,
                                  cli_nombre=cliente.nombre,
                                  cli_apellidos=cliente.apellidos,
                                  cli_cp=cliente.cp,
                                  cli_tipo_via=cliente.tipo_via,
                                  cli_direccion=cliente.direccion,
                                  cli_portal=cliente.portal,
                                  cli_escalera=cliente.escalera,
                                  cli_piso=cliente.piso,
                                  cli_casa=cliente.casa,
                                  cli_localidad=cliente.localidad,
                                  cli_provincia=cliente.provincia,
                                  cli_telefono1=cliente.telefono1,
                                  cli_telefono2=cliente.telefono2,
                                  cli_email=cliente.email,
                                  fecha=fecha,
                                  subtotal=subtotal,
                                  impuesto=impuesto,
                                  importe_total=importe_total,
                                  cli_socio= socio,
                                  cli_descuento=float(request.session['saldo_descontar'])
                                  )
                factura.save()  # Guardamos la factura
                # GENERAMOS LOS DETALLES DE LA FACTURA
                for producto in productos_carrito:
                    DetalleFactura(prod_codigo=producto.producto.codigo,
                                   prod_nombre=producto.producto.nombre,
                                   prod_descripcion_corta=producto.producto.descripcion_corta,
                                   prod_pvp=producto.producto.pvp,
                                   prod_categoria=producto.producto.categoria.id,
                                   prod_cantidad=producto.cantidad,
                                   prod_total=producto.importe_total,
                                   prod_iva=10,
                                   factura_id=factura.id
                                   ).save()
            carrito = Carrito(fecha_inicio=datetime.now(), cliente_id=cliente.id)
            carrito.save()
            request.session['cli_carrito'] = carrito.id
            request.session['cli_carrito_cantidad'] = 0
            categorias = Categoria.objects.all()
            context = {"categorias": categorias,"id_factura":factura.id}
            return render(request,'supermercado/public/thank-you.html',context)
        else:
            messages.info(request,"Ha habido un error.")
            return HttpResponseRedirect(reverse('cli_procederCompra'))
    else:
        messages.info(request, "Ha habido un error.")
        return HttpResponseRedirect(reverse('cli_procederCompra'))


def view_contacto(request):
    categorias = Categoria.objects.all()
    context = {"categorias": categorias}
    request.session['cli_navbar_active'] = "contacto"
    return render(request,'supermercado/public/contacto.html',context)


def sendMail(request):
    destinomensaje = "miguel.angel.langarita@gmail.com"
    asuntomensaje = "ASUNTO: " + request.POST['asunto'] + " | Mensaje enviado por: " + request.POST['nombre'] + " " + request.POST['apellidos']
    cuerpomensaje = "Mensaje de " + request.POST['email'] + "<br><br><hr><br>" + request.POST['mensaje']
    email = EmailMessage(asuntomensaje, cuerpomensaje, to=[destinomensaje])
    email.content_subtype = "html"  # Main content is now text/html
    email.send()
    messages.info(request,"Tu mensaje ha sido enviado con éxito. En breve recibiras una respuesta. Gracias por contactar con nosotros")
    return HttpResponseRedirect(reverse('cli_contacto'))