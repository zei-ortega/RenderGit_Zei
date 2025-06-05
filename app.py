# -----------------------------------------------
# APLICACIÓN WEB INTERACTIVA CON DASH Y PLOTLY
# -----------------------------------------------

# Bibliotecas
import dash  
from dash import dcc, html, Input, Output  
import dash_bootstrap_components as dbc  
import pandas as pd  
import plotly.express as px  

df = pd.read_csv("/Users/rubiherso/Downloads/HRDataset_v14.csv") 

# Extraemos las columnas del DataFrame 
columnas = df.columns  

#--------------------------
# CREACIÓN DE LA APLICACIÓN 
#--------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # Estilo visual
app.title = "Dashboard - HRDataset" 

# ------------------------------------------------
# DISEÑO VISUAL DE LA APLICACIÓN / LAYOUT GENERAL
# ------------------------------------------------
app.layout = html.Div([
    html.H1("Dashboard - HRDataset", style={'textAlign': 'center'}),

   
    html.Div([ 
        # Menú: Tipo de gráfico
        html.Div([
            html.Label("Tipo de gráfico:"),
            dcc.Dropdown(
                id='chart-type',
                options=[
                    {'label': 'Gráfico de Barras', 'value': 'bar'},
                    {'label': 'Gráfico de Dispersión', 'value': 'scatter'},
                    {'label': 'Boxplot', 'value': 'box'},
                    {'label': 'Histograma', 'value': 'histogram'},
                    {'label': 'Sunburst', 'value': 'sunburst'},
                    {'label': 'Treemap', 'value': 'treemap'}
                ],
                value='bar' # Valor inicial
            )
        ], style={'width': '30%', 'padding': '10px'}),

        # Menú para eje X
        html.Div([
            html.Label("Variable X:"),
            dcc.Dropdown(
                id='x-axis',
                options=[{'label': col, 'value': col} for col in columnas],
                value='Department' 
            )
        ], style={'width': '30%', 'padding': '10px'}),

        # Menú para eje Y
        html.Div([
            html.Label("Variable Y:"),
            dcc.Dropdown(
                id='y-axis',
                options=[{'label': col, 'value': col} for col in columnas],
                value='Salary'
            )
        ], style={'width': '30%', 'padding': '10px'}),
    ], style={'display': 'flex', 'justifyContent': 'center'}),  # Alineación horizontal de los menús

    # Gráfico generado
    dcc.Graph(id='graph-output'),

    # Descripción 
    html.Div(id='graph-description', style={
        'textAlign': 'center',
        'padding': '20px',
        'fontSize': '16px',
        'fontStyle': 'italic'
    })
])

#----------
#CALLBACK
#----------
@app.callback(
    Output('graph-output', 'figure'),
    Output('graph-description', 'children'),
    Input('chart-type', 'value'),
    Input('x-axis', 'value'),
    Input('y-axis', 'value')
)
def update_graph(chart_type, x, y):
    if chart_type == 'bar':
        fig = px.bar(df, x=x, y=y)
    elif chart_type == 'scatter':
        fig = px.scatter(df, x=x, y=y)
    elif chart_type == 'box':
        fig = px.box(df, x=x, y=y)
    elif chart_type == 'histogram':
        fig = px.histogram(df, x=x)
    elif chart_type == 'sunburst':
        try:
            fig = px.sunburst(df, path=[x, y], values=y)
        except:
            fig = px.sunburst(df, path=[x, y])
    elif chart_type == 'treemap':
        try:
            fig = px.treemap(df, path=[x, y], values=y)
        except:
            fig = px.treemap(df, path=[x, y])
    else:
        fig = px.bar(df, x=x, y=y)

# Descripción 
    if chart_type in ['sunburst', 'treemap']:
        description = f"Este gráfico muestra la jerarquía entre **{x}** y **{y}**, útil para representar datos categóricos con niveles."
    elif chart_type == 'histogram':
        description = f"Este gráfico muestra cómo se distribuyen los valores de **{x}** en intervalos definidos."
    else:
        description = f"Este gráfico muestra cómo varía **{y}** según **{x}**."

    return fig, description


if __name__ == "__main__":
    app.run(debug=True)

