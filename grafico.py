import pandas as pd

csv = pd.read_csv('data.csv', index_col= False , parse_dates = ["data"])
csv['medicao'] = pd.to_numeric(csv['medicao'].str.split(",").str.get(0))
print(csv.dtypes)


import plotly.express as px
#df = px.data(csv)
fig = px.line(csv, x="horas", y="medicao")
fig.show()

# import matplotlib.pyplot as plt
# csv.plot()