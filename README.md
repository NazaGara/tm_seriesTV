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

### Pre procesamiento

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


### Extraccion de datos y entrenamiento

Hasta este momento, tenia en claro como trabajar y que pasos iba a realizar. Desde la etapa de extraccion probe diferentes formas de poder llegar al objetivo, hare mencion de aquellas mas relevantes.

En un primer intento se intento utilizar el algoritmo de K-Nearest Neighbors para poder predecir, la idea era la de aplicar KNN en los distintos clusters y taggear manualmente cada centroide con un sentimiento y la razon del mismo. Pero esta version se descarto por el desgaste de hacerlo manualmente y que convenia mas aplicar en el preprocesamiento un analisis al sentimiento de cada tweet.

#### PMI
La siguiente idea fue utilizar una version de [Pointwise Mutual Information](https://en.wikipedia.org/wiki/Pointwise_mutual_information) especifica para la situacion que tenemos, tal que en cada cluster se puedan identificar las palabras que mas reflejen un sentimiento. Es decir, dentro de un conjunto de datos (todo el dataset o solo un cluster) poder aplicar la formula:

![PMI](https://imgur.com/SUkc17C.png)

Para la implementacion en codigo, necesito de una serie de colecciones para cada cluster y contadores de palabras para diferentes Dataframes, junto con un minimo de cantidad de veces que aparezca una palabra en el conjunto de datos.

```python
pmi = {}
for w in sent_counter:
    pmi[w] = np.log2(sent_counter[w]/(counter[w] * amount_of_sent_on_df))
Counter(pmi)
```

Finalmente, solo nos quedamos con las 5 palabras mas significantes de cada sentimiento para cada cluster, por ejemplo:

| Sentimiento   | word1         | word2  | word3 | word4 | word 5|
| ------------- |:-------------:| ------:|------:|------:|------:|
| NEU           | preocupaciones | licey | distrito | confirman | 10nov |
| POS           | unirme | commerce | encanto | recomiendo | encanta |
| NEG           | derrumba | sobrevalorado | horrible | harta | cojones |

son las palabras obtenidas considerando todos los tweets, con un minimo de que cada palabra aparezca al menos 20 veces.

#### LDA

Junto con las palabras que nos dan una nocion de cada sentimiento, tambien aplicamos una version de [LDA](https://github.com/bmabey/pyLDAvis) (la cual es mas interactiva) para poder identificar topicos y temas dentro de los tweets. El objetivo de esto, es poder ir mas alla de la clasficiacion de sentimiento habitual, y encontrar sobre que tema se trata cada tweet.


![LDAvis](https://imgur.com/bN5Hgnu.png)

Si combinamos la informacion que extraemos usando PMI y LDA de la forma descrita, tenemos palabras que representan sentimientos y palabras que son mas significativas para cada conjunto de datos (cada Cluster o todo el Dataset).

### Predicciones

## Resultados

### Trabajo futuro

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)

## Alumno
Garagiola, Nazareno