# water meter 

''''

class water meter
    url = url to webcrawler

    fetch_data()
    convert_csv()
    clean_data()
    append_timestamp()
    select_period(hours)
    create_graph
    render_graph
    publish_graph
    

   (1) fetch data
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

my_url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'

wt = Watermeter()
wt.fetch_data()