from flask import Flask
import pandas as pd
import plotly.express as px


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def index():
    return '<h1> Exemplo Rodando APP Flask Nginx e uwsgi </h1>'


@app.route("/grafico")
def grafico():
    csv = pd.read_csv('data.csv', index_col= False , parse_dates = ["data"])
    csv['medicao'] = pd.to_numeric(csv['medicao'].str.split(".").str.get(0))
    csv['horas'] = pd.to_datetime(csv['horas'], format='%H:%M').dt.time
    print(csv.dtypes)
    print(csv['horas'])
    fig = px.line(csv, x="horas", y="medicao")
    fig.show()
    


if __name__ == "__main__":
    app.run(host='0.0.0.0')




