# -*- coding: utf-8 -*-
"""Inmersion_Datos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zJzGPvptLGYfwEJ4mgyKqaoPkThEo2mI

#Conexion a Drive
"""

from google.colab import drive

drive.mount('/content/drive')

"""#Importacion librerias"""

import pandas as pd

inmuebles = pd.read_csv('/content/drive/MyDrive/Inmersion_datos/inmuebles_bogota.csv')

inmuebles.head(15)

inmuebles.shape #(filas, columnas)

inmuebles.columns #Nombres columnas

"""## Tratamiento sobre nombres columnas"""

dic_columnas = {
    'Baños': 'Banos',
    'Área': 'Area'
}

inmuebles = inmuebles.rename(columns = dic_columnas)
inmuebles.sample(10)

"""##Tipo de dato variables"""

inmuebles.info()

"""Significado Variables:


*   UPZ: Unidades de Planeacion Zonal, conformadas por uno o mas barrios
*   Area: en metros cuadrados
*   Valor: en pesos colombianos

##Cantidad viviendas por barrio
"""

inmuebles_barrio = inmuebles.Barrio.value_counts()
inmuebles_barrio

"""###Top 10 de barrios en grafico

Muestra de los barrios con mas inmuebles a la venta
"""

inmuebles_barrio.head(10).plot.bar();

"""##Cantidad viviendas por UPZ"""

inmuebles_upz = inmuebles.UPZ.value_counts()
inmuebles_upz

"""##Top 10 de UPZ en grafico"""

inmuebles_upz.head(10).plot.bar();

"""##Promedio de area de todos los barrios"""

barrios = list(inmuebles.Barrio.unique())
barrios

grupo_barrio = inmuebles.groupby(['Barrio'])

prom_barrio = grupo_barrio[['Area']].mean().round(2)
prom_barrio.sort_values(by = ['Area'], inplace=True, ascending=False)
prom_barrio

"""###Top 10 promedio area por barrio"""

prom_barrio.head(10).plot.bar();

"""#Tratamiento de datos de la columna 'Valor'

##Separacion simbolo $ y valor numerico
"""

valor = inmuebles.Valor.str.split(expand = True)
valor

inmuebles['Moneda'] = valor[0]
inmuebles['Precio'] = valor[1]
inmuebles.sample(5)

"""###Precio sigue siendo un objeto, no un valor numerico"""

inmuebles.info()

"""###Se debe sustituir los puntos de los separadores de miles"""

inmuebles['Precio'] = inmuebles['Precio'].str.replace('.','', regex = True)

inmuebles.info()

inmuebles['Precio_Millon'] = inmuebles.Precio.astype('float')/1000000

inmuebles.info()

"""#Datos estadisticos de variables numericas"""

pd.set_option('display.precision',2)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

inmuebles.describe()

"""Se puede ver que el maximo en 'Habitaciones' es 110 y el minimo en 'Area' es 2, por lo que probablemente se trate de un error de tipeo, pero deben tratarse para que no afecte al modelo final

#Primeros graficos
"""

import matplotlib.pyplot as plt

import seaborn as sns

"""###Hsitograma con curva de densidad de 'Precio_Millon'"""

plt.figure(figsize = (10,6))
hist1 = sns.histplot(data = inmuebles, x = 'Precio_Millon', kde = True);
hist1.set_title('Distribucion de valores de los inmuebles en Bogota (millones $)')
plt.xlim((50,1000)) #Limites superior e inferior, en base a cuartiles
plt.show()
plt.savefig('/content/drive/MyDrive/Inmersion_datos/valor_inmuebles.png',format = 'png')

"""###Se agrega al analisis la variable 'Tipo'"""

plt.figure(figsize = (10,6))
hist1 = sns.histplot(data = inmuebles, x = 'Precio_Millon', kde = True, hue = 'Tipo');
hist1.set_title('Distribucion de valores de los inmuebles en Bogota (millones $)')
plt.xlim((50,1000)) #Limites superior e inferior, en base a cuartiles
plt.ylim((0,500))
plt.show()
plt.savefig('/content/drive/MyDrive/Inmersion_datos/valor_inmuebles_con_tipo.png',format = 'png')

