# Más allá del sentimiento binario: descubriendo posiciones sobre un tema

Repositorio correspondiente al proyecto final de la materia Text-Mining del año 2021 de la carrera de Licenciatura en Ciencias de la Computación en FaMAF - UNC.


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Tabla de contenidos</h2></summary>
  <ul>
    <li><a href="#instalacion">Instalacion</a></li>
    <li><a href="#uso">Uso</a></li>
    <li><a href="#objetivo">Objetivo</a></li>
    <li><a href="#metodologia">Metodologia</a></li>
    <li><a href="#resultados">Resultados</a></li>
    <li><a href="#licencia">Licencia</a></li>
    <li><a href="#contacto">Contacto</a></li>
  </ul>
</details>


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

## Metodologia

El acercamiento que tuve para desarrollar el proyecto fue el siguiente:

Pre-Processing -> Sentiment Analysis -> Vectorization -> Clustering -> Extraction -> Model Training -> Prediction

Hasta la etapa de Clustering, el modo de trabajo fue muy similar al del practico de Clustering, con la gran diferencia de que esta vez, agrupamos documentos (tweets) en vez de palabras, por lo que pude utilizar [CountVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html). Al mismo tiempo que nosotros trabajamos con cada tweet, tambien procese los datos usando un Word Embedding de FastText de 100 dimensiones entrenado con informacion de Twitter, para luego poder comparar los resultados entre ambas versiones.

### Pre-procesamiento

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

y por ejempo, si fijamos el cluster 2 obtenidos usando los embeddings (sin perdida de generalidad), obtenemos las siguientes palabras, con un minimo de 5 veces:

| Sentimiento   | palabra 1  | palabra 2  | palabra 3 | palabra 4 | palabra  5|
| ------------- |:-------------:| ------:|------:|------:|------:|
| NEU           | hwang | dong | hyuk | revelo | segun |
| POS           | ganador | basado | exitosa | historia | gente |
| NEG           | cae | dolar | millonaria | creadores | muertos |

#### LDA

