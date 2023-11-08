[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8796826&assignment_repo_type=AssignmentRepo)
# Trabajo Práctico de Estructuras de Datos - 2022
#### Fecha de entrega: 02/11/2022

El objetivo de este trabajo práctico, es poner en práctica y sobre todo en código, los conocimientos adquiridos en la materia en un caso práctico.
## Consigna
En este TP vamos a investigar un tema que nos resulte interesante. El primer paso consiste en seleccionar un tema de actualidad que les gustaría trabajar, por ejemplo elecciones, vacunación contra el covid 2019, Pycon 2022, etc. Pueden proponer un tema que sea de su interés. El principal requisito es que haya información en twitter. Una vez definido el tema deben recopilar información disponible en twitter y portales de noticias sobre el tema, para formar un corpus. Se debe recopilar información al menos durante 2 semanas para armar nuestro corpus. 
Antes de empezar es necesario planificar el formato en que se va a guardar la información en crudo que se recopile (por ejemplo formato de archivos JSON para Twitter y XML para RSS) que luego les permita procesarlos para formar índices invertidos.
## Primer entregable (12/10/2022): 
Código fuente recopilación de tweets: Debe permitir recopilar información del stream en vivo de twitter y almacenarlos automáticamente en disco. El programa debe mostrar por pantalla su estado (fecha y hora de inicio, cantidad de tweets recolectados hasta el momento, cantidad de bytes recolectados hasta el momento). Se debe detener cuando se presione Control-C.
Para la primera entrega es necesario realizar las siguientes lecturas obligatorias y aplicar sus conceptos.

[Cómo construir una query en Twitter](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query)

[Construcción de filtros de alta calidad para obtener datos de Twitter](https://developer.twitter.com/en/docs/tutorials/building-high-quality-filters)

## Segundo entregable (02/11/2022):
Se deberá programar un buscador (y un menú que permita operarlo) de información que permita resolver:

**1. Consultas por fechas y horas:** por ejemplo los m primeros tweets de un usuario dado en un rango de fechas y horas. Los m primeros tweets de todos los usuarios en un rango de fechas y horas determinados (donde m es un parámetro de la búsqueda)

**2. Consultas de palabras o frases:** se debe permitir consultas booleanas (con los operadores and, not y or) de palabras o frases. Estas consultas deben devolver los m primeros tweets correspondientes, donde m es un parámetro de la búsqueda. Por ejemplo: (“Del Potro” and “Murray” and not “Copa Davis”, 10) debería traer los 10 primeros tweets que mencionan a Del Potro y a Andy Murray y que no mencionen a la Copa Davis.

El buscador se deberá programar sobre uno o varios índices invertidos en disco.
## Entregables opcionales
#### Módulo de estadísticas: 
Ranking de las n palabras más mencionadas en tweets, o usuario de  Twitter. Por ejemplo: las 10 palabras más frecuentes de todos los tweets recopilados. Las 10 palabras más usadas por un usuario determinado de twitter.
Ranking de las n palabras más mencionadas en los tweets en forma global. Idem anterior
#### Índice invertido comprimido:
Comprimir tanto la lista de apariciones como el índice propiamente dicho según las técnicas vistas en clase
## Entregas
#### Primera entrega: 
Cada grupo deberá pactar una reunión con su tutor asignado para presentarle los entregables mencionados.
#### Segunda entrega:

Se deberá entregar un informe en formato notebook de jupyter, con fragmentos de código embebido. El informe debe incluir diagrama de clases (si corresponde), decisiones de diseño, análisis de las páginas de los sitios seleccionados.
Junto al informe se deberán entregar código fuente, con menú para realizar pruebas y pruebas unitarias.

## Defensa
La defensa del trabajo consta de dos etapas: el armado de un video explicando y demostrando el sistema, y la defensa en una reunión por Meet con su tutor asignado.

#### Video explicativo
El video explicativo de menos de 10 minutos, deberá dar cuenta de:
- una demostración de uso
- las decisiones de diseño aplicadas
- las clases utilizadas
- las técnicas de programación que se emplearon

Esto deberá realizarse mediante algún software de captura de pantalla, con explicaciones mediante texto hablado. En pocas palabras: como un screencast.

Para simplificar el esfuerzo, se permite que sólamente un integrante muestre y hable en el video, ya que compilar los fragmentos implica un esfuerzo adicional que no reviste mayor beneficio.

El video deberá entregarse por YouTube, en forma de video oculto (accesible por dirección) el día de la entrega del trabajo, junto con la entrega anteriormente descrita.

#### Defensa por Meet
Una vez que los docentes revisen los videos y consideren que el trabajo se encuentra en condiciones de ser defendido, coordinarán con su tutor un momento en el que puedan realizar una videoconferencia para defender su trabajo.

Durante la misma, el tutor realizará preguntas para profundizar sobre las decisiones de diseño, la funcionalidad, y algunas ideas adicionales.
Se evaluará a todos los integrantes del grupo, por lo que es conveniente para esa ocasión tener micrófono y cámara disponibles, a modo de hacer la llamada más amena.

La configuración más simple es utilizar el teléfono celular para la llamada, con auriculares.
