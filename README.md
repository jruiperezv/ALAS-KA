# ALAS-KA


1. GUIA DE INSTALACION

En este apéndice se recogen los pasos para realizar la instalación e integración del código de ALAS-KA con el de Khan Academy

ELEMENTOS COMUNES E INDEPENDIENTES:
En este punto se comentan cuáles son los elementos comunes entre ALAS-KA y Khan Academy que hay que unificar y cuales son independientes el uno del otro.
- Elementos independientes:
  - La carpeta static_viewer, contiene los ficheros estáticos de ALAS-KA, entre ellos las imágenes necesarias y las hojas de estilo CSS.
  - Paquete viewer_code, contiene todo el código perteneciente a ALAS-KA de manera qué es mucho más sencillo ya que todo está aglutinado en un solo paquete
- Elementos comunes que hay que unificar entre ALAS-KA y Khan Academy:
  - El fichero main.py dónde está el mapping de las diferentes URL.
  - Fichero app.yaml de configuración de la aplicación .
  - Fichero cron.yaml de configuración de tareas cron job.
  - Fichero queue.yaml de configuración de queues.


PROCESO DE INSTALACIÓN DE ALAS-KA:

  1.1. UNIFICACIÓN DEL CÓDIGO

En primer lugar hay que unificar el código generado para ALAS-KA con el ya existente de Khan Academy. Eso implica que hay que copiar los elementos independientes a la raíz de Khan Academy y unificar los que son comunes añadiendo el código de ALAS-KA a los ficheros ya existentes de Khan Academy:
- Se introducen la carpeta static_viewer y el paquete viewer_code en la carpeta raíz de Khan Academy
- En el fichero main.py hay que añadir el mapping de las URL a las clases nuevas que hacen referencia en ALAS-KA. También añadir los import de dichas clases nuevas. Por esto se entiende que cuando llegue al sistema una petición get a dicha URL tendrá que redirigirla a las nuevas clases de ALAS-KA debidas que antes no estaban en Khan Academy.
- En el fichero app.yaml que es el archivo de configuración de la aplicación hay que realizar varias modificaciones. En primer lugar hay que habilitar la consola interactiva mediante el código necesario, esto ha sido ya explicado en la sección de Pruebas Realizadas en ALAS-KA. La segunda acción es incluir la librería el código para habilitar la librería de Numpy en  su versión “1.6.1”. Por último incluir el mapping del static dir para acceso a los recursos estáticos ubicados en la carpeta static_viewer.
- Introducir en el fichero cron.yaml las 6 tareas cron job desarrolladas para ALAS-KA sin modificar las existentes de Khan Academy.
- Introducir en el fichero queue.yaml las 6 queues desarrolladas para ALAS-KA sin modificar las existentes de Khan Academy.

En definitiva aunque todo este listado de modificaciones pueda parecer tedioso, de forma resumida lo único que hay que hacer es copiar todo el código generado para ALAS-KA en los archivos de Khan Academy sin sobrescribir ni modificar el código original.

  1.2. ADAPTACIÓN DEL CÓDIGO AL CURSO

Debido a que cada curso está compuesto por unos ejercicios y vídeos diferentes, así como su fecha de inicio, hay algunos detalles que hay que adaptar.
- Ya que los cursos tienen diferentes fechas de inicio, hay que adaptar la medida de la media y varianza (para calcular la constancia del alumno) poniendo el día de la fecha de inicio del curso. Para ello hay que modificar en el viewer_code/viewer_cron/time_distribution.py dentro de la función constancy_meanvar(self, usuario) la variable startDate a la fecha de inicio del curso.
- Los nombres de los ejercicios y las youtube_id de los vídeos también cambia por lo que hay que hacer esta adaptación también. En el fichero del script de carga de ejercicios y vídeos denominado scripts/exercise_videos_script.py escribir en la variable listaEjercicios los nombres de todos los ejercicios pertenecientes a dicho curso. De la misma forma en la variable listaVideos escribir las youtube_id de los vídeos del curso.
- También sería posible añadir un enlace a ALAS-KA en la pantalla inicial de Khan Academy que llevara a los usuarios de forma más sencilla a la pantalla inicial que está ubicada en http://(yourappid).appspot.com/menu_viewer.

  1.3. EJECUCIÓN DE SCRIPTS Y ASIGNACIÓN DE PERMISOS

En este paso habría que ejecutar los script necesarios para que se generen las entidades de ALAS-KA ViewerUser, ViewerExercise y ViewerVideo.

