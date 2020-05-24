# water meter 

''''

class water meter
    url = url to webcrawler

    get_page() - ok
    dict_csv() - ok
    clean_data() - ok 
    append_timestamp() - ok
    select_period(hours) - ok   
    create_graph
    render_graph
    publish_graph
    

   (1) get page
  webcrawler
   url => fetch water  level <== dict

   (2) prepar to data
  parse

    dict => convert CSV 
         => sanitizacao 
         => clean up 
         => append timestamp
                             <== csv 

   (3) plot graph

    csv => select period (24 horas)
        => create graph
        => renderer graph
        => publish graph

'''

from watermeter import Watermeter
from watermeter import handle



my_url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'

# wt = Watermeter()
# wt.start_display()
# dados = wt.get_page()

dados = ['24', '12:59', 'P', '99.0%', '1.0', '22.0']

arquivo = handle(dados)
arquivo.csv_file('novo.csv')
print(arquivo.filename)

# wt.dict_tocsv()
# wt.clean_dataset(day=1)
# wt.close_display()


