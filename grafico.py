import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px


csv = pd.read_csv('data.csv', index_col= False , parse_dates = ["data"])
csv['medicao'] = pd.to_numeric(csv['medicao'].str.split(".").str.get(0))
csv['horas'] = pd.to_datetime(csv['horas'], format='%H:%M').dt.time
print(csv.dtypes)
print(csv['horas'])
#fig = px.line(csv, x="horas", y="medicao")
#fig.show()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1(children='Caixa 119'),

    html.Div(children='''
        Medidor de Agua: Leitor da Caixa de Água .
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': csv['horas'], 'y': csv['medicao'], 'type': 'line', 'name': 'SF'},
                
            ],
            'layout': {
                'title': 'Mediçao Caixa de Agua'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)

   
