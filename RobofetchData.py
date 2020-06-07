from watermeter import Watermeter

med = Watermeter('2019.0071')
med.start_display()
data = med.get_page()
med.save_data('Data.csv')
med.close_display()