- En primer lugar hay que acceder a la consola interactiva, de la misma forma que se ha explicado en la sección de pruebas. La URL donde estará ubicada es http://(yourappid).appspot.com/admin/interactive.
- Se puede ejecutar el script para cargar los ejercicios y videos, como se ha dicho antes ubicado en scripts/exercise_videos_script.py sólo habría que copiar el contenido y ejecutarlo en la consola interactiva. Este script cargará los vídeos y ejercicios de las entidades Exercise y Video de Khan Academy necesarios para el curso, a las entidades de ALAS-KA ViewerExercise y ViewerVideo
- De la misma forma para cargar los usuarios existentes de la entidad UserData de Khan Academy a la entidad ViewerUser de ALAS-KA, se ejecuta el script situado en scripts/script_load_users.py.
- Ahora es necesario adjudicar los diferentes permisos, uno de los puntos de trabajo futuro es realizar una nterfaz para la administración de los diferentes permisos de los diferentes usuarios de ALAS-KA. Debido a que en la actualidad todavía no se encuentra disponible, hay que modificar estos permisos a mano desde la interfaz del Datastore. Por lo tanto desde la interfaz de administración de Google App Engine, en la pestaña del Datastore Viewer (se explicó su acceso en la sección de Validación y Verificación). Se accede a la entidad de ViewerUser y se tiene que ir usuario en usuario asignando los permisos. Para los profesores, hay que poner la propiedad professor = True, de forma similar para los alumnos habrá que poner la propiedad student = True. En caso de que ese usuario no tenga permisos y no deba acceder a las visualizaciones, habrá que dejar ambas propiedades a False.


2. MANUAL DE USUARIO

En este apéndice se va a hacer una revisión de las diferentes pantallas de ALAS-KA, que permitirán recorrer la interfaz y conocer los tipos de interacción que se puede hacer en cada una de las pantallas. Esta guía puede ayudar al usuario a entender la funcionalidad que existe implementada en la aplicación y como usarla de forma general.

INTRODUCCIÓN:
ALAS-KA es una herramienta de learning analytics que está basada en la plataforma de Khan Academy. Su objetivo es el de ofrecer unas visualizaciones de distintos tipos de información que puedan ayudar a los profesores y alumnos a mejorar el proceso de aprendizaje durante el curso en la plataforma de Khan Academy. Los alumnos van a poder acceder a las visualizaciones de sus propios parámetros pero no a las del resto de alumnos o a la clase. Los profesores podrán ver las visualizaciones de todos los alumnos del curso y también otras globales de la clase.

https://cloud.githubusercontent.com/assets/5990099/7161736/f07e7a7a-e390-11e4-8329-124760fb96bc.png

La forma de acceder a ALAS-KA es relativamente sencilla. Su sistema de log-in está asociado al mismo que utiliza Khan Academy, por lo tanto sólo se tiene que acceder a Khan Academy desde la URL habitual y hacer log-in. Una vez hecho esto puedes acceder a ALAS-KA desde la URL situada en http://your_khan_academy_url/menu_viewer.
La figura 88 muestra el menú de entrada en ALAS-KA. En el home de la interfaz de entrada se puede ver una breve descripción de la plataforma y unas tablas que están organizadas por los bloques de parámetros así como los distintos parámetros que los componen. Si se pone el ratón por encima de cualquiera de los bloques de medidas o de alguno de los parámetros, saltará el cuadro que sale en la imagen con una breve descripción para que se pueda comprender cada uno de ellos. Esto puede ayudar al usuario a ver en que bloques se agrupan las medidas y que información se muestra en cada uno de ellos, de esta forma dependiendo de qué tipo de información desee recibir acudirá a uno o a otro. También se puede leer la descripción de cada uno de los parámetros por separado para analizar con más exactitud qué información transmite cada uno de ellos.
Por otra parte, en caso de que se desee contactar con las personas participantes en la plataforma, las direcciones de contacto se pueden encontrar en la pantalla about como se ve en la figura 89.

https://cloud.githubusercontent.com/assets/5990099/7161745/ff963c3c-e390-11e4-8deb-a793a6c14e8b.png

En las secciones siguientes se van a describir cuáles son las visualizaciones que se pueden acceder y su significado.
VISUALIZACIONES INDIVIDUALES:
Para acceder a las visualizaciones individuales de los diferentes estudiantes hay que pinchar en la pestaña user del menú de ALAS-KA. Esto nos lleva a una interfaz en la que hay dos cajas de selección: en la primera denominada “Select the student” se pueden elegir los distintos estudiantes de la clase, y en la segunda llamada “Type of measure” se puede acceder al tipo de medidas que se quieren consultar. Las existentes en el tipo de medidas coincidirán con las tablas vistas en home y cada una de ellas incluirá dichos parámetros. Una vez que las dos cajas de selección tengan elementos escogidos, aparecerá la visualización acorde a lo que se haya elegido. También se puede ir cambiando las cajas e irán cambiando las visualizaciones acorde a su selección. Se puede ver dicha interfaz en la figura 90.

