from watermeter import Watermeter

med = Watermeter()
med.start_display()
data = med.get_page()
med.save_data('Data.csv')