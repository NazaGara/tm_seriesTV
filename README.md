# Más allá del sentimiento binario: descubriendo posiciones sobre un tema

Repositorio correspondiente al proyecto final de la materia Text-Mining del año 2021 de la carrera de Licenciatura en Ciencias de la Computación en FaMAF - UNC.

## Instalacion

Clonamos el repositorio:

`git clone https://github.com/NazaGara/clustering-tm.git`

## Uso

Se puede usar de dos formas, una local, para el cual hay que instalar las librerias necesarias y puede demandar mucha memoria y computo. O sino, se puede usar [Google Colab](https://colab.research.google.com/). Personalmente, recomiendo usarlo en Google Colab.

### Requisitos
Para instalar las librerias necesarias, ejecuta el comando:

```bash
pip install jupyter
pip install -r requirements.txt

jupyter-notebook clustering.ipynb
```
## Objetivo

El objetivo es el de poder hacer un analisis de sentimiento a tweets que hablen sobre elgun tema en particular, e identificar mas alla de la clasificacion: POSITIVO - NEGATIVO - NEUTRAL para ademas, poder entender sobre que temas en particular habla un tweet tratando de identificar la causa latente del sentimiento impuesto en el comentario.

### Caso de Estudio

Tome como caso de estudio tweets relacionados con la serie El Juego del Calamar, ya que al momento de comenzar el proyecto, la serie era muy discutida en las redes sociales, por lo que podia juntar un buen volumen de tweets rapidamente para poder comenzar a analizarlo.

Obtuve tweets utilizando la API de Twitter, con el impedimento de poder sacar solo tweets recientemente publicados y una pequeña fraccion de ellos extraidos a la fecha de lanzamiento de la serie.

Cuando llegue al numero de 19717 tweets, deje de buscar por nuevos datos y fije el corpus.

## Metodologia de trabajo

El acercamiento que tuve para desarrollar el proyecto fue el siguiente:

Pre-Processing -> Sentiment Analysis -> Vectorization -> Clustering -> Extraction -> Model Training -> Prediction

Hasta la etapa de Clustering, el modo de trabajo fue muy similar al del practico de Clustering, con la gran diferencia de que esta vez, agrupamos documentos (tweets) en vez de palabras, por lo que pude utilizar [CountVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html). Al mismo tiempo que nosotros trabajamos con cada tweet, tambien procese los datos usando un Word Embedding de FastText de 100 dimensiones entrenado con informacion de Twitter, para luego poder comparar los resultados entre ambas versiones.

### Pre-Processing

Una vez que ya tenia todos los tweets, el preprocesamiento de los tweets consistio de:

- Eliminar stopwords y URLs
- Eliminar signos de puntuacion y simbolo '@'
- Descartar palabras que tengan una frecuencia menor a 80
- Aplicar reduccion de dimensionalidad mediante la varianza de los datos
- Identificar sentimiento de cada tweet mediante la libreria: [PySentimiento](https://github.com/pysentimiento/pysentimiento)

Con esta limpieza de los datos, ahora si ya podiamos vectorizar y obtener una matriz de datos con la cual trabajar. Hay que hacer notar, que la vectorizacion de los datos y en el clustering no utilizo el sentimiento de cada tweet.

Por lo que al final de la etapa de clustering, tenemos 20 clusters de tweets, los cuales se agruparon por su semejanza, no por su sentimiento, por lo que en cada cluster podemos tener tweets con diferentes sentimientos, lo cual usamos para la parte de extraccion y entrenamiento del modelo.

Tenemos entonces, dos versiones de Clusters, una dada por la vectorizacion mas manual y otra por la realizada con el Embedding:

Version con Count Vectorizer:
![vectorization](https://imgur.com/qCBj6O3.png)


Usando embeddings:
![embeddings](https://imgur.com/V5zktXE.png)


### Extraction and Model Training

Hasta este momento, tenia en claro como trabajar y que pasos iba a realizar. Desde la etapa de extraccion probe diferentes formas de poder llegar al objetivo, hare mencion de aquellas mas relevantes.

En un primer intento se intento utilizar el algoritmo de K-Nearest Neighbors para poder predecir, la idea era la de aplicar KNN en los distintos clusters y taggear manualmente cada centroide con un sentimiento y la razon del mismo. Pero esta version se descarto por el desgaste de hacerlo manualmente y que convenia mas aplicar en el preprocesamiento un analisis al sentimiento de cada tweet.

### Predictions

## Resultados

### Trabajo futuro

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)

## Alumno
Garagiola, Nazareno