En cada uno de los bloques de medidas aparecen una serie de parámetros representados por visualizaciones de barras. Además aparece una tabla en la parte inferior que resume de forma verbal las diferentes medidas sobre dicho usuario, donde también se puede observar la definición de dichas medidas poniendo el curso por encima de ellas. En la figura 91 se puede observar las visualizaciones del bloque Uso Total de la Plataforma.

https://cloud.githubusercontent.com/assets/5990099/7161765/2556a89e-e391-11e4-8eac-2ca002731de2.png

En la imagen 91 se muestra el bloque de medidas de Uso Total de la Plataforma, que está orientado a ofrecer parámetros sobre el uso que han hecho los usuarios de los distintos elementos en la plataforma. La idea general de las visualizaciones, como se puede ver en la figura anterior, es la de mostrar en cada medida dos barras, una barra que haga referencia al usuario y otra que haga referencia al valor medio de la clase en dicho parámetro. Esto posibilita el darse cuenta si ese usuario destaca o está por debajo de la clase en dicho parámetro. La mayoría de las medidas están dadas de 0 a 100 en forma de porcentaje, el mantener el formato de esta forma facilita la compresión de las medidas, aunque hay en algunas que ha sido poco conveniente el mostrarlas en forma de porcentaje, por lo que no se ha hecho.
Analizando los usuarios de forma individual se puede saber cuál es su utilización de la plataforma, el progreso que han hecho u otros parámetros de diversa índole. Esto puede ayudar al profesor a realizar un seguimiento más personalizado para hacer recomendaciones, evitar que alumnos no consigan completar el curso de forma satisfactorio o conocer mejor el tipo de persona con la que está tratando y que forma de enseñanza pudiera ser más eficiente.

Otra de las visualizaciones disponibles son las de tipo de barra acumulada. Se puede ver un ejemplo en el bloque de medidas de Distribución del Tiempo de Uso de la Plataforma, en la medida para ver el uso temporal por intervalos. Se ve dicha gráfica en la figura 92.

https://cloud.githubusercontent.com/assets/5990099/7161784/30069f24-e391-11e4-8679-508cd9be45bb.png

La idea en esta visualización es que la barra completa represente el 100% del tiempo y sea rellenada por los distintos periodos de tiempo en los que ha trabajado. Por lo tanto el intervalo proporcional del total de la barra relleno por los diferentes colores (mañana, tarde y noche) representará el porcentaje de tiempo que dicho usuario ha trabajado en dicho intervalo. La barra inferior mostraría la misma idea, pero sobre el tiempo total de todos los usuarios de la plataforma, de esta forma también se puede comparar si el usuario en cuestión trabaja más que la media del resto de la clase en cada intervalo.

https://cloud.githubusercontent.com/assets/5990099/7161798/3982f91c-e391-11e4-85f1-667c58cfdf35.png

En la figura 93 se incluyen las gráficas de barras y la tabla con la descripción de dicho alumno. Dicha tabla sirve como un soporte adicional a las visualizaciones realizando una descripción verbal

de cuáles son los resultados de cada parámetro para dicho usuario. Por cada uno de los parámetros se definen unos umbrales mediante los cuales se agrupan los usuarios en 5 grupos y en base a dichos grupos se realiza la descripción que parece en las tablas posteriormente. Estos umbrales son también los mismos que se usan posteriormente para las visualizaciones de clase.
VISUALIZACIONES DE CLASE:
Para acceder a las visualizaciones de clase tan sólo hay que acceder a la pestaña class en el menú de ALAS-KA. Lo cual llevará a una pantalla de funcionamiento similar a la de user, pero en la que sólo hay una caja de selección denominada “Type of measure”, ya que las visualizaciones son de la clase completa y no se puede cambiar entre los diferentes estudiantes. En la figura 94 se puede ver un ejemplo de las gráficas de clase del grupo de medidas Progreso Correcto en la Plataforma.

https://cloud.githubusercontent.com/assets/5990099/7161800/4233e666-e391-11e4-9bb6-da0f995336d4.png

Como se puede ver en cada una de los parámetros se ofrecen 5 grupos para cada uno de los parámetros. Los umbrales de cada uno de estos intervalos son comunes con las tablas de descripción verbal en la pestaña user de visualizaciones individuales. Este tipo de gráficas pueden ayudar a obtener una idea de la clase de forma general, por ejemplo de una simple ojeada se podría ver qué porcentaje de la clase ha hecho un gran avance en vídeos o ejercicios, para saber cuál es el avance medio de la clase. También hay otras visualizaciones de clase que son algo diferentes, se puede ver un par de ejemplos en la siguiente figura.

https://cloud.githubusercontent.com/assets/5990099/7161801/47282f2e-e391-11e4-8b8d-9fe4dcb5242b.png

