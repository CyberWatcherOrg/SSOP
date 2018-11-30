import json,time
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login, logout
#from elaphe import barcode
from datetime import datetime
from io import BytesIO
from reportlab.platypus import (SimpleDocTemplate, Image, Spacer, Paragraph, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle,TA_LEFT,TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from Supermercado import settings
from django.core.mail import EmailMessage

def view_index(request):
    request.session['isA'] = -1
    return render(request, "supermercado/public/index.html")

def login_action(request):
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        if user.is_superuser:
            perfil = Perfil_Usuario.objects.get(user=user)
            request.session['isA'] = 1
            request.session['id_usr'] = user.id
            request.session['id_empl'] = perfil.id
            request.session['imageprofile'] = str(perfil.image)
            login(request, user)
            return HttpResponseRedirect(reverse("index_admin"))
        else:
            login(request, user)
            cliente = Cliente.objects.get(user=user)
            request.session['isA'] = 0
            request.session['id_usr'] = user.id
            request.session['id_cli'] = cliente.id
            request.session['cli_nombre'] = cliente.nombre
            request.session['cli_apellidos'] = cliente.apellidos
            request.session['cli_imageprofile'] = str(cliente.image)
            request.session['cli_descontar'] = -1
            #Comprobamos si tiene algun carrito
            try:
                cliente = Cliente.objects.get(pk=request.session['id_cli'])
                carritos = Carrito.objects.filter(cliente=cliente)
                existeCarritoSinConfirmar = False
                for carrito in carritos:
                    if carrito.fecha_confirmacion is None:
                        existeCarritoSinConfirmar = True
                        request.session['cli_carrito'] = carrito.id
                        break
                if existeCarritoSinConfirmar: #si existe, le mostramos el carrito
                    productosCarrito = Producto_Carrito.objects.filter(carrito_id=request.session['cli_carrito'])
                    request.session['cli_carrito_cantidad'] = 0
                    for producto in productosCarrito:
                        request.session['cli_carrito_cantidad'] = int(request.session['cli_carrito_cantidad']) + 1
                    return HttpResponseRedirect(reverse("cli_carrito"))
                else: #sino, se le crea uno y se va al index
                    carrito = Carrito(fecha_inicio=datetime.now(), cliente_id=cliente.id)
                    carrito.save()
                    request.session['cli_carrito'] = carrito.id
                    request.session['cli_carrito_cantidad'] = 0
                    categorias = Categoria.objects.all()
                    context = {"categorias": categorias}
                    return render(request, 'supermercado/public/index.html', context)
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse("index"))
    else:
        form = LoginForm()
        categorias = Categoria.objects.all()
        context = {"form": form,"categorias": categorias}
        messages.error(request,'El usuario o la contraseña es invalido')
        return render(request, 'supermercado/public/customer-register.html', context)