"""###Estudio histograma de valores inmuebles por tipo

Locales
"""

plt.figure(figsize = (10,6))
seleccion_tipo = inmuebles['Tipo'] == 'Local'
tipo = inmuebles[seleccion_tipo]
hist1 = sns.histplot(data = tipo, x = 'Precio_Millon', kde = True, color = 'red');
hist1.set_title('Distribucion de valores de los inmuebles del tipo Local en Bogota (millones $)')
plt.xlim((50,4000)) #Limites superior e inferior, en base a cuartiles
plt.ylim((0,20))
plt.show()
plt.savefig('/content/drive/MyDrive/Inmersion_datos/valor_inmuebles_con_tipo_local.png',format = 'png')

"""Casas"""

plt.figure(figsize = (10,6))
seleccion_tipo = inmuebles['Tipo'] == 'Casa'
tipo = inmuebles[seleccion_tipo]
hist1 = sns.histplot(data = tipo, x = 'Precio_Millon', kde = True, color = 'orange');
hist1.set_title('Distribucion de valores de los inmuebles del tipo Local en Bogota (millones $)')
plt.xlim((50,4000)) #Limites superior e inferior, en base a cuartiles
plt.ylim((0,250))
plt.show()
plt.savefig('/content/drive/MyDrive/Inmersion_datos/valor_inmuebles_con_tipo_casa.png',format = 'png')

"""###Precio del m2 por barrio"""

inmuebles['Valor_m2_Millon'] = inmuebles['Precio_Millon']/inmuebles['Area']
inmuebles.head(10)

"""Aca se muestra el promedio del valor por metro cuadrado de cada barrio por millon, pero es en base al valor por m2 de cada registro, y no segun la suma de todos los valores de precio dividido la suma de todos los valores de area de los registros pertenecientes al mismo barrio"""

inmuebles.groupby('Barrio').mean()

datos_barrio = inmuebles.groupby('Barrio').sum()

"""Muesta la suma de los datos pertenecientes a cada barrio, a partir de aca se calcula el promedio"""

datos_barrio

datos_barrio['Valor_m2_Barrio'] = datos_barrio['Precio_Millon']/datos_barrio['Area']

"""Se puede ver el impacto comparando con los resultados anteriores, ya que los resultados son distintos. En este caso, se toma como correcto el segundo calculo realizado"""

datos_barrio

m2_barrio = dict(datos_barrio['Valor_m2_Barrio'])

"""###Se aplica los resultados obtenidos del valor de los metros cuadrados por millon a 'inmuebles', creando una columna 'Valor_m2_Barrio' a partir de los valores obtenidos en la columna 'Valor_m2_Barrio' en 'datos_barrio'"""

inmuebles['Valor_m2_Barrio'] = inmuebles['Barrio']
inmuebles['Valor_m2_Barrio'] = inmuebles['Valor_m2_Barrio'].map(m2_barrio)
inmuebles.head(10)

"""Diez barrios con mayor cantidad de inmuebles a la venta"""

top_barrios = inmuebles['Barrio'].value_counts()[:10].index

datos_barrio.reset_index(inplace=True) #Ahora barrios sera una columna mas y no el indice
datos_barrio

"""###Consulta sobre datos_barrio de top 10 de barrios obtenido anteriormente"""

datos_barrio.query('Barrio in @top_barrios')

"""###Grafico de barras a partir de los datos de los barrios pertenecientes al top 10"""

plt.figure(figsize=(10,8))
ax = sns.barplot(data = datos_barrio.query('Barrio in @top_barrios'), x = 'Barrio', y = 'Valor_m2_Barrio')
plt.title('Grafico de barras sobre valor del m2 en millones de inmuebles de los barrios del top 10 de inmuebles a la venta')
ax.tick_params(axis = 'x', rotation = 45)

"""###Grafico box-plot sobre valor m2 por millon a partir de los datos de los barrios pertenecientes al top 10"""

