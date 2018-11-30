# SSOP (Safe & Secure Owner Password)

## ssop

Nuestra plataforma.

Aqui el usuario podrá registrarse por primera vez en la plataforma. Será también la plataforma sobre la que se conectarán los sitios que
tengan que hacer uso de ésta para identificar a sus usuarios. La idea es utilizar **OpenID** para esa comunicación.

## envio_moviles

Es parte de nuestra plataforma. Se encarga del envío de los SMS al móvil del usuario. Utilizamos la librería [Twilio](https://www.twilio.com) que permite el envío
de SMS gratuitos previo registro de los destinatarios. Nos servirá para hacer una demo con alguno de nuestros números.

## supermercado
Es la web de prueba que usaremos para conectar con nuestra plataforma.
Pertenece a un desarrollo propio pero anterior al hackathon. Aqui sólo añadiremos los cambios que permitan la conexión con ssop para la
identificación del usuario en el momento de validarse.

## Presentación PPT y PDF
*   https://github.com/CyberWatcherOrg/SSOP/tree/master/Presentacion_Hackathon
