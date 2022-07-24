import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

df=pd.read_csv('employee_data.csv')

# El código que permita desplegar el logotipo de la empresa en la aplicación web.
image=Image.open('logo.jpeg')
st.image(image,use_column_width=True)

# El código que contenga las instrucciones para el despliegue de un título y una breve descripción de la aplicación web.
st.title('Socialize your Knowledge - Marketing')
st.write('Reporte para el análisis del desempeño de los colaboradores de Socialize your Knowledge del área de Marketing.')
st.write('---')

st.sidebar.header('Seleccionar parametros')

# El código que permita desplegar un control para seleccionar el género del empleado.
genero=st.sidebar.multiselect('Seleccionar el género',df['gender'].unique(),df['gender'].unique())

# El código que permita desplegar un control para seleccionar un rango del puntaje de desempeño del empleado.
max_val=max(df['performance_score'])
min_val=min(df['performance_score'])
valores=st.sidebar.slider('Puntaje de desempeño',min_value=min_val,max_value=max_val,value=(min_val,max_val))

# El código que permita desplegar un control para seleccionar el estado civil del empleado.
edo_civil=st.sidebar.multiselect('Seleccionar el estado civil',df['marital_status'].unique(),df['marital_status'].unique())

# El código que permita mostrar un gráfico en donde se visualice la distribución de los puntajes de desempeño.
filter=(df['performance_score']>=valores[0])&(df['performance_score']<=valores[1])&(df['gender'].isin(genero))&(df['marital_status'].isin(edo_civil))
df_des_fil=df[filter]['performance_score']
fig=px.histogram(
    data_frame=df_des_fil,
    title='Distribución de los puntajes',
    labels={'value':'Puntaje de desempeño'},
    hover_data={'variable':False}
)
fig.update_layout(showlegend=False)
fig.update_layout(bargap=0.1)
st.plotly_chart(fig)

# El código que permita mostrar un gráfico en donde se visualice el promedio de horas trabajadas por el género del empleado.
df_hours=df[filter][['gender','average_work_hours']]
df_hours=df_hours.groupby('gender').mean().reset_index()
fig2=px.bar(
    df_hours,
    x='gender',
    y='average_work_hours',
    title='Promedio de horas trabajadas',
    labels={'gender':'Género',
            'average_work_hours':'Promedio'}
)
st.plotly_chart(fig2)

# El código que permita mostrar un gráfico en donde se visualice la edad de los empleados con respecto al salario de estos.
df_edad=df[filter][['age','salary']]
df_edad=df_edad.groupby('age').mean().reset_index()
fig3=px.line(
    df_edad,
    x='age',
    y='salary',
    title='Edad respecto al salario',
    labels={'age':'Edad',
            'salary':'Salario promedio'}
)
st.plotly_chart(fig3)

# El código que permita mostrar un gráfico en donde se visualice la relación del promedio de horas trabajadas versus el puntaje de desempeño.
df_rel=df[filter]
fig4=px.scatter(
    df_rel,
    x='average_work_hours',
    y='performance_score',
    title='Horas trabajadas vs puntaje de desempeño',
    labels={'average_work_hours':'Horas trabajadas',
            'performance_score':'Puntaje de desempeño'}
)
st.plotly_chart(fig4)

# El código que permita desplegar una conclusión sobre el análisis mostrado en la aplicación web.
st.write('''
### Conclusión

Observando el contenido del reporte podemos notar primeramente que el puntaje de desempeño que más común entre los empleados es **3**.
De igual manera podemos notar que el promedio de horas trabajadas al mes es muy similar entre hombres y mujeres.
Finalmente notamos que no existe una relación entre el puntaje de desempeño y el promedio de horas trabajadas.
''')