def logout_empl(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def view_administracion(request):
    if request.user.is_authenticated and request.session['isA']:
        productos = Producto.objects.all()
        clientes = Cliente.objects.all()
        carritos = Carrito.objects.all()
        carritosNuevos=0
        carritosConfirmados=0
        for carrito in carritos:
            if carrito.fecha_confirmacion is None:
                carritosNuevos = carritosNuevos + 1
            else:
                carritosConfirmados = carritosConfirmados + 1
        opiniones = Mensaje_Cliente.objects.filter(tipo_mensaje="Opinión")
        opinionesAceptadas = MensajeProducto.objects.filter(estado_mensaje="Aceptado",mensaje__tipo_mensaje="Opinión")
        opinionesRechazadas = MensajeProducto.objects.filter(estado_mensaje="Rechazado", mensaje__tipo_mensaje="Opinión")
        opinionesEnEspera = MensajeProducto.objects.filter(estado_mensaje="En espera",mensaje__tipo_mensaje="Opinión")
        mensajesTodos = Mensaje_Cliente.objects.raw("select * from supermercadoApp_mensaje_cliente where tipo_mensaje <> 'Opinión'")
        mensajesEnInbox = sum(1 for result in mensajesTodos)
        if mensajesEnInbox == 0:
            mensajesEnInbox = 0
        context = {"productos":productos,
                   "carritosNuevos": carritosNuevos,
                   "carritosConfirmados":carritosConfirmados,
                   "clientes":clientes,
                   "opiniones":opiniones,
                   "opinionesAceptadas":opinionesAceptadas,
                   "opinionesRechazadas":opinionesRechazadas,
                   "opinionesEnEspera":opinionesEnEspera,
                   "mensajesEnInbox":mensajesEnInbox
                   }
        return render(request, "supermercado/administracion/index.html",context)
    else:
        return HttpResponseRedirect(reverse("index"))


########    PRODUCTOS     #########

def view_productos(request):
    if request.user.is_authenticated and request.session['isA']:
        productos = Producto.objects.all()
        context = {"tabla": productos}
        return render(request, "supermercado/administracion/productos.html", context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_producto_alta(request):
    if request.user.is_authenticated and request.session['isA']:
        form = ProductoForm()
        context = {"form": form}
        return render(request, 'supermercado/administracion/productos_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def add_producto(request):
    if request.user.is_authenticated and request.session['isA']:
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            bc = barcode('ean13', form.cleaned_data['codigo'], options=dict(includetext=True), scale=2, margin=1)
            bc.save(settings.MEDIA_ROOT + 'productos/ean13/' + form.cleaned_data['codigo'] + '.png')
            productoForm = form.save()
            producto = Producto.objects.get(pk=productoForm.id)
            producto.ean13 = 'ean13/' + form.cleaned_data['codigo'] + '.png'
            producto.save()
            return redirect('productos')
        else:
            context = {"form": form}
            return render(request, 'supermercado/administracion/productos_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_producto_edit(request, id_producto):
    if request.user.is_authenticated and request.session['isA']:
        producto = Producto.objects.get(pk=id_producto)
        form = ProductoForm(instance=producto)
        context = {"form": form, "producto": producto}
        return render(request, 'supermercado/administracion/productos_editar.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def edit_producto(request, id_producto):
    if request.user.is_authenticated and request.session['isA']:
        if request.method == "POST":
            producto = Producto.objects.get(pk=id_producto)
            form = ProductoForm(request.POST, request.FILES, instance=producto)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("productos"))
            else:
                context = {"form": form, "producto": producto}
                return render(request, 'supermercado/administracion/productos_editar.html', context)
        return HttpResponseRedirect(reverse("productos"))
    else:
        return HttpResponseRedirect(reverse("index"))


def delete_producto(request, id_producto):
    if request.user.is_authenticated and request.session['isA']:
        producto = Producto.objects.get(pk=id_producto)
        producto.imagen.delete()
        producto.delete()
        return HttpResponse(json.dumps({}), content_type='application/json')
    else:
        return HttpResponseRedirect(reverse("index"))


########    CATEGORIAS     #########

def view_categorias(request):
    if request.user.is_authenticated and request.session['isA']:
        form = CategoriaForm()
        categorias = Categoria.objects.all()
        context = {"form": form, "tabla": categorias}
        return render(request, 'supermercado/administracion/categorias.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_categoria_alta(request):
    if request.user.is_authenticated and request.session['isA']:
        form = CategoriaForm()
        context = {"form": form}
        return render(request, 'supermercado/administracion/categorias_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def add_categoria(request):
    if request.user.is_authenticated and request.session['isA']:
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
        else:
            context = {"form": form}
            return render(request, 'supermercado/administracion/categorias_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_categoria_edit(request, id_categoria):
    if request.user.is_authenticated and request.session['isA']:
        categoria = Categoria.objects.get(pk=id_categoria)
        form = CategoriaForm(instance=categoria)
        context = {"form": form, "categoria": categoria}
        return render(request, 'supermercado/administracion/categorias_editar.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def edit_categoria(request, id_categoria):
    if request.user.is_authenticated and request.session['isA']:
        if request.method == "POST":
            categoria = Categoria.objects.get(pk=id_categoria)
            form = CategoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("categorias"))
            else:
                context = {"form": form, "categoria": categoria}
                return render(request, 'supermercado/administracion/categorias_editar.html', context)
        return HttpResponseRedirect(reverse("productos"))
    else:
        return HttpResponseRedirect(reverse("index"))


def delete_categoria(request, id_categoria):
    if request.user.is_authenticated and request.session['isA']:
        Categoria.objects.get(pk=id_categoria).delete()
        return HttpResponse(json.dumps({}), content_type='application/json')
    else:
        return HttpResponseRedirect(reverse("index"))


########    USUARIOS     #########

def view_usuarios(request):
    if request.user.is_authenticated and request.session['isA']:
        form = ProfileForm()
        perfilUsuario = Perfil_Usuario.objects.all()
        context = {"form": form, "tabla": perfilUsuario}
        return render(request, 'supermercado/administracion/usuarios.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_usuario_alta(request):
    if request.user.is_authenticated and request.session['isA']:
        formProfile = ProfileForm(prefix='profile')
        formUser = UserForm(prefix='register')
        context = {"formUser": formUser, "formProfile": formProfile}
        return render(request, 'supermercado/administracion/usuarios_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def add_usuario(request):
    if request.user.is_authenticated and request.session['isA']:
        register = UserForm(request.POST, prefix='register')
        usrprofile = ProfileForm(request.POST, request.FILES, prefix='profile')
        if register.is_valid() and usrprofile.is_valid():
            if User.objects.filter(email__iexact=register.cleaned_data['email']):
                register.add_error('email', 'El email ya existe')
                context = {"formUser": register, "formProfile": usrprofile, "error_user": register,
                           "error_profile": usrprofile}
                return render(request, 'supermercado/administracion/usuarios_alta.html', context)
            user = register.save()
            usrprof = usrprofile.save(commit=False)
            usrprof.user = user
            usrprof.save()
            user = User.objects.get(perfil_usuario__dni=usrprofile.cleaned_data['dni'])
            user.set_password(register.cleaned_data['password'])
            user.is_staff = True
            user.save()
            return HttpResponseRedirect(reverse("usuarios"))
        else:
            print(register.errors)
            print(usrprofile.errors)
            context = {"formUser": register, "formProfile": usrprofile, "error_user": register, "error_profile": usrprofile}
            return render(request, 'supermercado/administracion/usuarios_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_usuario_edit(request, id_usuario):
    if request.user.is_authenticated and request.session['isA']:
        user = User.objects.get(pk=id_usuario)
        profile = Perfil_Usuario.objects.get(user_id=user.id)
        dni = profile.dni
        username = user.username
        formProfile = ProfileEditForm(prefix='profile', instance=profile)
        formUser = UserEditForm(prefix='register', instance=user)
        context = {"formUser": formUser, "formProfile": formProfile, "id_usuario": id_usuario, "username": username,
                   'dni': dni}
        return render(request, 'supermercado/administracion/usuarios_editar.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def edit_usuario(request, id_usuario):
    if request.user.is_authenticated and request.session['isA']:
        if request.method == "POST":
            user_form = UserEditForm(request.POST, prefix='register')
            profile_form = ProfileEditForm(request.POST, request.FILES, prefix='profile')
            user = User.objects.get(pk=id_usuario)
            user.first_name = user_form.__getitem__('first_name').value()
            user.last_name = user_form.__getitem__('last_name').value()
            email = user_form.__getitem__('email').value()
            try:
                usuario = User.objects.get(email=email)
                if (user.email == email):
                    user.email = email
                else:
                    messages.error(request, 'El email ya existe')
                    context = {"formUser": user_form, "formProfile": profile_form, "id_usuario": id_usuario}
                    return render(request, 'supermercado/administracion/usuarios_editar.html', context)
            except ObjectDoesNotExist:
                user.email = email
            user.is_superuser = user_form.__getitem__('is_superuser').value()
            if user_form.__getitem__('is_superuser').value():
                user.is_staff = True
            else:
                user.is_staff = False
            if user_form.__getitem__('password').value() is not "":
                user.set_password(user_form.__getitem__('password').value())
            user.save()
            profile = Perfil_Usuario.objects.get(user_id=user.id)
            profile.cp = profile_form.__getitem__('cp').value()
            profile.tipo_via = profile_form.__getitem__('tipo_via').value()
            profile.direccion = profile_form.__getitem__('direccion').value()
            profile.portal = profile_form.__getitem__('portal').value()
            profile.escalera = profile_form.__getitem__('escalera').value()
            profile.piso = profile_form.__getitem__('piso').value()
            profile.casa = profile_form.__getitem__('casa').value()
            profile.localidad = profile_form.__getitem__('localidad').value()
            profile.provincia = profile_form.__getitem__('provincia').value()
            profile.telefono1 = profile_form.__getitem__('telefono1').value()
            profile.telefono2 = profile_form.__getitem__('telefono2').value()
            if profile_form.__getitem__('image').value() == False:
                profile.image.delete()
                profile.image = ""
            elif profile_form.__getitem__('image').value() is not "":
                profile.image.delete()
                profile.image = profile_form.__getitem__('image').value()
            profile.save()
            if request.session['id_empl'] == profile.id:
                request.session['imageprofile'] = str(profile.image)
            return HttpResponseRedirect(reverse("usuarios"))
        else:
            return HttpResponseRedirect(reverse("usuarios"))
    else:
        return HttpResponseRedirect(reverse("index"))


def delete_usuario(request, id_usuario):
    if request.user.is_authenticated and request.session['isA']:
        perfil = Perfil_Usuario.objects.get(user_id=id_usuario)
        User.objects.get(pk=id_usuario).delete()
        perfil.image.delete()
        perfil.delete()
        return HttpResponse(json.dumps({}), content_type='application/json')
    else:
        return HttpResponseRedirect(reverse("index"))


########    CLIENTES     #########

def view_clientes(request):
    if request.user.is_authenticated and request.session['isA']:
        form = ClienteAddForm()
        clientes = Cliente.objects.all()
        context = {"form": form, "tabla": clientes}
        return render(request, 'supermercado/administracion/clientes.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_cliente_alta(request):
    if request.user.is_authenticated and request.session['isA']:
        formcliente = ClienteAddForm(prefix='cliente')
        formUser = UserForm(prefix='register')
        context = {"form": formcliente,"formUser": formUser}
        return render(request, 'supermercado/administracion/cliente_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def add_cliente(request):
    if request.user.is_authenticated and request.session['isA']:
        clienteForm = ClienteAddForm(request.POST,request.FILES, prefix='cliente')
        register = UserForm(request.POST, prefix='register')
        if register.is_valid() and clienteForm.is_valid():
            if Cliente.objects.filter(dni__iexact=clienteForm.cleaned_data['email']):
                register.add_error('email', 'El email ya existe')
                context = {"form": clienteForm, "formUser": register}
                return render(request, 'supermercado/administracion/cliente_alta.html', context)
            user = register.save()
            cliente = clienteForm.save(commit=False)
            cliente.user = user
            cliente.save()
            user = User.objects.get(cliente__dni=clienteForm.cleaned_data['dni'])
            user.set_password(register.cleaned_data['password'])
            user.is_staff = False
            user.save()
            return HttpResponseRedirect(reverse("clientes"))
        else:

            context = {"form": clienteForm, "formUser": register}
            return render(request, 'supermercado/administracion/cliente_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_cliente_edit(request, id_usuario):
    if request.user.is_authenticated and request.session['isA']:
        user = User.objects.get(pk=id_usuario)
        cliente = Cliente.objects.get(user_id=user.id)
        form = ClienteEditForm(prefix='cliente', instance=cliente)
        formUser = UserEditForm(prefix='register', instance=user)
        context = {"form": form, "formUser": formUser, "id_usuario": id_usuario, "id_cliente":cliente.id, "cliente": cliente, "username":user.username}
        return render(request, 'supermercado/administracion/cliente_editar.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def edit_cliente(request, id_usuario):
    if request.user.is_authenticated and request.session['isA']:
        if request.method == "POST":
            clienteForm = ClienteEditForm(request.POST,request.FILES, prefix='cliente')
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
            if clienteForm.__getitem__('telefono1').value().__len__()<9:
                messages.error(request, 'El número de teléfono 1 no tiene 9 dígitos')
                context = {"form": clienteForm, "formUser": formUser, "id_usuario": id_usuario, "id_cliente": cliente.id,
                           "cliente": cliente}
                return render(request, 'supermercado/administracion/cliente_editar.html', context)
            if clienteForm.__getitem__('telefono2').value().__len__()<9:
                messages.error(request, 'El número de teléfono 2 no tiene 9 dígitos')
                context = {"form": clienteForm, "formUser": formUser, "id_usuario": id_usuario, "id_cliente": cliente.id,
                           "cliente": cliente}
                return render(request, 'supermercado/administracion/cliente_editar.html', context)
            cliente.telefono1 = clienteForm.__getitem__('telefono1').value()
            cliente.telefono2 = clienteForm.__getitem__('telefono2').value()
            email = clienteForm.__getitem__('email').value()
            try:
                usuario = Cliente.objects.get(email=email)
                if (cliente.email == email):
                    cliente.email = email
                else:
                    messages.error(request, 'El email ya existe')
                    context = {"form": clienteForm, "formUser": formUser, "id_usuario": id_usuario, "id_cliente": cliente.id,
                               "cliente": cliente}
                    return render(request, 'supermercado/administracion/cliente_editar.html', context)
            except ObjectDoesNotExist:
                cliente.email = email
            cliente.email = clienteForm.__getitem__('email').value()
            if clienteForm.__getitem__('image').value() == False:
                cliente.image.delete()
                cliente.image = ""
            elif clienteForm.__getitem__('image').value() is not "":
                cliente.image.delete()
                cliente.image = clienteForm.__getitem__('image').value()
            cliente.save()
            return HttpResponseRedirect(reverse("clientes"))
    else:
        return HttpResponseRedirect(reverse("index"))


def delete_cliente(request, id_cliente):
    if request.user.is_authenticated and request.session['isA']:
        cliente = Cliente.objects.get(pk=id_cliente)
        user = User.objects.get(cliente__dni=cliente.dni)
        cliente.delete()
        user.delete()
        return HttpResponse(json.dumps({}), content_type='application/json')
    else:
        return HttpResponseRedirect(reverse("index"))


########    TARJETAS SOCIO     #########

def view_tarjetas(request):
    if request.user.is_authenticated and request.session['isA']:
        form = TarjetaForm()
        tarjetas = Tarjeta.objects.all()
        context = {"form": form, "tabla": tarjetas}
        return render(request, 'supermercado/administracion/tarjetas.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_tarjeta_alta(request):
    if request.user.is_authenticated and request.session['isA']:
        form = TarjetaForm()
        context = {"form": form}
        return render(request, 'supermercado/administracion/tarjeta_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def add_tarjeta(request):
    if request.user.is_authenticated and request.session['isA']:
        tarjetaForm = TarjetaForm(request.POST)
        if tarjetaForm.is_valid():
            try:
                comprobarTarjeta = Tarjeta.objects.get(cliente=tarjetaForm.__getitem__('cliente').value())
                if comprobarTarjeta:
                    form = TarjetaForm(request.POST)
                    form.add_error('cliente', {'El cliente seleccionado ya tiene una tarjeta'})
                    context = {"form": form}
                    return render(request, 'supermercado/administracion/tarjeta_alta.html', context)
                else:
                    tarjetaForm.save()
                    return HttpResponseRedirect(reverse("tarjetas"))
            except ObjectDoesNotExist:
                tarjetaForm.save()
                return HttpResponseRedirect(reverse("tarjetas"))
        else:
            print(tarjetaForm.errors)
            context = {"form": tarjetaForm}
            return render(request, 'supermercado/administracion/tarjeta_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def addTarjetaToCliente(request, id_cliente):
    if request.user.is_authenticated and request.session['isA']:
        tarjeta = Tarjeta(fecha_adquisicion=datetime.now(), saldo_actual=0)
        cliente = Cliente.objects.get(pk=id_cliente)
        user = User.objects.get(cliente__dni=cliente.dni)
        id_usuario = user.id
        try:
            comprobarTarjeta = Tarjeta.objects.get(cliente_id=cliente.id)
            if comprobarTarjeta:
                messages.error(request,
                               "El cliente " + cliente.nombre + " " + cliente.apellidos + " ya dispone de una tarjeta socio.")
                return HttpResponseRedirect(reverse('clientes_editar', args=(id_usuario,)))
            else:
                tarjeta.cliente = cliente
                tarjeta.save()
                messages.success(request, "Se le ha asignado una tarjeta al cliente " + cliente)
                return HttpResponseRedirect(reverse('clientes_editar', args=(id_usuario,)))
        except ObjectDoesNotExist:
            tarjeta.cliente = cliente
            tarjeta.save()
            messages.success(request,
                             "Se le ha asignado una tarjeta al cliente " + cliente.nombre + " " + cliente.apellidos)
            return HttpResponseRedirect(reverse('clientes_editar', args=(id_usuario,)))
    else:
        return HttpResponseRedirect(reverse("index"))


def view_tarjeta_edit(request, id_tarjeta):
    if request.user.is_authenticated and request.session['isA']:
        tarjeta = Tarjeta.objects.get(pk=id_tarjeta)
        form = TarjetaForm(instance=tarjeta)
        context = {"form": form, "id_tarjeta": id_tarjeta}
        return render(request, 'supermercado/administracion/tarjeta_editar.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def edit_tarjeta(request, id_tarjeta):
    if request.user.is_authenticated and request.session['isA']:
        if request.method == "POST":
            tarjeta = Tarjeta.objects.get(pk=id_tarjeta)
            tarjetaForm = TarjetaForm(request.POST)
            if tarjetaForm.is_valid():
                tarjeta.fecha_adquisicion = tarjetaForm.cleaned_data['fecha_adquisicion']
                tarjeta.saldo_actual = tarjetaForm.__getitem__('saldo_actual').value()
                try:
                    comprobarTarjeta = Tarjeta.objects.get(cliente_id=int(tarjetaForm.__getitem__('cliente').value()))
                    if comprobarTarjeta.cliente.id == tarjeta.cliente.id:
                        cliente = Cliente.objects.get(pk=tarjetaForm.__getitem__('cliente').value())
                        tarjeta.cliente = cliente
                        tarjeta.save()
                        return HttpResponseRedirect(reverse("tarjetas"))
                    else:
                        form = TarjetaForm(request.POST)
                        form.add_error('cliente', 'El cliente seleccionado ya tiene una tarjeta')
                        context = {"form": form, "id_tarjeta": id_tarjeta}
                        return render(request, 'supermercado/administracion/tarjeta_editar.html', context)
                except ObjectDoesNotExist:
                    cliente = Cliente.objects.get(pk=tarjetaForm.__getitem__('cliente').value())
                    tarjeta.cliente = cliente
                    tarjeta.save()
                    return HttpResponseRedirect(reverse("tarjetas"))
            else:
                form = TarjetaForm(request.POST)
                context = {"form": form, "id_tarjeta": id_tarjeta}
                return render(request, 'supermercado/administracion/tarjeta_editar.html', context)
        else:
            form = TarjetaForm(request.POST)
            context = {"form": form, "id_tarjeta": id_tarjeta}
            return render(request, 'supermercado/administracion/tarjeta_editar.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def delete_tarjeta(request, id_tarjeta):
    if request.user.is_authenticated and request.session['isA']:
        Tarjeta.objects.get(pk=id_tarjeta).delete()
        return HttpResponse(json.dumps({}), content_type='application/json')
    else:
        return HttpResponseRedirect(reverse("index"))


########    CARRITOS DE COMPRA     #########

def view_carritos(request):
    if request.user.is_authenticated and request.session['isA']:
        form = CarritoForm()
        carritos = Carrito.objects.all()
        context = {"form": form, "tabla": carritos}
        return render(request, 'supermercado/administracion/carritos.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_carrito_alta(request):
    if request.user.is_authenticated and request.session['isA']:
        form = CarritoForm()
        context = {"form": form}
        return render(request, 'supermercado/administracion/carrito_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_carrito_productos(request, id_carrito):
    if request.user.is_authenticated and request.session['isA']:
        form = CarritoProductoForm()
        carritoProductos = Producto_Carrito.objects.filter(carrito_id=id_carrito)
        carrito = Carrito.objects.get(pk=id_carrito)
        context = {"form": form, "tabla": carritoProductos, "carrito": carrito}
        return render(request, 'supermercado/administracion/carrito_productos.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_producto_carrito(request, id_producto_carrito):
    if request.user.is_authenticated and request.session['isA']:
        productosCarrito = Producto_Carrito.objects.get(pk=id_producto_carrito)
        form = CarritoProductoForm(instance=productosCarrito)
        context = {"form": form, "id_producto_carrito": id_producto_carrito, "carrito": productosCarrito.carrito,"producto":productosCarrito}
        return render(request, 'supermercado/administracion/carrito_producto_editar.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_carrito_edit(request, id_carrito):
    if request.user.is_authenticated and request.session['isA']:
        carrito = Carrito.objects.get(pk=id_carrito)
        form = CarritoForm(instance=carrito)
        context = {"form": form, "carrito": carrito}
        return render(request, 'supermercado/administracion/carrito_editar.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_carrito_producto_add(request, id_carrito):
    if request.user.is_authenticated and request.session['isA']:
        carrito = Carrito.objects.get(pk=id_carrito)
        form = CarritoProductoForm(prefix="carrito")
        formCarrito = CarritoProductoAddForm(prefix="cliente", initial={"carrito": carrito.id})
        context = {"form": form, "formCarrito": formCarrito, "carrito": carrito}
        return render(request, 'supermercado/administracion/carrito_producto_anadir.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def add_carrito(request):
    if request.user.is_authenticated and request.session['isA']:
        form = CarritoForm(request.POST)
        if form.is_valid():
            try:
                carritos = Carrito.objects.filter(cliente=form.cleaned_data['cliente'])
                existeCarritoSinConfirmar = False
                for carrito in carritos:
                    if carrito.fecha_confirmacion is None:
                        existeCarritoSinConfirmar = True
                if existeCarritoSinConfirmar:
                    form.add_error('cliente', 'El cliente seleccionado ya tiene un carrito sin confirmar')
                    context = {"form": form}
                    return render(request, 'supermercado/administracion/carrito_alta.html', context)
                else:
                    form.save()
                    return HttpResponseRedirect(reverse("carritos"))
            except ObjectDoesNotExist:
                form.save()
                return HttpResponseRedirect(reverse("carritos"))
        else:
            context = {"form": form}
            return render(request, 'supermercado/administracion/carrito_alta.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def add_producto_carrito(request):
    if request.user.is_authenticated and request.session['isA']:
        form = CarritoProductoAdd2Form(request.POST, prefix="carrito")
        formCarrito = CarritoProductoAddForm(request.POST, prefix="cliente")
        if form.is_valid():
            if form.cleaned_data['cantidad'] == 0:
                carrito = Carrito.objects.get(pk=formCarrito.__getitem__('carrito').value())
                form.add_error('producto', 'La cantidad indicada no es posible. Debe introducir minimo valor: 1')
                context = {"form": form, "formCarrito": formCarrito, "carrito": carrito}
                return render(request, 'supermercado/administracion/carrito_producto_anadir.html', context)
            comprobarProducto = Producto.objects.get(pk=form.__getitem__('producto').value())
            if comprobarProducto.stock > 0:
                producto_carrito = Producto_Carrito(producto=form.cleaned_data['producto'],
                                                    carrito_id=formCarrito.__getitem__('carrito').value(),
                                                    cantidad=form.cleaned_data['cantidad'])
                producto_carrito.save()
                producto = Producto.objects.get(pk = form.__getitem__('producto').value())
                producto.stock = producto.stock-int(form.cleaned_data['cantidad'])
                producto.save()
                carrito = formCarrito.__getitem__('carrito').value()
                return HttpResponseRedirect(reverse("carrito_producto", args=(carrito,)))
            else:
                carrito = Carrito.objects.get(pk=formCarrito.__getitem__('carrito').value())
                form.add_error('producto', 'No existe stock del producto seleccionado')
                context = {"form": form, "formCarrito": formCarrito, "carrito": carrito}
                return render(request, 'supermercado/administracion/carrito_producto_anadir.html', context)
        else:
            carrito = Carrito.objects.get(pk=formCarrito.__getitem__('carrito').value())
            context = {"form": form, "formCarrito": formCarrito, "carrito": carrito}
            return render(request, 'supermercado/administracion/carrito_producto_anadir.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def producto_carrito_edit(request, id_producto_carrito):
    if request.user.is_authenticated and request.session['isA']:
        instance = Producto_Carrito.objects.get(pk=id_producto_carrito)
        form = CarritoProductoForm(request.POST, instance=instance)
        if form.is_valid():
            producto_carrito = Producto_Carrito.objects.get(pk=id_producto_carrito)
            producto_carrito.producto = form.cleaned_data['producto']
            producto_origen = Producto.objects.get(pk=form.__getitem__('producto').value())
            if producto_origen.stock < int(form.__getitem__('cantidad').value()):
                carrito = Carrito.objects.get(pk=form.__getitem__('carrito').value())
                form.add_error('producto', 'No existe la cantidad indicada del producto seleccionado. La cantidad actual del producto seleccionado es: '+ str(producto_origen.stock))
                context = {"form": form, "formCarrito": form, "carrito": carrito}
                return render(request, 'supermercado/administracion/carrito_producto_editar.html', context)
            if int(form.__getitem__('cantidad').value()) == 0:
                carrito = Carrito.objects.get(pk=form.__getitem__('carrito').value())
                form.add_error('producto','La cantidad indicada no es posible. Debe introducir minimo valor: 1')
                context = {"form": form, "formCarrito": form,"id_producto_carrito": id_producto_carrito, "carrito": carrito}
                return render(request, 'supermercado/administracion/carrito_producto_editar.html', context)
            if producto_carrito.cantidad < form.cleaned_data['cantidad']:
                producto_origen.stock = producto_origen.stock - (form.cleaned_data['cantidad'] - producto_carrito.cantidad)
            elif producto_carrito.cantidad > form.cleaned_data['cantidad']:
                producto_origen.stock = producto_origen.stock + (producto_carrito.cantidad - form.cleaned_data['cantidad'])
            producto_origen.save()
            producto_carrito.cantidad = form.cleaned_data['cantidad']
            producto_carrito.updateProductoCarrito()
            carrito = form.__getitem__('carrito').value()
            return HttpResponseRedirect(reverse("carrito_producto", args=(carrito,)))
        else:
            carrito = form.__getitem__('carrito').value()
            context = {"form": form, "id_producto_carrito": id_producto_carrito,"carrito":carrito}
            return render(request, 'supermercado/administracion/carrito_producto_editar.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


def edit_carrito(request, id_carrito):
    if request.user.is_authenticated and request.session['isA']:
        if request.method == "POST":
            carrito = Carrito.objects.get(pk=id_carrito)
            form = CarritoForm(request.POST, instance=carrito)
            if form.is_valid():
                try:
                    existeCarrito = False
                    carritoEncontrado = None
                    comprobarCarrito = Carrito.objects.filter(cliente=form.cleaned_data['cliente'])
                    for carritos in comprobarCarrito:
                        if carrito.cliente == carritos.cliente and carritos.fecha_confirmacion is None:
                            existeCarrito = True
                            carritoEncontrado = carritos
                            break
                    if existeCarrito:
                        productosCarrito = Producto_Carrito.objects.filter(carrito=carritoEncontrado)
                        if form.cleaned_data['fecha_confirmacion'] is not None and form.cleaned_data['fecha_confirmacion'] <= form.cleaned_data['fecha_inicio']:
                            form.add_error('fecha_confirmacion', 'La fecha de confirmación no puede ser menor o igual que la de inicio de compra.')
                            context = {"form": form, "carrito": carrito}
                            return render(request, 'supermercado/administracion/carrito_editar.html', context)
                        elif carritoEncontrado.id == carrito.id and productosCarrito.__len__() > 0:
                            form.save()
                            return HttpResponseRedirect(reverse("carritos"))
                        elif carritoEncontrado.fecha_confirmacion is None and carritoEncontrado.id != carrito.id:
                            form.add_error('cliente', 'El cliente seleccionado ya tiene un carrito sin confirmar')
                            context = {"form": form, "carrito": carrito}
                            return render(request, 'supermercado/administracion/carrito_editar.html', context)

                        elif productosCarrito.__len__() == 0 and carritoEncontrado.id != carrito.id:
                            form.add_error('fecha_confirmacion',
                                           'No existen productos añadidos al carrito #' + id_carrito + '. Un carrito tiene que tener minimo de 1 producto para ser confirmado.')
                            context = {"form": form, "carrito": carrito}
                            return render(request, 'supermercado/administracion/carrito_editar.html', context)

                        elif productosCarrito.__len__() != 0 and carritoEncontrado.id == carrito.id:
                            form.add_error('fecha_confirmacion',
                                           'No existen productos añadidos al carrito #' + id_carrito + '. Un carrito tiene que tener minimo de 1 producto para ser confirmado.')
                            context = {"form": form, "carrito": carrito}
                            return render(request, 'supermercado/administracion/carrito_editar.html', context)

                        elif productosCarrito.__len__() != 0 and carritoEncontrado.id == carrito.id and form.cleaned_data['fecha_confirmacion'] is not None and form.cleaned_data['fecha_confirmacion'] > form.cleaned_data['fecha_inicio']:
                            form.add_error('fecha_confirmacion',
                                           'No existen productos añadidos al carrito #' + id_carrito + '. Un carrito tiene que tener minimo de 1 producto para ser confirmado.')
                            context = {"form": form, "carrito": carrito}
                            return render(request, 'supermercado/administracion/carrito_editar.html', context)

                        elif productosCarrito.__len__() <= 0 and carritoEncontrado.id == carrito.id and form.cleaned_data['fecha_confirmacion'] is not None:
                            form.add_error('fecha_confirmacion',
                                           'No existen productos añadidos al carrito #' + id_carrito + '. Un carrito tiene que tener minimo de 1 producto para ser confirmado.')
                            context = {"form": form, "carrito": carrito}
                            return render(request, 'supermercado/administracion/carrito_editar.html', context)

                        elif productosCarrito.__len__() > 0:
                            form.save()
                            updateProductsCarritoCliente(id_carrito)
                            return HttpResponseRedirect(reverse("carritos"))

                        else:
                            form.save()
                            updateProductsCarritoCliente(id_carrito)
                            return HttpResponseRedirect(reverse("carritos"))
                    else:
                        if form.cleaned_data['fecha_confirmacion'] is not None:
                            form.add_error('fecha_confirmacion',
                                           'No puede introducir una fecha de confirmación a un cliente que todavia no tiene un carrito asignado.')
                            context = {"form": form, "carrito": carrito}
                            return render(request, 'supermercado/administracion/carrito_editar.html', context)
                        else:
                            form.save()
                            updateProductsCarritoCliente(id_carrito)
                            return HttpResponseRedirect(reverse("carritos"))
                except:
                    form.save()
                    updateProductsCarritoCliente(id_carrito)
                    return HttpResponseRedirect(reverse("carritos"))
            else:
                context = {"form": form, "carrito": carrito}
                return render(request, 'supermercado/administracion/carrito_editar.html', context)
        return HttpResponseRedirect(reverse("carritos"))
    else:
        return HttpResponseRedirect(reverse("index"))


def updateProductsCarritoCliente(id_carrito):
    productos = Producto_Carrito.objects.filter(carrito_id=id_carrito)
    for producto in productos:
        producto.updateImporteTotalProduct()


def confirmarCarrito(request, id_carrito):
    if request.user.is_authenticated and request.session['isA']:
        try:
            productosCarrito = Producto_Carrito.objects.filter(carrito_id=id_carrito)
            if productosCarrito.__len__() != 0:
                carrito = Carrito.objects.get(pk=id_carrito)
                carrito.fecha_confirmacion = datetime.now()
                carrito.save()
                return HttpResponseRedirect(reverse('generar_factura', args=(id_carrito,)))
            else:
                messages.error(request,
                               'No existen productos añadidos al carrito #' + id_carrito + '. Un carrito tiene que tener minimo de 1 producto para ser confirmado.')
                return HttpResponseRedirect(reverse("carritos"))
        except:
            messages.error(request,
                           'No existen productos añadidos al carrito #' + id_carrito + '. Un carrito tiene que tener minimo de 1 producto para ser confirmado.')
            return HttpResponseRedirect(reverse("carritos"))
    else:
        return HttpResponseRedirect(reverse("index"))


def delete_carrito(request):
    if request.user.is_authenticated and request.session['isA']:
        id_carrito = request.GET.get('id_carrito', None)
        Carrito.objects.get(pk=id_carrito).delete()
        data = {"estado":"noerror","mensaje":"El carrito ha sido borrado"}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(reverse("index"))


def delete_producto_carrito(request, id_producto_carrito):
    if request.user.is_authenticated and request.session['isA']:
        producto_carrito = Producto_Carrito.objects.get(pk=id_producto_carrito)
        producto = Producto.objects.get(pk=producto_carrito.producto.id)
        producto.stock = producto.stock + producto_carrito.cantidad
        producto.save()
        producto_carrito.delete()
        return HttpResponse(json.dumps({}), content_type='application/json')
    else:
        return HttpResponseRedirect(reverse("index"))


########    FACTURAS     #########

def generar_factura(request, id_carrito):
    if request.user.is_authenticated and request.session['isA']:
        carrito = Carrito.objects.get(pk=id_carrito)
        cliente = Cliente.objects.get(pk = carrito.cliente.id)
        # Calculo el subtotal
        productos_carrito = Producto_Carrito.objects.filter(carrito=carrito)
        subtotal = 0
        # Si la factura es a titular de un cliente con tarjeta socio, tambien se comprueba los productos que tiene en el carrito
        # y en caso de que haya productos con "diferencia en tarjeta", se le añade a su saldo de la tarjeta.
        saldo_tarjeta=0
        comprobar_cliente_tarjeta_socio = None
        try:
            comprobar_cliente_tarjeta_socio = Tarjeta.objects.get(cliente_id=carrito.cliente.id)
            for producto in productos_carrito:
                subtotal = subtotal + producto.importe_total
                if producto.producto.diferencia_en_tarjeta:
                    saldo_aux = (producto.producto.pvp - producto.producto.pvp_socio) * producto.cantidad
                    saldo_tarjeta = saldo_tarjeta + saldo_aux
            comprobar_cliente_tarjeta_socio.saldo_actual = comprobar_cliente_tarjeta_socio.saldo_actual + saldo_tarjeta
            comprobar_cliente_tarjeta_socio.save() # Guardamos el nuevo saldo del cliente
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
                              cli_socio=1,
                              cli_descuento=0
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
        factura = Factura(codigo=int(time.mktime(datetime.today().timetuple())*1000),
                          cli_dni=cliente.dni,
                          cli_nombre=cliente.nombre,
                          cli_apellidos=cliente.apellidos,
                          cli_cp = cliente.cp,
                          cli_tipo_via=cliente.tipo_via,
                          cli_direccion=cliente.direccion,
                          cli_portal=cliente.portal,
                          cli_escalera=cliente.escalera,
                          cli_piso = cliente.piso,
                          cli_casa = cliente.casa,
                          cli_localidad=cliente.localidad,
                          cli_provincia=cliente.provincia,
                          cli_telefono1=cliente.telefono1,
                          cli_telefono2=cliente.telefono2,
                          cli_email= cliente.email,
                          fecha=fecha,
                          subtotal=subtotal,
                          impuesto=impuesto,
                          importe_total=importe_total
                          )
        factura.save() # Guardamos la factura
        #GENERAMOS LOS DETALLES DE LA FACTURA
        for producto in productos_carrito:
            DetalleFactura(prod_codigo= producto.producto.codigo,
                           prod_nombre=producto.producto.nombre,
                           prod_descripcion_corta=producto.producto.descripcion_corta,
                           prod_pvp=producto.producto.pvp,
                           prod_categoria=producto.producto.categoria.id,
                           prod_cantidad=producto.cantidad,
                           prod_total=producto.importe_total,
                           prod_iva=10,
                           factura_id=factura.id
                           ).save()
        messages.success(request, "Se ha generado la factura correctamente. Número de factura: #" + str(factura.codigo))
        return HttpResponseRedirect(reverse('carritos'))
    else:
        return HttpResponseRedirect(reverse("index"))

def view_facturas(request):
    if request.user.is_authenticated and request.session['isA']:
        form = FacturaForm()
        facturas = Factura.objects.all()
        context = {"form": form, "tabla": facturas}
        return render(request, 'supermercado/administracion/facturas.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))

def view_facturas_detalle(request,id_factura):
    if request.user.is_authenticated and request.session['isA']:
        factura = Factura.objects.get(pk = id_factura)
        detallefactura = DetalleFactura.objects.filter(factura=factura)
        context = {"tabla": detallefactura,"factura":factura}
        return render(request, 'supermercado/administracion/detalle_factura.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))

########    OPINIONES     #########

def view_opiniones(request):
    if request.user.is_authenticated and request.session['isA']:
        opiniones = Mensaje_Cliente.objects.filter(tipo_mensaje='Opinión')
        mensajesproductos = MensajeProducto.objects.all()
        context = {"opiniones":opiniones,"mensajesProductos":mensajesproductos}
        return render(request,'supermercado/administracion/opiniones.html',context)
    else:
        return HttpResponseRedirect(reverse("index"))


def aceptar_opinion(request, id_mensaje):
    if request.user.is_authenticated and request.session['isA']:
        mensaje = MensajeProducto.objects.get(pk = id_mensaje)
        mensaje.estado_mensaje = "Aceptado"
        mensaje.save()
        return HttpResponseRedirect(reverse('opiniones'))
    else:
        return HttpResponseRedirect(reverse("index"))


def rechazar_opinion(request, id_mensaje):
    if request.user.is_authenticated and request.session['isA']:
        mensaje = MensajeProducto.objects.get(pk = id_mensaje)
        mensaje.estado_mensaje = "Rechazado"
        mensaje.save()
        return HttpResponseRedirect(reverse('opiniones'))
    else:
        return HttpResponseRedirect(reverse("index"))


def opinion_enEspera(request, id_mensaje):
    if request.user.is_authenticated and request.session['isA']:
        mensaje = MensajeProducto.objects.get(pk = id_mensaje)
        mensaje.estado_mensaje = "En espera"
        mensaje.save()
        return HttpResponseRedirect(reverse('opiniones'))
    else:
        return HttpResponseRedirect(reverse("index"))



def delete_opinion(request, id_mensaje, id_mensajeproducto):
    if request.user.is_authenticated and request.session['isA']:
        MensajeProducto.objects.get(pk = id_mensajeproducto).delete()
        Mensaje_Cliente.objects.get(pk=id_mensaje).delete()
        return HttpResponseRedirect(reverse('opiniones'))
    else:
        return HttpResponseRedirect(reverse("index"))

def opinion_ver(request,id_mensaje):
    if request.user.is_authenticated and request.session['isA']:
        mensaje = Mensaje_Cliente.objects.get(pk=id_mensaje)
        data = {"mensaje": mensaje.mensaje,"cliente":"Opinión del cliente " + mensaje.cliente.nombre + " " + mensaje.cliente.apellidos}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(reverse("index"))



########    OPINIONES     #########

def view_mailbox(request):
    if request.user.is_authenticated and request.session['isA']:
        todos_los_mensajes = Mensaje_Cliente.objects.raw("select * from supermercadoApp_mensaje_cliente where tipo_mensaje <> 'Opinión'")
        mensajes = sum(1 for result in todos_los_mensajes)
        if mensajes == 0:
            mensajes = 0
        todos_los_mensajes = sum(1 for result in todos_los_mensajes)
        if todos_los_mensajes == 0:
            todos_los_mensajes = 0
        mensajesproductos = MensajeProducto.objects.all()
        mensajesproductos_Dudas = Mensaje_Cliente.objects.filter(tipo_mensaje="Duda")
        mensajesproductos_Sugerencia= Mensaje_Cliente.objects.filter(tipo_mensaje="Sugerencia")
        mensajesproductos_Reclamacion = Mensaje_Cliente.objects.filter(tipo_mensaje="Reclamación")
        request.session['tipo_mensaje'] = "Todos"
        context = {"mensajes":todos_los_mensajes,"mensajesProductos":mensajesproductos,"mensajesProductos_Dudas":mensajesproductos_Dudas,"mensajesProductos_Sugerencias":mensajesproductos_Sugerencia,"mensajesProductos_Reclamacion":mensajesproductos_Reclamacion}
        return render(request,'supermercado/administracion/mailbox/mailbox.html',context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_mailbox_dudas(request):
    if request.user.is_authenticated and request.session['isA']:
        mensajesTodos = Mensaje_Cliente.objects.raw(
            "select * from supermercadoApp_mensaje_cliente where tipo_mensaje <> 'Opinión'")
        mensajes = sum(1 for result in mensajesTodos)
        if mensajes == 0:
            mensajes = 0
        mensajesproductos = MensajeProducto.objects.all()
        mensajesproductos_Dudas = Mensaje_Cliente.objects.filter(tipo_mensaje="Duda")
        mensajesproductos_Sugerencia= Mensaje_Cliente.objects.filter(tipo_mensaje="Sugerencia")
        mensajesproductos_Reclamacion = Mensaje_Cliente.objects.filter(tipo_mensaje="Reclamación")
        request.session['tipo_mensaje'] = "dudas"
        context = {"mensajes":mensajes,"mensajesProductos":mensajesproductos,"mensajesProductos_Dudas":mensajesproductos_Dudas,"mensajesProductos_Sugerencias":mensajesproductos_Sugerencia,"mensajesProductos_Reclamacion":mensajesproductos_Reclamacion}
        return render(request,'supermercado/administracion/mailbox/mailbox.html',context)
    else:
        return HttpResponseRedirect(reverse("index"))

def view_mailbox_reclamaciones(request):
    if request.user.is_authenticated and request.session['isA']:
        mensajesTodos = Mensaje_Cliente.objects.raw(
            "select * from supermercadoApp_mensaje_cliente where tipo_mensaje <> 'Opinión'")
        mensajes = sum(1 for result in mensajesTodos)
        if mensajes == 0:
            mensajes = 0
        mensajesproductos = MensajeProducto.objects.all()
        mensajesproductos_Dudas = Mensaje_Cliente.objects.filter(tipo_mensaje="Duda")
        mensajesproductos_Sugerencia= Mensaje_Cliente.objects.filter(tipo_mensaje="Sugerencia")
        mensajesproductos_Reclamacion = Mensaje_Cliente.objects.filter(tipo_mensaje="Reclamación")
        request.session['tipo_mensaje'] = "reclamaciones"
        context = {"mensajes":mensajes,"mensajesProductos":mensajesproductos,"mensajesProductos_Dudas":mensajesproductos_Dudas,"mensajesProductos_Sugerencias":mensajesproductos_Sugerencia,"mensajesProductos_Reclamacion":mensajesproductos_Reclamacion}
        return render(request,'supermercado/administracion/mailbox/mailbox.html',context)
    else:
        return HttpResponseRedirect(reverse("index"))

def view_mailbox_sugerencias(request):
    if request.user.is_authenticated and request.session['isA']:
        mensajesTodos = Mensaje_Cliente.objects.raw(
            "select * from supermercadoApp_mensaje_cliente where tipo_mensaje <> 'Opinión'")
        mensajes = sum(1 for result in mensajesTodos)
        if mensajes == 0:
            mensajes = 0
        mensajesproductos = MensajeProducto.objects.all()
        mensajesproductos_Dudas = Mensaje_Cliente.objects.filter(tipo_mensaje="Duda")
        mensajesproductos_Sugerencia= Mensaje_Cliente.objects.filter(tipo_mensaje="Sugerencia")
        mensajesproductos_Reclamacion = Mensaje_Cliente.objects.filter(tipo_mensaje="Reclamación")
        request.session['tipo_mensaje'] = "sugerencias"
        context = {"mensajes":mensajes,"mensajesProductos":mensajesproductos,"mensajesProductos_Dudas":mensajesproductos_Dudas,"mensajesProductos_Sugerencias":mensajesproductos_Sugerencia,"mensajesProductos_Reclamacion":mensajesproductos_Reclamacion}
        return render(request,'supermercado/administracion/mailbox/mailbox.html',context)
    else:
        return HttpResponseRedirect(reverse("index"))

def view_mailbox_readMail(request,id_mensaje):
    if request.user.is_authenticated and request.session['isA']:
        mensajeLectura = Mensaje_Cliente.objects.get(pk = id_mensaje)
        mensajeLecturaProducto = MensajeProducto.objects.get(mensaje=mensajeLectura)
        mensajesTodos = Mensaje_Cliente.objects.raw(
            "select * from supermercadoApp_mensaje_cliente where tipo_mensaje <> 'Opinión'")
        mensajes = sum(1 for result in mensajesTodos)
        if mensajes == 0:
            mensajes = 0
        mensajesproductos = MensajeProducto.objects.all()
        mensajesproductos_Dudas = Mensaje_Cliente.objects.filter(tipo_mensaje="Duda")
        mensajesproductos_Sugerencia = Mensaje_Cliente.objects.filter(tipo_mensaje="Sugerencia")
        mensajesproductos_Reclamacion = Mensaje_Cliente.objects.filter(tipo_mensaje="Reclamación")
        if mensajeLectura.tipo_mensaje == "Duda":
            request.session['tipo_mensaje'] = "duda"
        elif mensajeLectura.tipo_mensaje == "Sugerencia":
            request.session['tipo_mensaje'] = "sugerencias"
        elif mensajeLectura.tipo_mensaje == "Reclamación":
            request.session['tipo_mensaje'] = "reclamación"
        context = {"mensajes": mensajes, "mensajesProductos": mensajesproductos,
                   "mensajesProductos_Dudas": mensajesproductos_Dudas,
                   "mensajesProductos_Sugerencias": mensajesproductos_Sugerencia,
                   "mensajesProductos_Reclamacion": mensajesproductos_Reclamacion,
                   "mensajeLectura":mensajeLectura,
                   "mensajeLecturaProducto":mensajeLecturaProducto}

        return render(request,'supermercado/administracion/mailbox/read-mail.html',context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_mailbox_redactar(request):
    if request.user.is_authenticated and request.session['isA']:
        mensajesTodos = Mensaje_Cliente.objects.raw(
            "select * from supermercadoApp_mensaje_cliente where tipo_mensaje <> 'Opinión'")
        mensajes = sum(1 for result in mensajesTodos)
        if mensajes == 0:
            mensajes = 0
        mensajesproductos = MensajeProducto.objects.all()
        mensajesproductos_Dudas = Mensaje_Cliente.objects.filter(tipo_mensaje="Duda")
        mensajesproductos_Sugerencia = Mensaje_Cliente.objects.filter(tipo_mensaje="Sugerencia")
        mensajesproductos_Reclamacion = Mensaje_Cliente.objects.filter(tipo_mensaje="Reclamación")
        clientes = Cliente.objects.all()
        form = MensajeEmailForm()
        request.session['tipo_mensaje'] = "sugerencias"
        context = {"mensajes": mensajes, "mensajesProductos": mensajesproductos,
                   "mensajesProductos_Dudas": mensajesproductos_Dudas,
                   "mensajesProductos_Sugerencias": mensajesproductos_Sugerencia,
                   "mensajesProductos_Reclamacion": mensajesproductos_Reclamacion,
                   "clientes":clientes,
                   "form": form
                   }

        return render(request,'supermercado/administracion/mailbox/redactar.html',context)
    else:
        return HttpResponseRedirect(reverse("index"))


def view_mailbox_responderMail(request,id_mensaje):
    if request.user.is_authenticated and request.session['isA']:
        mensajeLectura = Mensaje_Cliente.objects.get(pk = id_mensaje)
        mensajesTodos = Mensaje_Cliente.objects.raw(
            "select * from supermercadoApp_mensaje_cliente where tipo_mensaje <> 'Opinión'")
        mensajes = sum(1 for result in mensajesTodos)
        if mensajes == 0:
            mensajes = 0
        mensajesproductos = MensajeProducto.objects.all()
        mensajesproductos_Dudas = Mensaje_Cliente.objects.filter(tipo_mensaje="Duda")
        mensajesproductos_Sugerencia = Mensaje_Cliente.objects.filter(tipo_mensaje="Sugerencia")
        mensajesproductos_Reclamacion = Mensaje_Cliente.objects.filter(tipo_mensaje="Reclamación")
        clientes = Cliente.objects.all()
        form = MensajeEmailForm(instance=mensajeLectura)
        request.session['tipo_mensaje'] = "sugerencias"
        context = {"mensajes": mensajes, "mensajesProductos": mensajesproductos,
                   "mensajesProductos_Dudas": mensajesproductos_Dudas,
                   "mensajesProductos_Sugerencias": mensajesproductos_Sugerencia,
                   "mensajesProductos_Reclamacion": mensajesproductos_Reclamacion,
                   "mensajeLectura":mensajeLectura,
                   "clientes": clientes,
                   "form":form
                   }

        return render(request,'supermercado/administracion/mailbox/redactar.html',context)
    else:
        return HttpResponseRedirect(reverse("index"))


def delete_mensaje(request, id_mensaje, id_mensajeproducto):
    if request.user.is_authenticated and request.session['isA']:
        MensajeProducto.objects.get(pk = id_mensajeproducto).delete()
        Mensaje_Cliente.objects.get(pk=id_mensaje).delete()
        return HttpResponseRedirect(reverse('mailbox'))
    else:
        return HttpResponseRedirect(reverse("index"))


def generarPDF(request,id_factura):
    factura = Factura.objects.get(pk = id_factura)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Factura'+factura.codigo + factura.cli_dni+'.pdf"'

    buffer = BytesIO()
    izquierda = ParagraphStyle('parrafos',
                               alignment=TA_LEFT,
                               fontSize=12,
                               spaceAfter=6,
                               spaceBefore = 6,
                               fontName="Times-Roman")
    detalle2 = ParagraphStyle('cabeceradetalle',
                             alignment=TA_LEFT,
                             fontSize=15,
                             spaceAfter=6,
                             spaceBefore=6,
                             fontName="Helvetica")
    detalle = ParagraphStyle('cabeceradetalle',
                             alignment=TA_LEFT,
                             fontSize=12,
                             spaceAfter=6,
                             spaceBefore=6,
                             fontName="Helvetica")
    textoFinal = ParagraphStyle('textoFinal',
                             alignment=TA_CENTER,
                             fontSize=12,
                             spaceAfter=6,
                             spaceBefore=6,
                             fontName="Helvetica")
    documento = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    cliente_p = Paragraph(u"<b>Cliente:</b> " + factura.cli_dni + ' |  ' + factura.cli_nombre + " " + factura.cli_apellidos, izquierda)
    socio_p = Paragraph(u" ", izquierda)
    if factura.cli_socio == 1:
        socio_p = Paragraph(u"<b>Socio del supermercado</b> " ,izquierda)
    direccion_p = Paragraph(u"<b>Dirección entrega y facturación:</b> " + factura.cli_tipo_via + ' '  + factura.cli_direccion + ' ' + str(factura.cli_portal) + ' ' + str(factura.cli_escalera) + ' ' + str(factura.cli_piso) + ' ' + str(factura.cli_casa), izquierda)
    localidad_p = Paragraph(u"<b>Localidad:</b> " + factura.cli_cp + ', '+ factura.cli_localidad + ' - Provincia: ' + factura.cli_provincia,izquierda)
    telefono_p = Paragraph(u"<b>Télefono/s:</b> " + factura.cli_telefono1 + ' | ' + factura.cli_telefono2, izquierda)
    im = Image(settings.MEDIA_ROOT + '/pdf/logo.png', width=120, height=80, hAlign='LEFT')
    separacioncomponente = Image(settings.MEDIA_ROOT + '/pdf/separacioncomponentes.png', width=550, height=30)
    separacion = Image(settings.MEDIA_ROOT + '/pdf/separacion.png', width=550, height=10)
    story.append(im)
    story.append(separacioncomponente)
    texto = Paragraph(u"<u><b>FACTURA</b> Nº " + str(factura.codigo) + '</u>', detalle2)
    story.append(texto)
    story.append(separacion)
    story.append(socio_p)
    story.append((cliente_p))
    story.append((direccion_p))
    story.append((localidad_p))
    story.append((telefono_p))
    story.append(separacioncomponente)
    cabeceraProductos_p = Paragraph(u"DETALLE DE FACTURA", detalle)
    story.append(cabeceraProductos_p)

    encabezados = ('Código de producto', 'Producto', 'Cantidad', 'Precio', 'Total')
    lista_productos = []
    for factura_data in DetalleFactura.objects.filter(factura_id=id_factura):
        lista_productos.append((factura_data.prod_codigo, factura_data.prod_nombre, str(factura_data.prod_cantidad), str("{0:.2f}".format(factura_data.prod_pvp).replace('.', ',')), str("{0:.2f}".format(factura_data.prod_total).replace('.', ','))))
        lista_productos.reverse()
    detalle_orden = Table([encabezados] + lista_productos, colWidths=[100, 190, 50, 50, 60])
    # Aplicamos estilos a las celdas de la tabla
    detalle_orden.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (4, -1), 2, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 3, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
            # # La primera fila(encabezados) va a estar centrada
            # ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            # # Los bordes de todas las celdas serán de color negro y con un grosor de 1
            # ('GRID', (0, 0), (-1, -1), 0, colors.transparent),
            # # El tamaño de las letras de cada una de las celdas será de 10
            # ('FONTSIZE', (0, 0), (0, 0), 10),

        ]
    ))
    story.append(detalle_orden)
    story.append(separacioncomponente)
    cabeceraFinal_p = Paragraph(u"IMPORTE DE LA FACTURA", detalle)
    story.append(cabeceraFinal_p)
    if factura.cli_socio == 1:
        encabezados = ('Subtotal','DESCUENTO','IVA','IMPORTE TOTAL')
        lista_detalleFinal = []
        lista_detalleFinal.append((str("{0:.2f}".format(factura.subtotal).replace('.',',')),str("{0:.2f}".format(factura.cli_descuento).replace('.',',')),str("{0:.2f}".format(factura.impuesto).replace('.',',')),str("{0:.2f}".format(factura.importe_total).replace('.',',')) + "€"))
        detalleFinal_orden = Table([encabezados] + lista_detalleFinal, colWidths=[150, 110, 100,90])
        # Aplicamos estilos a las celdas de la tabla
        detalleFinal_orden.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (4, -1), 2, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 3, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
                # # La primera fila(encabezados) va a estar centrada
                # ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                # # Los bordes de todas las celdas serán de color negro y con un grosor de 1
                # ('GRID', (0, 0), (-1, -1), 0, colors.transparent),
                # # El tamaño de las letras de cada una de las celdas será de 10
                # ('FONTSIZE', (0, 0), (0, 0), 10),

            ]
        ))
    else:
        encabezados = ('Subtotal', 'IVA', 'IMPORTE TOTAL')
        lista_detalleFinal = []
        lista_detalleFinal.append((str("{0:.2f}".format(factura.subtotal).replace('.', ',')),
                                   str("{0:.2f}".format(factura.impuesto).replace('.', ',')),
                                   str("{0:.2f}".format(factura.importe_total).replace('.', ',')) + "€"))
        detalleFinal_orden = Table([encabezados] + lista_detalleFinal, colWidths=[180, 140, 130, 0])
        # Aplicamos estilos a las celdas de la tabla
        detalleFinal_orden.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (4, -1), 2, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 3, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
                # # La primera fila(encabezados) va a estar centrada
                # ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                # # Los bordes de todas las celdas serán de color negro y con un grosor de 1
                # ('GRID', (0, 0), (-1, -1), 0, colors.transparent),
                # # El tamaño de las letras de cada una de las celdas será de 10
                # ('FONTSIZE', (0, 0), (0, 0), 10),

            ]
        ))
    story.append(detalleFinal_orden)
    story.append(separacioncomponente)
    story.append(separacioncomponente)

    textoFinal = Paragraph(u"Gracias por comprar en Evian Supermercados", textoFinal)
    story.append(textoFinal)
    story.append(Spacer(0, 15))
    documento.build(story)
    response.write(buffer.getvalue())
    buffer.close()
    return response



def sendMail(request):
    destinomensaje = request.POST['destino_mensaje']
    asuntomensaje = request.POST['asunto_mensaje']
    form = MensajeEmailForm(request.POST)
    cuerpomensaje = form.__getitem__('mensaje').value()
    email = EmailMessage(asuntomensaje, cuerpomensaje, to=[destinomensaje])
    email.content_subtype = "html"  # Main content is now text/html
    email.send()
    return HttpResponseRedirect(reverse('mailbox'))