from django.conf.urls import url
from . import views,views_public

urlpatterns = [
    url(r'^$', views_public.view_index, name='index'),


#############################     PARTE ADMINISTRACIÓN     #############################
    url(r'^administracion/$', views.view_administracion, name='index_admin'),
    url(r'^login/$', views.login_action, name='login'),
    url(r'^logout_empll/$', views.logout_empl, name='logoutempll'),


    url(r'^productos/$', views.view_productos, name='productos'),
    url(r'^productos_alta/$', views.view_producto_alta, name='productos_alta'),
    url(r'^productos_edit/(?P<id_producto>[0-9]+)/$', views.view_producto_edit, name='productos_editar'),
    url(r'^add_producto/$', views.add_producto, name='add_producto'),
    url(r'^edit_producto/(?P<id_producto>[0-9]+)/$', views.edit_producto, name='edit_producto'),
    url(r'^delete_producto/(?P<id_producto>[0-9]+)/$', views.delete_producto, name='producto_delete'),

    url(r'^categorias/$', views.view_categorias, name='categorias'),
    url(r'^categoria_alta/$', views.view_categoria_alta, name='categoria_alta'),
    url(r'^categoria_edit/(?P<id_categoria>[0-9]+)/$', views.view_categoria_edit, name='categoria_editar'),
    url(r'^add_categoria/$', views.add_categoria, name='add_categoria'),
    url(r'^edit_categoria/(?P<id_categoria>[0-9]+)/$', views.edit_categoria, name='edit_categoria'),
    url(r'^delete_categoria/(?P<id_categoria>[0-9]+)/$', views.delete_categoria, name='categoria_delete'),

    url(r'^usuarios/$', views.view_usuarios, name='usuarios'),
    url(r'^usuarios_alta/$', views.view_usuario_alta, name='usuarios_alta'),
    url(r'^add_usuario/$', views.add_usuario, name='add_usuario'),
    url(r'^usuarios_edit/(?P<id_usuario>[0-9]+)/$', views.view_usuario_edit, name='usuarios_editar'),
    url(r'^edit_usuario/(?P<id_usuario>[0-9]+)/$', views.edit_usuario, name='edit_usuario'),
    url(r'^delete_usuario/(?P<id_usuario>[0-9]+)/$', views.delete_usuario, name='usuario_delete'),

    url(r'^clientes/$', views.view_clientes, name='clientes'),
    url(r'^clientes_alta/$', views.view_cliente_alta, name='clientes_alta'),
    url(r'^add_cliente/$', views.add_cliente, name='add_cliente'),
    url(r'^clientes_edit/(?P<id_usuario>[0-9]+)/$', views.view_cliente_edit, name='clientes_editar'),
    url(r'^edit_cliente/(?P<id_usuario>[0-9]+)/$', views.edit_cliente, name='edit_cliente'),
    url(r'^delete_cliente/(?P<id_cliente>[0-9]+)/$', views.delete_cliente, name='cliente_delete'),

    url(r'^tarjetas/$', views.view_tarjetas, name='tarjetas'),
    url(r'^tarjetas_alta/$', views.view_tarjeta_alta, name='tarjetas_alta'),
    url(r'^add_tarjeta/$', views.add_tarjeta, name='add_tarjeta'),
    url(r'^add_tarjeta_cliente/(?P<id_cliente>[0-9]+)/$', views.addTarjetaToCliente, name='add_tarjeta_cliente'),
    url(r'^tarjetas_edit/(?P<id_tarjeta>[0-9]+)/$', views.view_tarjeta_edit, name='tarjetas_editar'),
    url(r'^edit_tarjeta/(?P<id_tarjeta>[0-9]+)/$', views.edit_tarjeta, name='edit_tarjeta'),
    url(r'^delete_tarjeta/(?P<id_tarjeta>[0-9]+)/$', views.delete_tarjeta, name='tarjeta_delete'),

    url(r'^carritos/$', views.view_carritos, name='carritos'),
    url(r'^carrito_confirmar/(?P<id_carrito>[0-9]+)/$', views.confirmarCarrito, name='carrito_confirmar'),
    url(r'^carrito_add/$', views.view_carrito_alta, name='carrito_alta'),
    url(r'^carrito_productos/(?P<id_carrito>[0-9]+)/$', views.view_carrito_productos, name='carrito_producto'),
    url(r'^carrito_productos_add/(?P<id_carrito>[0-9]+)/$', views.view_carrito_producto_add, name='carrito_producto_alta'),
    url(r'^add_producto_carrito/$', views.add_producto_carrito, name='add_producto_carrito'),
    url(r'^add_carrito/$', views.add_carrito, name='add_carrito'),
    url(r'^carrito_edit/(?P<id_carrito>[0-9]+)/$', views.view_carrito_edit, name='carrito_editar'),
    url(r'^carrito_producto_edit/(?P<id_producto_carrito>[0-9]+)/$', views.view_producto_carrito, name='carrito_producto_edit'),
    url(r'^edit_carrito/(?P<id_carrito>[0-9]+)/$', views.edit_carrito, name='edit_carrito'),
    url(r'^edit_carrito_producto/(?P<id_producto_carrito>[0-9]+)/$', views.producto_carrito_edit, name='edit_carrito_producto'),
    url(r'^delete_carrito/$', views.delete_carrito, name='carrito_delete'),
    url(r'^delete_producto_carrito/(?P<id_producto_carrito>[0-9]+)/$', views.delete_producto_carrito, name='producto_carrito_delete'),

    url(r'^facturas/$', views.view_facturas, name='facturas'),
    url(r'^generar_factura/(?P<id_carrito>[0-9]+)/$', views.generar_factura, name='generar_factura'),
    url(r'^factura_detalle/(?P<id_factura>[0-9]+)/$', views.view_facturas_detalle, name='factura_detalle'),
    url(r'^factura_generarPDF/(?P<id_factura>[0-9]+)/$', views.generarPDF, name='facturaPDF'),

    url(r'^opiniones/$', views.view_opiniones, name='opiniones'),
    url(r'^mostrar_mensaje/(?P<id_mensaje>[0-9]+)/$', views.opinion_ver, name='opinion_ver'),
    url(r'^opinion_espera/(?P<id_mensaje>[0-9]+)/$', views.opinion_enEspera, name='opinion_espera'),
    url(r'^opinion_aceptar/(?P<id_mensaje>[0-9]+)/$', views.aceptar_opinion, name='opinion_aceptar'),
    url(r'^opinion_rechazar/(?P<id_mensaje>[0-9]+)/$', views.rechazar_opinion, name='opinion_rechazar'),
    url(r'^delete_opinion/(?P<id_mensaje>[0-9]+)/(?P<id_mensajeproducto>[0-9]+)/$', views.delete_opinion, name='opinion_delete'),


    url(r'^mail/$', views.view_mailbox, name='mailbox'),
    url(r'^mail_dudas/$', views.view_mailbox_dudas, name='mail_dudas'),
    url(r'^mail_sugerencias/$', views.view_mailbox_sugerencias, name='mail_sugerencias'),
    url(r'^mail_reclamaciones/$', views.view_mailbox_reclamaciones, name='mail_reclamaciones'),
    url(r'^mail_read/(?P<id_mensaje>[0-9]+)/$', views.view_mailbox_readMail, name='mailbox_read'),
    url(r'^mail_redactar/$', views.view_mailbox_redactar, name='mailbox_redactar'),
    url(r'^mail_responder/(?P<id_mensaje>[0-9]+)/$', views.view_mailbox_responderMail, name='mailbox_responder'),
    url(r'^mail_eliminar/(?P<id_mensaje>[0-9]+)/(?P<id_mensajeproducto>[0-9]+)/$', views.delete_mensaje, name='mail_delete'),
    url(r'^mail_enviar/$', views.sendMail, name='mail_enviar'),




    #############################     PARTE PUBLICA     #############################
    url(r'^logout/$', views_public.logout_cli, name='logout_cli'),
    url(r'^register/$', views_public.view_register, name='register'),
    url(r'^nuevo_cliente/$', views_public.view_cliente_register, name='cli_register'),
    url(r'^add_nuevo_cliente/$', views_public.add_cliente, name='cli_add_register'),
    url(r'^mis-datos/$', views_public.view_cliente_edit, name='cli_view_edit'),
    url(r'^mi-perfil/$', views_public.view_cliente_menu, name='cli_menu'),
    url(r'^editar-mis-datos/$', views_public.edit_cliente, name='cli_edit'),
    url(r'^solicitar-tarjeta-socio/$', views_public.addTarjetaToCliente, name='cli_tarjeta_add'),

    url(r'^mi-carrito/$', views_public.view_carrito_compra, name='cli_carrito'),
    url(r'^mi-carrito-producto-actualizar/(?P<id_producto_carrito>[0-9]+)/(?P<id_carrito>[0-9]+)/$', views_public.update_producto_carrito,name='cli_producto_carrito_update'),
    url(r'^quitar-producto-mi-carrito/(?P<id_producto_carrito>[0-9]+)/$', views_public.delete_producto_carrito,name='cli_producto_carrito_delete'),
    url(r'^proceder-pago-mi-carrito/$', views_public.view_procederCompra, name='cli_procederCompra'),
    url(r'^thank-you/$', views_public.checkout, name='cli_finCompra'),


    url(r'^tienda/$', views_public.view_tienda, name='cli_tienda'),
    url(r'^tienda-buscar/$', views_public.tienda_autocompletaBusqueda, name='cli_tienda_buscar'),
    url(r'^tienda-categoria/(?P<id_categoria>[0-9]+)/$', views_public.view_tienda_by_categoria, name='cli_tienda_categoria'),
    url(r'^tienda-producto-detalle/(?P<id_producto>[0-9]+)/$', views_public.view_producto_detalle, name='cli_producto_detalle'),
    url(r'^tienda-add-producto/(?P<id_producto>[0-9]+)/$', views_public.add_producto_carrito, name='cli_add_producto_carrito'),
    url(r'^mensaje/(?P<id_producto>[0-9]+)/$', views_public.cli_add_mensaje, name='cli_enviar_mensaje'),


    url(r'^contacto/$', views_public.view_contacto, name='cli_contacto'),
    url(r'^contacto-mensaje/$', views_public.sendMail, name='cli_contacto_mensaje'),

    url(r'^tarjeta-socio/$', views_public.view_tarjetaSocio, name='cli_tarjetaSocio'),
]