plt.figure(figsize=(10,8))
ax = sns.boxplot(data = inmuebles.query('Barrio in @top_barrios'), x = 'Barrio', y = 'Valor_m2_Millon')
ax.tick_params(axis = 'x', rotation = 45)
plt.ylim((0,20))
plt.title('Grafico de Caja del valor del m2 por millon de los inmuebles de los barrios del top 10 de inmuebles a la venta')
plt.show()

"""###Grafico box-plot sobre Area a partir de los datos de los barrios pertenecientes al top 10"""

plt.figure(figsize=(10,8))
ax = sns.boxplot(data = inmuebles.query('Barrio in @top_barrios'), x = 'Barrio', y = 'Area')
ax.tick_params(axis = 'x', rotation = 45)
plt.ylim((0,500))
plt.title('Grafico de Caja del area de los inmuebles de los barrios del top 10 de inmuebles a la venta')
plt.show()

"""Grafico box-plot sobre Precio por millon a partir de los datos de los barrios pertenecientes al top 10"""

plt.figure(figsize=(10,8))
ax = sns.boxplot(data = inmuebles.query('Barrio in @top_barrios'), x = 'Barrio', y = 'Precio_Millon')
ax.tick_params(axis = 'x', rotation = 45)
plt.ylim((0,2000))
plt.title('Grafico de Caja del precio por millon de los inmuebles de los barrios del top 10 de inmuebles a la venta')
plt.show()

"""Se traen datos estadísticos de la ciudad de Bogotá, directamente del DANE y se verá como estos datos nos ayudan en inclusión de nuevas variables para el cálculo del precio de los inmuebles en la ciudad de Bogotá.

Encuesta Multiproposito de Bogotá para obtener información socio-económica y de entorno urbano de los habitantes de Bogotá para la formulación, seguimiento y evaluación de las políticas distritales.

https://microdatos.dane.gov.co/index.php/catalog/743
"""

datos_raw = pd.read_csv('/content/drive/MyDrive/Inmersion_datos/Identificación (Capítulo A).csv', encoding = 'latin-1', sep = ';')

"""El departamento 11001 corresponde a Bogotá, ciudad sobre la cual se esta haciendo el analisis, por lo que se deberia filtrar la informacion para obtener solo los datos que corresponden al analisis"""

datos_raw.head(10)

datos_raw.shape

"""Se eliminan 20 mil registros aproximadamente, que correspondian al area rural de Bogotá"""

datos_raw = datos_raw.loc[datos_raw.MPIO == 11001]
datos_raw.shape

"""###Improtacion de otras variables que seran usadas en el analisis extraidas del DANE"""

datos_b = pd.read_csv('/content/drive/MyDrive/Inmersion_datos/Datos de la vivenda y su entorno (Capítulo B).csv',sep=';',encoding='latin-1')
datos_c = pd.read_csv('/content/drive/MyDrive/Inmersion_datos/Condiciones habitacionales del hogar (Capítulo C).csv',sep=';',encoding='latin-1')
datos_e = pd.read_csv('/content/drive/MyDrive/Inmersion_datos/Composición del hogar y demografía (Capítulo E).csv',sep=';',encoding='latin-1')
datos_h = pd.read_csv('/content/drive/MyDrive/Inmersion_datos/Educación (Capitulo H).csv',sep=';',encoding='latin-1')
datos_l = pd.read_csv('/content/drive/MyDrive/Inmersion_datos/Percepción sobre las condiciones de vida y el desempeño institucional (Capítulo L).csv',sep=';',encoding='latin-1')
datos_k = pd.read_csv('/content/drive/MyDrive/Inmersion_datos/Fuerza de trabajo (Capítulo K).csv',sep=';',encoding='latin-1')

"""Se importaron 6 bases de datos, pero para el analisis por ahora solo seran necesarias las correspondientes a 'Datos de la vivienda y su entorno', 'Condiciones habitacionales del hogar' y 'Composicion del hogar y demografia'"""

datos_dane = pd.merge(datos_raw,datos_b,on='DIRECTORIO', how='left')
datos_dane.shape

datos_dane = pd.merge(datos_dane,datos_c,on='DIRECTORIO', how='left')
datos_dane.shape

