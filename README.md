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
[Link para descargar el embedding](https://drive.google.com/file/d/1h_ncLs_ZmdE1K0_AgghzCxqzfH1GjtP1/view?usp=sharing)

### Pre-procesamiento

Una vez que ya tenia todos los tweets, el preprocesamiento de los tweets consistio de:

- Eliminar stopwords y URLs
- Eliminar signos de puntuacion y palabras que comienzan con '@'
- Descartar palabras que tengan una frecuencia menor a 80
- Aplicar reduccion de dimensionalidad mediante la varianza de los datos
- Identificar sentimiento de cada tweet usando la libreria: [PySentimiento](https://github.com/pysentimiento/pysentimiento)

Con esta limpieza de los datos, ahora si ya podemos vectorizar y obtener una matriz de datos con la cual trabajar. Notar que en la vectorizacion de los datos y el clustering no se usan los sentimientos de cada tweet.
Por lo que al final de la etapa de clustering, tenemos 20 clusters de tweets, los cuales se agruparon por su semejanza, no por su sentimiento, entonces en cada cluster podemos tener tweets con diferentes sentimientos, lo cual usamos para la parte de extraccion y entrenamiento del modelo.

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

    if topic_values == [0 for _ in range(len(topics_list))]:
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

Algo para notar, es que para poder entrenar los clasificadores, tuve que seleccionar a mano 3 tweets, uno de cada una de las clases de sentimiento. Esto para asegurarme que se realize el entrenamiento de cada clasificador, que es necesario que tengan diferentes clases para hacer el entrenamiento.

#### Metricas

En la notebook podemos ver que luego de crear y entrenar cada modelo, tambien tenemos para poder revisar algunas metricas de cada uno, por ejemplo:
`{'NEG': {'precision': 0.5517241379310345, 'recall': 0.3333333333333333, 'f1-score': 0.4155844155844156, 'support': 48}, 'NEU': {'precision': 0.9909881914232442, 'recall': 0.99423226812159, 'f1-score': 0.9926075791767178, 'support': 6415}, 'POS': {'precision': 0.40476190476190477, 'recall': 0.38636363636363635, 'f1-score': 0.3953488372093023, 'support': 44}, 'accuracy': 0.9852466574458276, 'macro avg': {'precision': 0.6491580780387278, 'recall': 0.5713097459395199, 'f1-score': 0.6011802773234786, 'support': 6507}, 'weighted avg': {'precision': 0.9837838528369948, 'recall': 0.9852466574458276, 'f1-score': 0.9843124360233451, 'support': 6507}}`

Donde podemos ver que tenemos una [precision](https://en.wikipedia.org/wiki/Precision_and_recall#Precision) general del 64.5% con un [recall](https://en.wikipedia.org/wiki/Precision_and_recall#Recall) (exhaustividad o sensibilidad) menor al 60% en total, solo para la clase NEU siendo esta del 99%, lo cual indica que en su mayoria, el modelo predice el valor neutral y coincide en su mayoria de las veces.


En otro caso tenemos:
`Df 2. Report: {'NEG': {'precision': 0.9, 'recall': 0.8181818181818182, 'f1-score': 0.8571428571428572, 'support': 11}, 'NEU': {'precision': 0.9736070381231672, 'recall': 0.9458689458689459, 'f1-score': 0.9595375722543353, 'support': 351}, 'POS': {'precision': 0.3333333333333333, 'recall': 0.5625, 'f1-score': 0.4186046511627907, 'support': 16}, 'accuracy': 0.9259259259259259, 'macro avg': {'precision': 0.7356467904855002, 'recall': 0.7755169213502547, 'f1-score': 0.7450950268533277, 'support': 378}, 'weighted avg': {'precision': 0.9443635018903835, 'recall': 0.9259259259259259, 'f1-score': 0.9336612002868989, 'support': 378}}`

Tenemos una precision promedio del 73% y valores de recall del 81% para clase NEG, 94% para NEU y 56% para POS. Lo cual nos da a entender de que los clasificadores de los clusters estan mejor distribuidos en comparacion con el clasificador general, y que pueden predecir correctamente y no solo un valor por defecto.


Para poder comparar entre los resultados, se puede ver que si tomamos todos los clasificadores que vienen dados por los vectores obtenidos por el Embedding, estos tienen mayor precision. Es decir, tenemos que:
* __macro avg precision gral__: 0.5735923326204706
* __macro avg recall gral__: 0.5168061982717155
* __macro avg precision por cluster__: 0.6969713581095525
* __macro avg recall por cluster__: 0.6861866236867549

## Resultados

Comienzo aclarando que para obtener los resultados finales, solo pude realizarlo usando los vectores por el metodo de los embeddings, esto por dos razones: La primera por una cuestion de tiempo, y la segunda ya que CountVectorizer sirve para poder traducir documentos a vectores, que tienen un tamaño definido por el vocabulario usado, si agrego un nuevo tweet, este puede incrementar el vocabulario por lo que habria que hacer todo de nuevo a partir del clustering.

Se adquirieron un nuevo conjunto de aproximadamente 1000 tweets para poder evaluar el modelo. Ademas, para identificar si un nuevo tweet coincide en alguno de los topicos, se removieron las palabras "juego" y "calamar" ya que estos siempre van a coincidir y opacan al resto.


Para poder tener una medida cuantitativa de la correctitud del modelo y clasificadores entrenados, lo que se hace es para cada uno de los tweets de evaluacion se los pasa por el metodo de prediccion, es decir, primero se limpia el tweet, se toma el valor del vector que lo represente, se busca si el tweet puede acomodarse a alguno de los clusters usando la lista de topicos que identificamos mediante LDA y finalmente, se usa el predictor de dicho cluster para predecir el sentmiento y el predictor general de todo el conjunto inicial de datos. Ademas, de analyzar con Pysentimiento el tweet para luego tener una comparacion con nuestra meta inicial.
En el caso de que el tweet nuevo no coincida con ninguna de las listas de topicos, se usa el predictor general de todo el dataset.
```py
        #en la funcion predict
        processed_tw = convert_listwords(list_words).strip()
        clf_cluster = preds[cluster][0]
        topics.append(topic)
        cluster_pred.append(clf_cluster.predict([tw_vector]))
        dataset_pred.append(clf_dataset.predict([tw_vector]))
        pysent.append(sentiment.output)
```

Luego de procesar y evaluar todos los nuevos tweets, registro cada vez que coincida el valor predecido con el valor que el analizador de Pysentimiento nos da, para luego poder tener una medida de precision promedio segun si uso los clasificadores de cada cluster o el clasificador general.
```py
c_pred, d_pred, tpcs, pysent = predict(eval_tweets, wv_predictors)
score_general, score_clusters, results = 0, 0, []
for i in range(len(eval_tweets)):
    score_general += (d_pred[i][0] == pysent[i])
    score_clusters += (c_pred[i][0] == pysent[i])
```

Obteniendo los resultados:
- __Precision basado en clasificadores separados por Topicos__: 0.4949596774193548 
- __Precision utilizando el clasificador de todo el corpus__: 0.5524193548387096

Por lo que podemos ver una mejora de aproximadente el 6% del clasificador general con respecto a cada uno de los clasificadores de los clusters. 
Los resultados son en inesperados, pues imaginaba que los clasificadores de cada cluster iban a ser mas correctos que el clasificiador general, ya que habiamos visto que tenian una Precision y una Recall mayor en comparacion al clasificaor general. 

Creo, hay dos razones por las cuales lo que estabamos esperando no funciona adecuadamente:
- La mayoria de los nuevos tweets que hablan sobre el Juego del Calamar son neutrales ya que se deben a referencias a la serie mas que opinar sobre ella, y ya que el clasificador general en su mayoria predice NEU esta coincide con los valores dados por Pysentimiento.
- La forma de asignar los clusters a partir de los topicos puede ser refinada o hace falta seguir refinando la extraccion en la etapa donde se aplica LDA.


Es importante ver que la comparacion final se hace contra un valor que nos da el analizador usado y no contra un label que le asigno un ser humano que fue revisando los tweets, por lo que esta comparacion final puede tener sus imprecisiones dadas por el modelo usado, tanto por las imperfecciones que se encuentran en el modelo creado.


A continuacion, un par de ejemplos a la lista de resultados:
1. "twitter esta en el juego del calamar - SENT: ('NEU', 'NEU', 'NEU') - TOPICS: Using dataset configuration, we dont have the topics related"
1. "@LIDOMRD Que empiece el Juego del Calamar. Toros, eliminados  - SENT: ('NEU', 'NEU', 'NEG') - TOPICS: Using dataset configuration, we dont have the topics related"
1. "Algo parecido a lo que me paso con el juego del calamar, aunque la serie en si me gusto mucho - SENT: ('NEU', 'NEU', 'NEU') - TOPICS: ['serie', 'netflix', 'temporada', 'creador', 'confirma']"
1. "¿Veran la segunda parte del juego del Calamar, o en una sola temporada se quemaron todos los cartuchos? - SENT: ('NEU', 'NEU', 'NEG') - TOPICS: ['muneca', 'temporada', 'corea', 'creador', 'sur']"


Se pueden ver casos en los que no aun no se tienen los topicos (1° y 2°). Un caso en el que tanto el modelo como los clusters coinciden o en el que ambos fallan en su prediccion.

### Trabajo futuro

Como funcionalidades que me hubiese gustado abarcar pero por tiempo y fines del trabajo no pude concretar son:

- Mejorar la forma de identificar el cluster a partir de los topicos:
    
    Explorar cual era la mejor forma a identificar el cluster para ver que clasificador utilizar.

- Identificar Tweets con mayor precision:
    
    Poder dedicar mas tiempo a lo que respecta a information retrieval.

- Generalizar el modelo para poder buscar sobre diferentes temas de opiniones o tendencias en la red:

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