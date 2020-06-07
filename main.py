
from watermeter import Watermeter
from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

my_url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'



@app.route('/')
def plot():
    med2 = Watermeter('2019.0071')
    plot_url = med2.save_graph('Data.csv')
    return render_template('plot.html', plot_url=plot_url)

# med.start_display()
# data = med.get_page()
# med.save_data('Data.csv')


if __name__ == "__main__":
    app.run(host='0.0.0.0')


