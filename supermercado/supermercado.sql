-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 30-11-2018 a las 11:28:28
-- Versión del servidor: 5.7.24-0ubuntu0.18.04.1
-- Versión de PHP: 7.2.10-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `supermercado`
--
USE supermercado;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add permission', 2, 'add_permission'),
(5, 'Can change permission', 2, 'change_permission'),
(6, 'Can delete permission', 2, 'delete_permission'),
(7, 'Can add group', 3, 'add_group'),
(8, 'Can change group', 3, 'change_group'),
(9, 'Can delete group', 3, 'delete_group'),
(10, 'Can add user', 4, 'add_user'),
(11, 'Can change user', 4, 'change_user'),
(12, 'Can delete user', 4, 'delete_user'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add carrito', 7, 'add_carrito'),
(20, 'Can change carrito', 7, 'change_carrito'),
(21, 'Can delete carrito', 7, 'delete_carrito'),
(22, 'Can add categoria', 8, 'add_categoria'),
(23, 'Can change categoria', 8, 'change_categoria'),
(24, 'Can delete categoria', 8, 'delete_categoria'),
(25, 'Can add cliente', 9, 'add_cliente'),
(26, 'Can change cliente', 9, 'change_cliente'),
(27, 'Can delete cliente', 9, 'delete_cliente'),
(28, 'Can add detalle factura', 10, 'add_detallefactura'),
(29, 'Can change detalle factura', 10, 'change_detallefactura'),
(30, 'Can delete detalle factura', 10, 'delete_detallefactura'),
(31, 'Can add factura', 11, 'add_factura'),
(32, 'Can change factura', 11, 'change_factura'),
(33, 'Can delete factura', 11, 'delete_factura'),
(34, 'Can add mensaje_ cliente', 12, 'add_mensaje_cliente'),
(35, 'Can change mensaje_ cliente', 12, 'change_mensaje_cliente'),
(36, 'Can delete mensaje_ cliente', 12, 'delete_mensaje_cliente'),
(37, 'Can add perfil_ usuario', 13, 'add_perfil_usuario'),
(38, 'Can change perfil_ usuario', 13, 'change_perfil_usuario'),
(39, 'Can delete perfil_ usuario', 13, 'delete_perfil_usuario'),
(40, 'Can add producto', 14, 'add_producto'),
(41, 'Can change producto', 14, 'change_producto'),
(42, 'Can delete producto', 14, 'delete_producto'),
(43, 'Can add producto_ carrito', 15, 'add_producto_carrito'),
(44, 'Can change producto_ carrito', 15, 'change_producto_carrito'),
(45, 'Can delete producto_ carrito', 15, 'delete_producto_carrito'),
(46, 'Can add supermercado', 16, 'add_supermercado'),
(47, 'Can change supermercado', 16, 'change_supermercado'),
(48, 'Can delete supermercado', 16, 'delete_supermercado'),
(49, 'Can add tarjeta', 17, 'add_tarjeta'),
(50, 'Can change tarjeta', 17, 'change_tarjeta'),
(51, 'Can delete tarjeta', 17, 'delete_tarjeta'),
(52, 'Can add mensaje producto', 18, 'add_mensajeproducto'),
(53, 'Can change mensaje producto', 18, 'change_mensajeproducto'),
(54, 'Can delete mensaje producto', 18, 'delete_mensajeproducto');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'sha1$IHJIyr8yeIGW$4a9f5a77da89f7be9a01db0ad695200e243e9658', '2018-11-29 16:31:03.256917', 1, 'miguelangel', 'Miguel Angel', 'Barba', 'miguel.angel.langarita@gmail.com', 1, 1, '2018-11-29 16:26:31.324013'),
(2, 'sha1$pNITtlKmKPNO$bada855548194994d4b7af09aac45f55ea37aea7', '2018-11-29 16:33:35.441606', 0, 'jmanrique', '', '', '', 0, 1, '2018-11-29 16:33:34.928555');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2018-11-29 16:30:32.369481', '1', '17762131J -  ', 1, '[{\"added\": {}}]', 13, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'supermercadoApp', 'carrito'),
(8, 'supermercadoApp', 'categoria'),
(9, 'supermercadoApp', 'cliente'),
(10, 'supermercadoApp', 'detallefactura'),
(11, 'supermercadoApp', 'factura'),
(18, 'supermercadoApp', 'mensajeproducto'),
(12, 'supermercadoApp', 'mensaje_cliente'),
(13, 'supermercadoApp', 'perfil_usuario'),
(14, 'supermercadoApp', 'producto'),
(15, 'supermercadoApp', 'producto_carrito'),
(16, 'supermercadoApp', 'supermercado'),
(17, 'supermercadoApp', 'tarjeta');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2018-11-29 16:25:01.083861'),
(2, 'auth', '0001_initial', '2018-11-29 16:25:10.206385'),
(3, 'admin', '0001_initial', '2018-11-29 16:25:12.430934'),
(4, 'admin', '0002_logentry_remove_auto_add', '2018-11-29 16:25:12.555547'),
(5, 'contenttypes', '0002_remove_content_type_name', '2018-11-29 16:25:13.813485'),
(6, 'auth', '0002_alter_permission_name_max_length', '2018-11-29 16:25:13.946804'),
(7, 'auth', '0003_alter_user_email_max_length', '2018-11-29 16:25:14.079431'),
(8, 'auth', '0004_alter_user_username_opts', '2018-11-29 16:25:14.151362'),
(9, 'auth', '0005_alter_user_last_login_null', '2018-11-29 16:25:14.742039'),
(10, 'auth', '0006_require_contenttypes_0002', '2018-11-29 16:25:14.784239'),
(11, 'auth', '0007_alter_validators_add_error_messages', '2018-11-29 16:25:14.838624'),
(12, 'auth', '0008_alter_user_username_max_length', '2018-11-29 16:25:15.893557'),
(13, 'sessions', '0001_initial', '2018-11-29 16:25:17.049712'),
(14, 'supermercadoApp', '0001_initial', '2018-11-29 16:25:30.903861'),
(15, 'supermercadoApp', '0002_auto_20180511_0956', '2018-11-29 16:25:32.627717'),
(16, 'supermercadoApp', '0003_auto_20180511_0958', '2018-11-29 16:25:35.063361'),
(17, 'supermercadoApp', '0004_auto_20180511_1324', '2018-11-29 16:25:37.445740'),
(18, 'supermercadoApp', '0005_auto_20180511_1406', '2018-11-29 16:25:42.279504'),
(19, 'supermercadoApp', '0006_auto_20180511_1411', '2018-11-29 16:25:43.516489'),
(20, 'supermercadoApp', '0007_auto_20180511_1412', '2018-11-29 16:25:44.163310'),
(21, 'supermercadoApp', '0008_auto_20180511_1800', '2018-11-29 16:25:44.643152'),
(22, 'supermercadoApp', '0009_auto_20180511_1843', '2018-11-29 16:25:45.845181'),
(23, 'supermercadoApp', '0010_auto_20180511_1856', '2018-11-29 16:25:46.310544'),
(24, 'supermercadoApp', '0011_auto_20180511_1939', '2018-11-29 16:25:46.717052'),
(25, 'supermercadoApp', '0012_auto_20180512_1029', '2018-11-29 16:25:48.487386'),
(26, 'supermercadoApp', '0013_auto_20180512_1153', '2018-11-29 16:25:53.522243'),
(27, 'supermercadoApp', '0014_auto_20180515_0830', '2018-11-29 16:25:53.936201'),
(28, 'supermercadoApp', '0015_auto_20180515_0905', '2018-11-29 16:25:54.618279'),
(29, 'supermercadoApp', '0016_auto_20180515_1143', '2018-11-29 16:25:55.669945'),
(30, 'supermercadoApp', '0017_auto_20180515_1455', '2018-11-29 16:25:56.202499'),
(31, 'supermercadoApp', '0018_auto_20180517_1642', '2018-11-29 16:25:56.558770'),
(32, 'supermercadoApp', '0019_auto_20180517_1726', '2018-11-29 16:25:57.554446'),
(33, 'supermercadoApp', '0020_auto_20180517_1956', '2018-11-29 16:25:58.721512'),
(34, 'supermercadoApp', '0021_auto_20180517_2004', '2018-11-29 16:25:59.782561');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('xs6rb09wvx81blzsk7ze72nf86n5knbi', 'MzMyZDBlMjFlNzk0MDY2ZGRkYzA5OTliZDBhNDlkNjA2ZGEyNTc3OTp7ImNsaV9uYXZiYXJfYWN0aXZlIjoiY2Fycml0byIsImlzQSI6MCwiaWRfdXNyIjoyLCJpZF9jbGkiOjEsImNsaV9ub21icmUiOiJKYXZpZXIiLCJjbGlfYXBlbGxpZG9zIjoiTWFucmlxdWUgUGVsbGVqZXJvIiwiY2xpX2ltYWdlcHJvZmlsZSI6ImNsaWVudGUvZGVmYXVsdC5wbmciLCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNDc5YzRhODQwOTc0MDQ2ZWFkZDc5MGNjZDdiNzE2Y2Y0YjkyZmJmOSJ9', '2018-12-13 16:33:39.256948');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_carrito`
--

CREATE TABLE `supermercadoApp_carrito` (
  `id` int(11) NOT NULL,
  `fecha_inicio` datetime(6) NOT NULL,
  `fecha_confirmacion` datetime(6) DEFAULT NULL,
  `cliente_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `supermercadoApp_carrito`
--

INSERT INTO `supermercadoApp_carrito` (`id`, `fecha_inicio`, `fecha_confirmacion`, `cliente_id`) VALUES
(1, '2018-11-29 16:33:35.540427', NULL, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_categoria`
--

CREATE TABLE `supermercadoApp_categoria` (
  `id` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `observaciones` varchar(4000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `supermercadoApp_categoria`
--

INSERT INTO `supermercadoApp_categoria` (`id`, `nombre`, `observaciones`) VALUES
(1, 'Lacteos', ''),
(2, 'Carne', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_cliente`
--

CREATE TABLE `supermercadoApp_cliente` (
  `id` int(11) NOT NULL,
  `dni` varchar(9) NOT NULL,
  `image` varchar(100) NOT NULL,
  `nombre` varchar(80) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `cp` varchar(5) NOT NULL,
  `tipo_via` varchar(10) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `portal` int(11) NOT NULL,
  `escalera` varchar(10) DEFAULT NULL,
  `piso` int(11) NOT NULL,
  `casa` varchar(10) NOT NULL,
  `localidad` varchar(200) NOT NULL,
  `provincia` varchar(200) NOT NULL,
  `telefono1` varchar(9) NOT NULL,
  `telefono2` varchar(9) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `token` varchar(15) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `supermercadoApp_cliente`
--

INSERT INTO `supermercadoApp_cliente` (`id`, `dni`, `image`, `nombre`, `apellidos`, `cp`, `tipo_via`, `direccion`, `portal`, `escalera`, `piso`, `casa`, `localidad`, `provincia`, `telefono1`, `telefono2`, `email`, `token`, `user_id`) VALUES
(1, '26056941B', 'cliente/default.png', 'Javier', 'Manrique Pellejero', '50014', 'CALLE', 'Cyberwatcher', 18, NULL, 5, 'A', 'ZARAGOZA', 'ZARAGOZA', '976123122', '650122123', 'jmanriquepellejero@gmail.com', NULL, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_detallefactura`
--

CREATE TABLE `supermercadoApp_detallefactura` (
  `id` int(11) NOT NULL,
  `prod_codigo` varchar(12) NOT NULL,
  `prod_nombre` varchar(120) NOT NULL,
  `prod_descripcion_corta` varchar(250) NOT NULL,
  `prod_pvp` double NOT NULL,
  `prod_categoria` int(11) NOT NULL,
  `prod_cantidad` int(11) NOT NULL,
  `prod_total` double NOT NULL,
  `factura_id` int(11) NOT NULL,
  `prod_iva` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_factura`
--

CREATE TABLE `supermercadoApp_factura` (
  `id` int(11) NOT NULL,
  `codigo` varchar(40) NOT NULL,
  `cli_dni` varchar(9) NOT NULL,
  `cli_nombre` varchar(80) NOT NULL,
  `cli_apellidos` varchar(100) NOT NULL,
  `cli_cp` varchar(5) NOT NULL,
  `cli_tipo_via` varchar(50) NOT NULL,
  `cli_direccion` varchar(200) NOT NULL,
  `cli_portal` int(11) NOT NULL,
  `cli_escalera` varchar(10) DEFAULT NULL,
  `cli_piso` int(11) NOT NULL,
  `cli_casa` varchar(10) DEFAULT NULL,
  `cli_localidad` varchar(200) NOT NULL,
  `cli_provincia` varchar(200) NOT NULL,
  `cli_telefono1` varchar(9) NOT NULL,
  `cli_telefono2` varchar(9) DEFAULT NULL,
  `cli_email` varchar(254) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `subtotal` double NOT NULL,
  `impuesto` double NOT NULL,
  `importe_total` double NOT NULL,
  `cli_socio` int(11) NOT NULL,
  `cli_descuento` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_mensajeproducto`
--

CREATE TABLE `supermercadoApp_mensajeproducto` (
  `id` int(11) NOT NULL,
  `mensaje_id` int(11) NOT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `estado_mensaje` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_mensaje_cliente`
--

CREATE TABLE `supermercadoApp_mensaje_cliente` (
  `id` int(11) NOT NULL,
  `tipo_mensaje` varchar(11) NOT NULL,
  `mensaje` varchar(1000) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `cliente_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_perfil_usuario`
--

CREATE TABLE `supermercadoApp_perfil_usuario` (
  `id` int(11) NOT NULL,
  `dni` varchar(9) NOT NULL,
  `image` varchar(100) NOT NULL,
  `cp` varchar(5) NOT NULL,
  `tipo_via` varchar(10) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `portal` int(11) NOT NULL,
  `escalera` varchar(10) DEFAULT NULL,
  `piso` int(11) NOT NULL,
  `casa` varchar(10) NOT NULL,
  `localidad` varchar(200) NOT NULL,
  `provincia` varchar(200) NOT NULL,
  `telefono1` varchar(9) NOT NULL,
  `telefono2` varchar(9) DEFAULT NULL,
  `token` varchar(15) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `supermercadoApp_perfil_usuario`
--

INSERT INTO `supermercadoApp_perfil_usuario` (`id`, `dni`, `image`, `cp`, `tipo_via`, `direccion`, `portal`, `escalera`, `piso`, `casa`, `localidad`, `provincia`, `telefono1`, `telefono2`, `token`, `user_id`) VALUES
(1, '17762131J', 'admin/cyberwatcher.png', '50014', 'CALLE', 'CALLE CYBERCAMP', 18, '', 6, 'A', 'ZARAGOZA', 'ZARAGOZA', '976123123', '650123123', 'jmdo2h39hd928hc', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_producto`
--

CREATE TABLE `supermercadoApp_producto` (
  `id` int(11) NOT NULL,
  `codigo` varchar(12) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `descripcion` varchar(4000) NOT NULL,
  `descripcion_corta` varchar(250) NOT NULL,
  `imagen` varchar(100) NOT NULL,
  `stock` int(11) NOT NULL,
  `pvp` double NOT NULL,
  `pvp_socio` double NOT NULL,
  `diferencia_en_tarjeta` tinyint(1) NOT NULL,
  `ean13` varchar(100) NOT NULL,
  `categoria_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_producto_carrito`
--

CREATE TABLE `supermercadoApp_producto_carrito` (
  `id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `importe_total` double NOT NULL,
  `carrito_id` int(11) NOT NULL,
  `producto_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_supermercado`
--

CREATE TABLE `supermercadoApp_supermercado` (
  `id` int(11) NOT NULL,
  `NIF` varchar(9) NOT NULL,
  `responsable` varchar(200) NOT NULL,
  `direccion` varchar(4000) NOT NULL,
  `telefono1` varchar(9) NOT NULL,
  `tiene_parking` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supermercadoApp_tarjeta`
--

CREATE TABLE `supermercadoApp_tarjeta` (
  `id` int(11) NOT NULL,
  `num_tarjeta` varchar(50) NOT NULL,
  `fecha_adquisicion` datetime(6) NOT NULL,
  `saldo_actual` double NOT NULL,
  `cliente_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `supermercadoApp_carrito`
--
ALTER TABLE `supermercadoApp_carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `supermercadoApp_carr_cliente_id_99e72ef9_fk_supermerc` (`cliente_id`);

--
-- Indices de la tabla `supermercadoApp_categoria`
--
ALTER TABLE `supermercadoApp_categoria`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `supermercadoApp_cliente`
--
ALTER TABLE `supermercadoApp_cliente`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `dni` (`dni`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `token` (`token`);

--
-- Indices de la tabla `supermercadoApp_detallefactura`
--
ALTER TABLE `supermercadoApp_detallefactura`
  ADD PRIMARY KEY (`id`),
  ADD KEY `supermercadoApp_deta_factura_id_0787f23d_fk_supermerc` (`factura_id`);

--
-- Indices de la tabla `supermercadoApp_factura`
--
ALTER TABLE `supermercadoApp_factura`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `supermercadoApp_mensajeproducto`
--
ALTER TABLE `supermercadoApp_mensajeproducto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `supermercadoApp_mens_mensaje_id_b4488e51_fk_supermerc` (`mensaje_id`),
  ADD KEY `supermercadoApp_mens_producto_id_576a0a03_fk_supermerc` (`producto_id`);

--
-- Indices de la tabla `supermercadoApp_mensaje_cliente`
--
ALTER TABLE `supermercadoApp_mensaje_cliente`
  ADD PRIMARY KEY (`id`),
  ADD KEY `supermercadoApp_mens_cliente_id_0f87aae7_fk_supermerc` (`cliente_id`);

--
-- Indices de la tabla `supermercadoApp_perfil_usuario`
--
ALTER TABLE `supermercadoApp_perfil_usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `dni` (`dni`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `token` (`token`);

--
-- Indices de la tabla `supermercadoApp_producto`
--
ALTER TABLE `supermercadoApp_producto`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`),
  ADD KEY `supermercadoApp_prod_categoria_id_578094fd_fk_supermerc` (`categoria_id`);

--
-- Indices de la tabla `supermercadoApp_producto_carrito`
--
ALTER TABLE `supermercadoApp_producto_carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `supermercadoApp_prod_carrito_id_b9f448d8_fk_supermerc` (`carrito_id`),
  ADD KEY `supermercadoApp_prod_producto_id_63194256_fk_supermerc` (`producto_id`);

--
-- Indices de la tabla `supermercadoApp_supermercado`
--
ALTER TABLE `supermercadoApp_supermercado`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `NIF` (`NIF`);

--
-- Indices de la tabla `supermercadoApp_tarjeta`
--
ALTER TABLE `supermercadoApp_tarjeta`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `num_tarjeta` (`num_tarjeta`),
  ADD KEY `supermercadoApp_tarj_cliente_id_0d918a4e_fk_supermerc` (`cliente_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;
--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_carrito`
--
ALTER TABLE `supermercadoApp_carrito`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_categoria`
--
ALTER TABLE `supermercadoApp_categoria`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_cliente`
--
ALTER TABLE `supermercadoApp_cliente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_detallefactura`
--
ALTER TABLE `supermercadoApp_detallefactura`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_factura`
--
ALTER TABLE `supermercadoApp_factura`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_mensajeproducto`
--
ALTER TABLE `supermercadoApp_mensajeproducto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_mensaje_cliente`
--
ALTER TABLE `supermercadoApp_mensaje_cliente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_perfil_usuario`
--
ALTER TABLE `supermercadoApp_perfil_usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_producto`
--
ALTER TABLE `supermercadoApp_producto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_producto_carrito`
--
ALTER TABLE `supermercadoApp_producto_carrito`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_supermercado`
--
ALTER TABLE `supermercadoApp_supermercado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `supermercadoApp_tarjeta`
--
ALTER TABLE `supermercadoApp_tarjeta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `supermercadoApp_carrito`
--
ALTER TABLE `supermercadoApp_carrito`
  ADD CONSTRAINT `supermercadoApp_carr_cliente_id_99e72ef9_fk_supermerc` FOREIGN KEY (`cliente_id`) REFERENCES `supermercadoApp_cliente` (`id`);

--
-- Filtros para la tabla `supermercadoApp_cliente`
--
ALTER TABLE `supermercadoApp_cliente`
  ADD CONSTRAINT `supermercadoApp_cliente_user_id_7b417571_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `supermercadoApp_detallefactura`
--
ALTER TABLE `supermercadoApp_detallefactura`
  ADD CONSTRAINT `supermercadoApp_deta_factura_id_0787f23d_fk_supermerc` FOREIGN KEY (`factura_id`) REFERENCES `supermercadoApp_factura` (`id`);

--
-- Filtros para la tabla `supermercadoApp_mensajeproducto`
--
ALTER TABLE `supermercadoApp_mensajeproducto`
  ADD CONSTRAINT `supermercadoApp_mens_mensaje_id_b4488e51_fk_supermerc` FOREIGN KEY (`mensaje_id`) REFERENCES `supermercadoApp_mensaje_cliente` (`id`),
  ADD CONSTRAINT `supermercadoApp_mens_producto_id_576a0a03_fk_supermerc` FOREIGN KEY (`producto_id`) REFERENCES `supermercadoApp_producto` (`id`);

--
-- Filtros para la tabla `supermercadoApp_mensaje_cliente`
--
ALTER TABLE `supermercadoApp_mensaje_cliente`
  ADD CONSTRAINT `supermercadoApp_mens_cliente_id_0f87aae7_fk_supermerc` FOREIGN KEY (`cliente_id`) REFERENCES `supermercadoApp_cliente` (`id`);

--
-- Filtros para la tabla `supermercadoApp_perfil_usuario`
--
ALTER TABLE `supermercadoApp_perfil_usuario`
  ADD CONSTRAINT `supermercadoApp_perfil_usuario_user_id_57d7fe7b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `supermercadoApp_producto`
--
ALTER TABLE `supermercadoApp_producto`
  ADD CONSTRAINT `supermercadoApp_prod_categoria_id_578094fd_fk_supermerc` FOREIGN KEY (`categoria_id`) REFERENCES `supermercadoApp_categoria` (`id`);

--
-- Filtros para la tabla `supermercadoApp_producto_carrito`
--
ALTER TABLE `supermercadoApp_producto_carrito`
  ADD CONSTRAINT `supermercadoApp_prod_carrito_id_b9f448d8_fk_supermerc` FOREIGN KEY (`carrito_id`) REFERENCES `supermercadoApp_carrito` (`id`),
  ADD CONSTRAINT `supermercadoApp_prod_producto_id_63194256_fk_supermerc` FOREIGN KEY (`producto_id`) REFERENCES `supermercadoApp_producto` (`id`);

--
-- Filtros para la tabla `supermercadoApp_tarjeta`
--
ALTER TABLE `supermercadoApp_tarjeta`
  ADD CONSTRAINT `supermercadoApp_tarj_cliente_id_0d918a4e_fk_supermerc` FOREIGN KEY (`cliente_id`) REFERENCES `supermercadoApp_cliente` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
