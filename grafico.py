import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from flask import Flask, Response
import io, random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure



def preparaDados():
    csv = pd.read_csv('data.csv', index_col= False , parse_dates = ["data"])
    csv['medicao'] = pd.to_numeric(csv['medicao'].str.split(".").str.get(0))
    csv['horas'] = pd.to_datetime(csv['horas'], format='%H:%M').dt.time
    return csv

app = Flask(__name__)

@app.route('/plot.png')
def plot_png():
    csv = preparaDados()
    fig = create_figure(csv)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure(csv):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = csv['dia'] 
    ys = csv['medicao']
    axis.plot(xs, ys)
    return fig

def grafico_dash(csv):

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



# grafico_dash(csv)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

   