datos_dane = pd.merge(datos_dane,datos_e,on='DIRECTORIO', how='left')   
datos_dane.shape

datos_dane.info()

"""##Se continua trabajando con la base de datos actualizada y ya tratada para focalizar sobre el analisis de los datos y no tanto sobre su tratamiento"""

datos_dane = pd.read_csv('/content/drive/MyDrive/Inmersion_datos/datos_dane.csv')
datos_dane.head(10)

datos_dane.shape

"""Los codigos de las columnas corresponde a nomenclatura disponible en la documentacion de DANE"""

datos_dane.info()

"""Se procede a cambiar los codigos mencionados por su definicion formal"""

dic_dane = {
       'NVCBP4':'CONJUNTO_CERRADO',
       'NVCBP14A':'FABRICAS_CERCA', 'NVCBP14D':'TERMINALES_BUS', 'NVCBP14E':'BARES_DISCO', 
       'NVCBP14G':'OSCURO_PELIGROSO', 'NVCBP15A':'RUIDO', 'NVCBP15C':'INSEGURIDAD',
       'NVCBP15F':'BASURA_INADECUADA', 'NVCBP15G':'INVASION','NVCBP16A3':'MOV_ADULTOS_MAYORES', 
       'NVCBP16A4':'MOV_NINOS_BEBES',
       'NPCKP17':'OCUPACION','NPCKP18':'CONTRATO','NPCKP23':'SALARIO_MES', 
       'NPCKP44A':'DONDE_TRABAJA', 'NPCKPN62A':'DECLARACION_RENTA', 
       'NPCKPN62B':'VALOR_DECLARACION', 'NPCKP64A':'PERDIDA_TRABAJO_C19', 
       'NPCKP64E':'PERDIDA_INGRESOS_C19',
       'NHCCP3':'TIENE_ESCRITURA', 'NHCCP6':'ANO_COMPRA', 'NHCCP7':'VALOR_COMPRA', 'NHCCP8_1':'HIPOTECA_CRED_BANCO',
       'NHCCP8_2':'OTRO_CRED_BANCO', 'NHCCP8_3':'CRED_FNA', 'NHCCP8_6':'PRESTAMOS_AMIGOS',
       'NHCCP8_7':'CESANTIAS', 'NHCCP8_8':'AHORROS', 'NHCCP8_9':'SUBSIDIOS',
       'NHCCP9':'CUANTO_PAGARIA_MENSUAL', 'NHCCP11':'PLANES_ADQUIRIR_VIVIENDA', 
       'NHCCP11A':'MOTIVO_COMPRA', 'NHCCP12':'RAZON_NO_ADQ_VIV', 'NHCCP41':'TIENE_CARRO','NHCCP41A':'CUANTOS_CARROS',
       'NHCCP47A':'TIENE_PERROS', 'NHCCP47B':'TIENE_GATOS', 'NHCLP2A':'VICTIMA_ATRACO', 'NHCLP2B':'VICTIMA_HOMICIDIO', 
       'NHCLP2C':'VICTIMA_PERSECUSION',
       'NHCLP2E':'VICTIMA_ACOSO', 'NHCLP4':'COMO_VIVE_ECON', 'NHCLP5':'COMO_NIVEL_VIDA', 
       'NHCLP8AB':'REACCION_OPORTUNA_POLICIA', 'NHCLP8AE':'COMO_TRANSPORTE_URBANO', 'NHCLP10':'SON_INGRESOS_SUFICIENTES',
       'NHCLP11':'SE_CONSIDERA_POBRE', 'NHCLP29_1A':'MED_C19_TRABAJO', 
       'NHCLP29_1C':'MED_C19_CAMBIO_VIVIENDA', 'NHCLP29_1E':'MED_C19_ENDEUDAMIENTO', 
       'NHCLP29_1F':'MED_C19_VENTA_BIENES','NPCHP4':'NIVEL_EDUCATIVO'
       }

datos_dane = datos_dane.rename(columns = dic_dane)
datos_dane.columns

