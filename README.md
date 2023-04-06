# Inmersion Datos

## Proyecto creado por Ezequiel Rodriguez en base a programa de Alura "Inmersion en Datos"

### Proyecto destinado a trabajar mediante el uso de una base de datos sobre inmuebles a la venta en la ciudad de Bogotá de mas de 9 mil elementos, sumado a datos estadisticos extraidos del DANE, a traves del lenguaje Python. El principal objetivo es desarrollar un modelo de Machine Learning para predecir valores de inmuebles en base a ciertas caracteristicas del mismo, como el barrio al que pertenece, la cantidad de habitaciones y baños y otras variables.

### Conocimientos aplicados:
* Importar datos y exportar dataframes
* Limpiar y tratar datos faltantes
* Tarbajar con selecciones y frecuencias de datos
* Crear diferentes agrupamientos para aplicar estadistica descriptiva
* Analisis sobre graficos generados mediante librearias
* Importar datos desde encuestas gubernamentales para aplicar a base de datos ya existente
* Excluir outliers para poder modelar de manera correcta
* Analizar grado de correlacion entre variables
* Modelar Machine Learning mediante regresion lineal

### Uso de Python Pandas, Matplotlib, Seaborn, SciKit Learn y Jupyter

## Resultados obtenidos

### Luego del tratamiento y analisis estadistico sobre los datos proporcionados, se tomaron dos caminos distintos teniendo en cuenta la exclusion de outliers en base al precio en millones de pesos colombianos de los inmuebles. En el desarrollo del Machine Learning para predecir precios de inmuebles en millones de pesos (Precio_Millon) se tuvieron en cuenta las siguentes variables: UPZ al cual pertenecian (COD_UPZ_GRUPO), cantidad de habitaciones (Habitaciones), cantidad de baños (Banos), si pertenecia a un conjunto cerrado (CONJUNTO_CERRADO), el salario anual en millones del propietario (SALARIO_ANUAL_MI) y si el inmuebles poseia escritura (TIENE_ESCRITURA).

### En el primer caso se optó por excluir de aquellos inmuebles que escapaban a los limites planteados por el grafico de caja de la variable ya previamente mencionada a partir de los 5000 millones, obteniendo un modelo predictivo con un error absoluto medio de 241.9 millones y un coeficiente de determinacion de 0.42, lo cual puede considerarse que el ajuste del modelo se encuentra en un rango aceptable cercano a lo bueno.
Mapa de calor sobre correlaciones entre variables en el primer caso
![graficoCorr0](https://user-images.githubusercontent.com/111917955/230476955-c3732dce-a22d-4dee-937f-d9435e57e9ea.png)


### En el segundo caso, se optó por excluir aquellos outliers que superasen los 1500 millones de pesos colombianos, obteniendo un modelo predictivo con un error absoluto medio de 144.4 millones y un coeficiente de determinacion de 0.534, lo cual lleva a poder afirmar que el uso de menos datos, debido a la exclusion de una mayor cantidad de outliers, conduce a una mayor correlacion entre las variables, dando como resultado un modelo mas ajustado que en el primer caso.
Mapa de calor sobre correlaciones entre variables en el segundo caso
![graficoCorrelacion](https://user-images.githubusercontent.com/111917955/230477044-a013c6b2-c3e3-41b5-99c3-442c7d86e66c.png)