Junto con las palabras que nos dan una nocion de cada sentimiento, tambien aplicamos una version de [LDA](https://github.com/bmabey/pyLDAvis) (la cual es mas interactiva) para poder identificar topicos y temas dentro de los tweets. El objetivo de esto, es poder ir mas alla de la clasficiacion de sentimiento habitual, y encontrar sobre que tema se trata cada tweet.

![LDAvis](https://imgur.com/bN5Hgnu.png)

Si combinamos la informacion que extraemos usando PMI y LDA de la forma descrita, tenemos palabras que representan sentimientos y palabras que son mas significativas para cada conjunto de datos (cada Cluster o todo el Dataset).

Para el caso del dataset, por ejemplo, asique podemos ver las palabras que denoten topicos para los casos que vimos las palabras de sentimiento.

| Caso      | palabra 1  | palabra 2  | palabra 3 | palabra 4 | palabra  5|
| --------- |:-------------:| ------:|------:|------:|------:|
| Topicos 0 | disfraces | serie | visto | halloween | mas |
| Topicos 1 | casa | criptomoneda | papel | millones | estafa |
| Topicos 2 | gente | vi | mas | viendo | capitulo |
| Topicos 3 | mas | bien | series | gusto | serie |
| Topicos 4 | ninos | serie | anos | disfrazados | jugando |
| Topicos 5 | serie | netflix | temporada | creador | mas |
| Topicos 6 | disfraz | halloween | muneca | fiesta | personas |

Para el caso del 2° cluster, tenemos:

| Caso      | palabra 1  | palabra 2  | palabra 3 | palabra 4 | palabra  5|
| --------- |:-------------:| ------:|------:|------:|------:|
| Topicos 0 | video | final |serie | creador |vi |
| Topicos 1 | mas | serie |fiesta | anos |netflix |
| Topicos 2 | criptomoneda | inspirada |estafa | criptodivisa |dias |
| Topicos 3 | casa | papel |disfraz | halloween |disfraces |
| Topicos 4 | serie | netflix |exito | creador |pese |
| Topicos 5 | luz | gente |visto | historia |verde |
| Topicos 6 | muneca | temporada |corea | creador |sur |

Si desamos ver toda la informacion que tenemos sobre cada conjunto de datos, podemos ejecutar la celda que contiene:
```py
for k in wv_pmi_lda:
    print(f"-----{k}-----")
    display(wv_pmi_lda[k][0],wv_pmi_lda[k][1],wv_pmi_lda[k][2],wv_pmi_lda[k][3])
```

### Predicciones y Modelos

Para poder predecir el sentimiento de nuevos tweets, utilizo la implementacion de la [Regresion Logistica](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) y tener clasificadores para cada uno de los clusters y para el todo el corpus. En cada clasificador el input es un vector (obtenido a partir del tweet nuevo) con ciertas dimensiones y me devuelve el label correspondiente al sentimiento relacionado.

Lo bueno de tener 1 clasificador general y uno para cada cluster es que puedo predecir dos valores de sentimiento, uno obtenido por el clasificador de todo el dataset y otro segun los topicos del que trate el nuevo tweet. Entonces, con la lista de palabras obtenidas usando LDA puedo identificar sobre que topico habla un nuevo tweet, seleccionar el cluster de dicha lista, y predecir usando el clasificador de ese cluster.

```py
# en la funcion predict
        cluster, topic = get_cluster(processed_tw)
#...
topics_list = []
for k in wv_pmi_lda: 
    if k!='dataset': topics_list.append(wv_pmi_lda[k][0])
    
def get_cluster(tweet):
    topic_values = []

    for t in topics_list:
        topic_values.append(int(identify_topic(tweet, t)))

    if topic_values == [0 for _ in range(len(topics_list))]: #que no ocurre nunca en la lista de topicos
        cluster, topics = "dataset", "Using dataset configuration, we dont have the topics related"
    else:
        cluster = topic_values.index(max(topic_values))
        topics = topics_list[cluster][max(topic_values)]

    return cluster, topics
```

Una de las cosas que hay que destacar, es que para entrenar el modelo  con el objetivo de predecir sentimiento hay dos formas de tomar las labels de los vectores de entrenamiento, una es usando directamente el valor obtenido al comienzo cuando analizamos con PySentimiento o la otra forma, es utilizar las palabras obtenidas con LDA para cada conjunto de datos. Por lo que para poder realizar esta segunda opcion, hubo que implementar una nueva funcion para identificar sentimiento de una lista de tweets:

```py
def identify_sentiment(tweet_list, sentiments_list):
    y = np.empty(0)
    labels = {0: 'NEU', 1: 'POS', 2: 'NEG'}
    for tw in tweet_list:
        counts = [0 for _ in range(len(sentiments_list))]
        for i in range(len(sentiments_list)):
            c = 0
            for w in sentiments_list[i]:
                c += count_subwords(tw, w)
            counts[i] = c
        y = np.append(y, labels[counts.index(max(counts))])
    return y
```

Y luego, en la funcion para crear y evaluar cada modelo llamamos a esta funcion para etiquetar cada tweet que estaba en cada conjunto de datos, con el fin de poder entrenar el modelo con estas etiquetas.


#### Metricas

En la notebook podemos ver que luego de crear y entrenar cada modelo, tambien tenemos para poder revisar algunas metricas de cada uno, por ejemplo:
`Df dataset. Report: {'NEG': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 48}, 'NEU': {'precision': 0.9858613800522514, 'recall': 1.0, 'f1-score': 0.9928803590775422, 'support': 6415}, 'POS': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 44}, 'accuracy': 0.9858613800522514, 'macro avg': {'precision': 0.3286204600174171, 'recall': 0.3333333333333333, 'f1-score': 0.3309601196925141, 'support': 6507}, 'weighted avg': {'precision': 0.9719226606785298, 'recall': 0.9858613800522514, 'f1-score': 0.9788424010269607, 'support': 6507}} `

Donde podemos ver que tenemos una [precision](https://en.wikipedia.org/wiki/Precision_and_recall#Precision) general del 98.9% pero un [recall](https://en.wikipedia.org/wiki/Precision_and_recall#Recall) (exhaustividad o sensibilidad) nulas para las clases POS y NEG, lo cual quiere decir que el modelo practicamente predice siempre NEU, lo cual ocurre por el gran volumen de tweets neutrales en comparacion con las demas clases.


En otro caso tenemos:
`Df 2. Report: {'NEG': {'precision': 0.9, 'recall': 0.8181818181818182, 'f1-score': 0.8571428571428572, 'support': 11}, 'NEU': {'precision': 0.9736070381231672, 'recall': 0.9458689458689459, 'f1-score': 0.9595375722543353, 'support': 351}, 'POS': {'precision': 0.3333333333333333, 'recall': 0.5625, 'f1-score': 0.4186046511627907, 'support': 16}, 'accuracy': 0.9259259259259259, 'macro avg': {'precision': 0.7356467904855002, 'recall': 0.7755169213502547, 'f1-score': 0.7450950268533277, 'support': 378}, 'weighted avg': {'precision': 0.9443635018903835, 'recall': 0.9259259259259259, 'f1-score': 0.9336612002868989, 'support': 378}}`

Tenemos una precision promedio del 73% y valores de recall del 81% para clase NEG, 94% para NEU y 56% para POS. Lo cual nos da a entender de que los clasificadores de los clusters estan mejor distribuidos en comparacion con el clasificador general, y que pueden predecir correcatamente y no solo un valor por defecto.

## Resultados

TO DO:

- Destacar que es mejor cluster vs dataset vs pysentimiento
- Concluir, mostrar ejemplos y mostrar cuantitativamente cual anda mejor y con cuanta precision

### Trabajo futuro

Como funcionalidades que me hubiese gustado abarcar pero por tiempo y fines del trabajo no pude concretar son:

-   Identificar Tweets con mayor precision.
    
    Poder dedicar mas tiempo a lo que respecta a information retrieval.

- Generalizar el modelo para poder buscar sobre diferentes temas de opiniones o tendencias en la red.

    Hacer crecer para que mas rapidamente se detecten los tweets y se ejecute el modelo.

- Probar con entrenar con tweets genericos: 
    
    Usar tweets objetivamente neutrales, positivos o negativos y ver si funciona para diferentes temas, sin usar terminos especificos de cada tendencia.

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)

## Contacto
* Garagiola, Nazareno
* [LinkedIn](https://www.linkedin.com/in/nazareno-garagiola/)
* [Mail](nazagara1277@gmail.com)
* [Twitter](https://twitter.com/nazagara99)