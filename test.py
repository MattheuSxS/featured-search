import pandas as pd

df = pd.read_excel('/Users/matheus.santos.silva/Documents/Project_datalake/gitlab/featured-search/featured-search/configs/Geral_RJ.xlsx')

print(df.dtypes)
print(df.get('Tdur'))