"""###Se seleccionan algunas de las variables mas significativas para trabajar en el analisis de los datos con ellas

En la base de datos utilizada, las respuestas a las preguntas de la encuesta se corresponden con un 1 para las afirmativas y con un 2 para las negativas

Nombre estrato = Nombre UPZ
"""

datos_dane.groupby('NOMBRE_ESTRATO')[['CONJUNTO_CERRADO','INSEGURIDAD','TERMINALES_BUS','BARES_DISCO','RUIDO','OSCURO_PELIGROSO','SALARIO_MES','TIENE_ESCRITURA','PERDIDA_TRABAJO_C19','PERDIDA_INGRESOS_C19','PLANES_ADQUIRIR_VIVIENDA']].mean().head()

"""###Se sustituyen los 2 de las respuestas negativas por 0, para mayor facilidad de trabajo con los datos utilizados en el analisis"""

datos = datos_dane[['NOMBRE_ESTRATO','CONJUNTO_CERRADO','INSEGURIDAD','TERMINALES_BUS','BARES_DISCO','RUIDO','OSCURO_PELIGROSO','SALARIO_MES','TIENE_ESCRITURA','PERDIDA_TRABAJO_C19','PERDIDA_INGRESOS_C19','PLANES_ADQUIRIR_VIVIENDA']].replace(2,0)

datos.head(10)

datos_tratados = datos.groupby('NOMBRE_ESTRATO')[['CONJUNTO_CERRADO','INSEGURIDAD','TERMINALES_BUS','BARES_DISCO','RUIDO','OSCURO_PELIGROSO','SALARIO_MES','TIENE_ESCRITURA','PERDIDA_TRABAJO_C19','PERDIDA_INGRESOS_C19','PLANES_ADQUIRIR_VIVIENDA']].mean()
datos_tratados

pd.merge(inmuebles, datos_tratados, left_on = 'UPZ', right_on = 'NOMBRE_ESTRATO', how = 'left')

"""##Estos datos son los que seran utilizados para desarrollar la Machine Learning (ML)"""

datos_ml = pd.merge(inmuebles, datos_tratados, left_on = 'UPZ', right_on = 'NOMBRE_ESTRATO', how = 'left')
datos_ml.info()

"""Para poder aplicar la regresion lineal se debe contar con valores numericos y no de tipo objeto, por lo que se procede a cambiar los valores de UPZ por sus codigos correspondientes"""

upz = pd.read_csv('/content/drive/MyDrive/Inmersion_datos/cod_upz.csv')
upz.head(10)

datos_ml = pd.merge(datos_ml, upz, left_on = 'UPZ', right_on = 'NOMBRE_ESTRATO', how = 'inner') #inner: interseccion de ambos conjuntos
datos_ml.head(10)

datos_ml.sample(10)

"""Se puede observar que ya no hay ningun NaN dentro de los datos a utilizar en el analisis"""

datos_ml.info()

plt.figure(figsize = (10,8))
sns.boxplot(data = datos_ml, y = 'Precio_Millon');
plt.title('Grafico de Caja del precio por millon de los inmuebles')
plt.show()

"""Se decide quitar los outliers a partir de los 5000 millones y los menores a 60 millones"""

datos_ml.query('Precio_Millon > 5000 | Precio_Millon < 60')

datos_ml = datos_ml.query('Precio_Millon < 5000 & Precio_Millon > 60')
datos_ml

plt.figure(figsize = (10,8))
sns.boxplot(data = datos_ml, y = 'Precio_Millon');
plt.title('Grafico de Caja del precio por millon de los inmuebles')
plt.show()

"""Se calcula el salario anual a partir del salario mensual, y se lleva a millones para trabajar con una menor cantidad de digitos"""

datos_ml['SALARIO_ANUAL_MI'] = datos_ml['SALARIO_MES']*12/1000000
datos_ml['SALARIO_ANUAL_MI']

"""###Scatterplot de precio en millones de los m2 de los inmuebles en funcion del salario anual en millones"""

