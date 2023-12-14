# PL-OCR-2023
 Optical-Character-Recognition System:--------MATCOM--2023--Adrián Hernández Castellanos
 
 Este repositorio contiene el código fuente de un Sistema de Reconocimiento Óptico de Caracteres, al cual se le insertará una imagen o conjunto de imágenes y se generará el texto contenido en las imágenes a través de una interfaz gráfica. El proyecto está desarrollado en el lenguaje de programación Python con las herramientas especificadas a continuación...

 Herramientas utilizadas en el desarrollo de este proyecto:
 -Python 3.12.0         (Lenguaje de programación)
 -OpenCV 4.8.1.78       (Procesaminto de imágenes)
 -Matplotlib 3.8.0      (Operaciones de mapeo de imágenes)
 -Pytesseract           (Modelo de aprendizaje preentrenado con herramientas de OCR)

 INSTRUCCIONES DE USO:
 -> Al ser una versión portable, el OCR no necesita una instalación. El ejecutable se puede compilar a partir del archivo main.py
 -> Antes de iniciar, debe copiar las imágenes que desea convertir a la carpeta _Content_
 -> Al ejecutar el sistema se generará un archivo .txt en la carpeta Output con el nombre de la imágen y su conteido
 -> Los formatos de imágen admitidos son: *.jpg y .png*

 BREVE EXPLICACIÓN DEL FUNCIONAMIENTO:
 Este proyecto usa dos herramientas fundamentales para realizar su función.
 OpenCV es una biblioteca de visión computacional con una extensa cantidad de métodos que ofrecen múltiples variantes de procesamiento de imágenes para desarrollar sistemas de interpretación, comprensión, búsqueda y predicción de datos relacionados o contenidos en una imágen.
 El trabajo de esta biblioteca de clases en este sistema no es más que recibir una entrada y optimizarla según sus condiciones, aplicando los filtros adecuados para mejorar la calidad del análisis posterior.
 Por otro lado, Tesseract es una biblioteca con un modelo preentrenado integrado, útil para encontrar cuadros de texto y caracteres en imágenes. El entrenamiento recibido previamente por este modelo ha sido mejorado a partir de redes neuronales conocidas como Long Short-Term Memory. También cuenta con una funcionalidad de post-procesado en la cual se corrigen las predicciones del sistema en comparación con las respuestas esperadas a partir de la información del dataset. Este modelo puede ser entrenado bajo un contexto específico para estimular y mejorar su efectividad en dicho espacio. Por ejemplo, usando texto manuscrito en un lenguaje específico.
 El sistema consta de 3 partes de funcionamiento que se complementan con el preprocesamiento de la imagen:
 --Detección de líneas de texto: La cual constituye la principal ejecución del programa, y se encarga de trazar una búsqueda de un fragmento rectangular de texto con irregularidades despreciables en los cuales su contenido contenga gran cantidad de bordes .
 --Identificación de caracteres: Analizar la estructura de cada borde, realizar un mapeo y comparar con los caracteres del conjunto de datos para retornar una respuesta cercana a lo esperado.
 --Estructuramiento del texto a devolver