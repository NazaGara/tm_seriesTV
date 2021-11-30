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

El objetivo es el de poder hacer un analisis de sentimiento a tweets que hablen sobre elgun tema en particular, e identificar diferentes subclases de POSITIVO - NEGATIVO - NEUTRAL, que se aproximen a la Causa Latente de la posicion del tweet en particular.

### Caso de Estudio

Tome como caso de estudio tweets relacionados con la serie El Juego del Calamar, ya que al momento de comenzar el proyecto, la serie era muy discutida en las redes sociales, por lo que podia juntar un buen volumen de tweets rapidamente para poder comenzar a analizarlo.

### Pipeline de Trabajo

Hay dos aproximaciones para poder trabajar cada tweet:
- tweets --▶ CountVectorizer --▶ KMeans (o LDA) --▶ PMI --▶ KNN (predictor + patrones)
- tweets --▶      fasttext            --▶ LDA --▶ PMI --▶ KNN (predictor + patrones)


### Primeras Aproximaciones

### Version Final

## Resultados


## Licencia
[MIT](https://choosealicense.com/licenses/mit/)

## Alumno
- Garagiola, Nazareno