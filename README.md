# Proyecto
## Pensamiento Computacional para Ingeniería
### Esteban Padilla Cerdio
#### A01703068

---------------------------------------------------------

Descripción:

Por medio de una aplicación basada en la librería OpenCV para Python, este proyecto servirá como un apoyo para los individuos que sufran de alguna discapacidad visual, permitiéndoles identificar el monto de un billete de pesos mexicanos con el uso de su cámara. El prototipo actual utiliza algoritmos de reconocimiento de contornos, líneas continuas, líneas rectas y rectángulos para identificar la posible ubicación de billetes dentro de la imagen. Una vez identificadas las áreas en donde es posible que exista un billete en cuadro, se calcula el color promedio del área en cuestión, para así definir la probabilidad de que el billete fotografiado posea uno de tres valores distintos.

Limitaciones:

Los algoritmos actuales no tienen la velocidad suficiente como para identificar los billetes en tiempo real por medio de video, por lo que es necesario utilizar fotografías. Igualmente, la mala calidad o falta de luz en algunas fotografías dificulta la detección de los billetes, por lo que se han precargado siete imagenes donde ésto no es un problema. 

Instrucciones:

Antes de comenzar con el programa, es necesario descargar las siete imágenes que se encuentran en este repositorio y colocarlas, sin cambiarles el nombre, dentro de la misma carpeta que el programa. Es posible sustituir alguna de ellas con una personal, siempre y cuando mantenga el nombre.

