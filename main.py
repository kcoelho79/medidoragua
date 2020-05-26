# water meter 

''''

class water meter
    

   (3) plot graph

    csv => select period (24 horas)
        => create graph
        => renderer graph
        => publish graph

'''

from watermeter import Watermeter
from watermeter import handle
from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

my_url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'


medidor = Watermeter()
medidor.start_display()
data = medidor.get_page()
#data = ['25', '22:50', 'P', '100.0%', '1.0', '21.0']
medidor.sanitize_data(data)

@app.route('/')
def index():

    wt = Watermeter()
    wt.start_display()
    dados = wt.get_page()
    arquivo = handle(dados)
    arquivo.csv_file()
    arquivo.clean()
    arquivo.period(day=1)
    arquivo.create_graph()
    wt.close_display()

    return ("<h1> /plot para visualizar grafico </h1>") 

@app.route('/plot')
def plot():
    return render_template('plot.html') 



# if __name__ == "__main__":
#     app.run(host='0.0.0.0')