plt.figure(figsize = (10,8))
sns.scatterplot(data = datos_ml, x = 'SALARIO_ANUAL_MI', y = 'Valor_m2_Millon');
plt.ylim((0,15))
plt.title('Grafico de dispersion del valor por millon del m2 en base al salario anual en millones')
plt.show()

"""Viendo el grafico de dispersion generado en base al analisis realizado, se puede llegar a la conclusion de que el salario anual de las personas no tiene una relacion directa con el precio del metro cuadrado del inmueble en la UPZ

###Grado de correlacion entre variables

* Cercano a 1: correlacion directa
* Cercano a -1: correlacion indirecta (inversa)
* Cercano a 0: no hay correlacion
"""

datos_ml.corr()

"""En base a esta tabla, se puede observar que si exsite una correlacion buena (0.46) entre el valor por metro cuadrado en millones y el salario anual

Se aplica entonces un mapa de calor para poder observar de manera grafica dicha tabla de correlaciones
"""

plt.figure(figsize=(18, 8))
#https://www.tylervigen.com/spurious-correlations
#mascara = np.triu(np.ones_like(datos_ml.corr(), dtype=bool)) mask=mascara,
heatmap = sns.heatmap(datos_ml.corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlacion de las variables', fontdict={'fontsize':18}, pad=16);

"""#Modelado de Machine Learning

###Uso de SciKit Learn para aplicar Machine Learning
"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

"""Variables de entrada: codigo de grupo de UPZ

Variable de respuesta: precio en millones de los inmuebles
"""

X = datos_ml[['COD_UPZ_GRUPO']]
y = datos_ml[['Precio_Millon']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 99)

X_train #Corresponde al 75% de los datos, los cuales se utilizar para entrenar al modelo

X_test #Corresponde al 25% de los datos, los cuales se utilizan para testear el modelo

y_train #Corresponde al 75% de los datos

y_test #Corresponde al 25% de los datos

"""###Instanciamiento de modelo de regresion lineal"""

modelo = LinearRegression()

modelo.fit(X_train, y_train)

y_predict_test = modelo.predict(X_test)

"""###Una vez construido el modelo, se procede a evaluar su performance en base a dos metricas: el error absoluto medio (mae) y r^2 (coeficiente de determinacion)

Cuanto r^2 este mas cercano a 1, mas ajustado está el modelo
"""

from sklearn.metrics import mean_absolute_error, r2_score

baseline_mae = mean_absolute_error(y_test, y_predict_test)
baseline_mae

"""El error absoluto medio nos dice que si, en este caso, introducimos el valor de un inmueble, este va a tener una variacion de 349 millones de pesos, lo caul puede considerarse un error alto"""

baseline_r2 = r2_score(y_test, y_predict_test)
baseline_r2

"""El valor de r^2 es muy cercano a cero, por lo que podemos afirmar que la baseline no se esta desempeñando de beuna forma """

print(baseline_mae, baseline_r2)

"""Estos valores se deben a que solo se tomó un atributo para desarrollar el modelo, y al tener una cantidad grade de datos no se justifica tomar solo uno de los atributos

###Por lo tanto, se procede a tomar 2 variables mas a colocar en X y se realiza nuevamente el analisis
"""

X = datos_ml[['COD_UPZ_GRUPO','Habitaciones','Banos']] 

Y = datos_ml["Precio_Millon"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 99)
modelo_1 = LinearRegression()
modelo_1.fit(X_train, y_train)
y_predict_test = modelo_1.predict(X_test)
y_predict_train = modelo_1.predict(X_train)
mae_test = mean_absolute_error(y_test, y_predict_test)
r2_test = r2_score(y_test, y_predict_test)
mae_train = mean_absolute_error(y_train, y_predict_train)
r2_train = r2_score(y_train, y_predict_train)
print('Con datos de testeo: ',mae_test,r2_test)
print('Con datos de entrenamiento: ',mae_train,r2_train)

"""Se puede observar una importante rteduccion en el valor del mae a 241 millones, y un aumento en el r^2 a 0.39, lo que indica que este modelo desarrollado tiene una mejor performance que el desarrollado en primera instancia

###Ahora se agregan 3 variables mas a X para observar el cambio en las metricas elegidas para evaluar el performance
"""

X = datos_ml[['COD_UPZ_GRUPO','Habitaciones','Banos','CONJUNTO_CERRADO','SALARIO_ANUAL_MI','TIENE_ESCRITURA']]

Y = datos_ml["Precio_Millon"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 99)
modelo_2 = LinearRegression()
modelo_2.fit(X_train, y_train)
y_predict_test = modelo_2.predict(X_test)
y_predict_train = modelo_2.predict(X_train)
mae_test = mean_absolute_error(y_test, y_predict_test)
r2_test = r2_score(y_test, y_predict_test)
mae_train = mean_absolute_error(y_train, y_predict_train)
r2_train = r2_score(y_train, y_predict_train)
print('Con datos de testeo: ',mae_test,r2_test)
print('Con datos de entrenamiento: ',mae_train,r2_train)

"""##Aplicacion del modelo con un caso de prueba

Se utiliza para la prueba el ultimo modelo desarrollado, por lo que los datos necesarios seran:
* Codigo de UPZ: 816
* Cantidad de habitaciones: 3
* Cantidad de baños: 2
* Si es un conjunto cerrado: 1 (Si)
* Salario anual en millones: 50
* Si tiene escritura: 1 (Si)

###En base a los datos de prueba proporcionados, el modelo predice que el inmueble valdrá 476 millones de pesos colombianos
"""

modelo_2.predict([[816,3,2,1,50,1]])

"""##Modificacion de los datos utilizados para el modelado

###Ahora se busca saber si la afirmacion de que en caso de haber excluido una mayor cantidad de outliers, el modelo hubiera contado con menor cantidad de datos, pero hubiera tenido una mayor correlacion entre los variables seleccionadas para el modelaje, dando como resultado un modelo mas ajustado y con un error absoluto medio menor al obtenido
"""

datos_ml = datos_ml.query('Precio_Millon < 1500 & Precio_Millon > 60')
datos_ml

plt.figure(figsize = (6,8))
sns.boxplot(data = datos_ml, y = 'Precio_Millon');
plt.title('Grafico de Caja del recio por millon de los inmuebles')
plt.show()

plt.figure(figsize = (10,8))
sns.scatterplot(data = datos_ml, x = 'SALARIO_ANUAL_MI', y = 'Valor_m2_Millon');
plt.ylim((0,15))
plt.title('Grafico de dispersion del valor por millon del m2 en base al salario anual en millones')
plt.show()

datos_ml.corr()

plt.figure(figsize=(18, 8))
heatmap = sns.heatmap(datos_ml.corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlacion de las variables', fontdict={'fontsize':18}, pad=16);

"""###Modelado del Machine Learning con nuevos datos filtrados"""

x = datos_ml[['COD_UPZ_GRUPO','Habitaciones','Banos','CONJUNTO_CERRADO','SALARIO_ANUAL_MI','TIENE_ESCRITURA']]

y = datos_ml["Precio_Millon"]

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 99)
modelo_3 = LinearRegression()
modelo_3.fit(x_train, y_train)
y_predict_test = modelo_3.predict(x_test)
y_predict_train = modelo_3.predict(x_train)
mae_test = mean_absolute_error(y_test, y_predict_test)
r2_test = r2_score(y_test, y_predict_test)
mae_train = mean_absolute_error(y_train, y_predict_train)
r2_train = r2_score(y_train, y_predict_train)
print('Con datos de testeo: ',mae_test,r2_test)
print('Con datos de entrenamiento: ',mae_train,r2_train)

"""Se puede observar un descenso significativo del error absoluto medio a 144 millones de pesos y un aumento en el r^2 a 0.53, lo que lleva suponer que la afirmacion realizada previamente sobre el excluir mayor cantidad de outliers para obtener un modelo mas ajustado y con un MAE menor es correcta

###Ahora, se aplica este modelo obtenido sobre el caso de prueba presentado anteriormente
"""

modelo_3.predict([[816,3,2,1,50,1]])

"""En base a los datos de prueba proporcionados, el modelo predice que el inmueble valdrá 450 millones de pesos colombianos"""