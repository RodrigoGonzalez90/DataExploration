import streamlit as st
import pandas as pd
# import screeninfo
import plotly.express as px


st.set_page_config(page_title = "Exploracion de datos",
                   page_icon = ":hammer_and_wrench:",
                   layout = "wide")

st.title("Exploracion de datos:")
st.markdown("")
st.info( """

        ###### **Importante:**

        * ###### Es necesario que los datos se encuentren normalizados.

        * ###### La cantidad de datos por columna deben coincidir en todas las columnas.

        * ###### Los valores numericos deben ser del tipo numero, no string.

        """)

def cargar():
    files = st.file_uploader("Datos para el análisis.", accept_multiple_files=True)
    return files

# def get_screen_size():
#     screen_info = screeninfo.get_monitors()[0]
#     width, height = screen_info.width, screen_info.height
#     return width, height

def create_scatter_plot(df, x_column, y_column, selected_columns):
    fig = px.scatter(df, x=x_column, y=y_column)
    # Verifica si hay más de dos columnas seleccionadas
    if len(selected_columns) > 2:
        # Agrega los conjuntos de datos adicionales como trazos en la figura
        for column in selected_columns[2:]:
            fig.add_scatter(x=df[x_column], y=df[column], mode='markers', name=column)
            total_sum = df[column].sum()
            fig.add_annotation(x=df[x_column], y=df[column], text=f"Suma Total: {total_sum}", showarrow=False)
    
    return fig


def create_bar_plot(df, x_column, y_column, selected_columns):
    fig = px.bar(df, x=x_column, y=y_column, barmode='group')
    
    # Agrega los conjuntos de datos adicionales como trazos en la figura
    for column in selected_columns[2:]:
        fig.add_bar(x=df[x_column], y=df[column], name=column)
        total_sum = df[column].sum()
        fig.add_annotation(x=df[x_column], y=df[column], text=f"Suma Total: {total_sum}", showarrow=False)
    
    return fig

def create_line_plot(df, x_column, y_column, selected_columns):
    fig = px.line(df, x=x_column, y=y_column)
    total_sum = y_column.sum()
    fig.add_annotation(x=x_column, y=y_column, text=f"Suma Total: {total_sum}", showarrow=False)
    # Agrega los conjuntos de datos adicionales como trazos en la figura
    for column in selected_columns[2:]:
        fig.add_scatter(x=df[x_column], y=df[column], mode='lines', name=column)
        total_sum = df[column].sum()
        fig.add_annotation(x=df[x_column], y=df[column], text=f"Suma Total: {total_sum}", showarrow=False)

    return fig
  
# def calculate_difference(df_selected, selected_columns):
#     difference_df = df_selected[selected_columns].diff()
#     return difference_df

    
files = cargar()
# screen_width, screen_height = get_screen_size()

if files:

        selected_file = st.multiselect("Seleccionar archivo", options=[i.name for i in files], key=[uploaded_file for uploaded_file in files])

        if selected_file:
            dfs = []  # Lista para almacenar los DataFrames
            suffix_counter = 1
            
            for uploaded_file in files:
                if uploaded_file.name in selected_file:
                    df_selected = pd.read_excel(uploaded_file)
                    info = {
                        "Column Names": df_selected.columns.tolist(),
                        "Data Types": df_selected.dtypes.tolist(),
                        "Non-null Count": df_selected.count().tolist(),
                        }
                    st.title(uploaded_file.name)
                    st.table(pd.DataFrame(info))
                    # Agregar sufijo numérico a las columnas
                    suffix = f"{suffix_counter:02d}"  # Utiliza un número secuencial como sufijo
                    file_name = uploaded_file.name.split(".")[0]  # Obtiene el nombre del archivo sin extensión
                    df_selected.columns = [file_name + "_" + col + "_" + suffix for col in df_selected.columns]
                    #df_selected.columns = [col + "_" + suffix for col in df_selected.columns]
                    dfs.append(df_selected)
                    suffix_counter += 1

            if dfs:
                df_selected = pd.concat(dfs, axis=1)
#                 st.dataframe(df_selected, height=int(screen_height * 0.8), width=int(screen_width * 0.8))
                st.dataframe(df_selected)
                selected_columns = st.multiselect("Seleccionar columnas comenzando por la variable independiente (X) y luego las variables dependientes(Y)", options=df_selected.columns.tolist(), key=f'{uploaded_file}+1')

                dtypes = df_selected[selected_columns].dtypes
                if selected_columns and len(selected_columns) >= 2:
                    st.write("Columnas seleccionadas", dtypes)

                    # Selecciona las columnas para el eje x e y del gráfico
                    x_column = selected_columns[0]
                    y_column = selected_columns[1]

                    tipo_grafico = st.selectbox(
                        label='Seleccionar tipo de gráfico',
                        options=['Dispersion', 'Barras', 'Lineas'],
                        key=f'{uploaded_file}+2'
                    )

                    fig = None

                    if tipo_grafico == 'Dispersion':
                        fig = create_scatter_plot(df_selected, x_column, y_column, selected_columns)
                    elif tipo_grafico == 'Barras':
                        fig = create_bar_plot(df_selected, x_column, y_column, selected_columns)
                    elif tipo_grafico == 'Lineas':
                        fig = create_line_plot(df_selected, x_column, y_column, selected_columns)

                    if fig is not None:
                        # Modifica el tamaño del gráfico
#                         fig.update_layout(width=int(screen_width * 0.8), height=int(screen_height * 0.8))
                        st.plotly_chart(fig)
  
#                     if st.button("Calcular diferencia"):
#                         difference_df = calculate_difference(df_selected, selected_columns)
#                         st.dataframe(difference_df)
                else:
                    st.warning("Debe seleccionar al menos dos columnas para graficar.")

else:
    st.warning("Seleccione los datos primero.")
