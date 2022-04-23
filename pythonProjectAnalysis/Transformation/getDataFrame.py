from Connection.connection_v2 import getEngine
from Extract.extractData import getDataFrame
import pandas as pd
import numpy as np
df = getDataFrame(r'C:\Users\densh\Desktop\курсовая\main_df\main_file.csv')

#формирование справочников

#источник финансирования фонда
try:

    ar = df['money_collecting_way'].unique()
    df_finance = pd.DataFrame(ar, index=list(range(1, len(ar) + 1)), columns=['Name'])
    eng = getEngine()
    pd.DataFrame.to_sql(df_finance, con=eng, name="Source_finance", schema="JKH", index=True, index_label="Id_variant")
except:
    print('Data Source_finance already exists')

#регионы
try:
    df_region = pd.read_csv(r'C:\Users\densh\Desktop\курсовая\sb.csv', delimiter=';', low_memory=False)
    pd.DataFrame.to_sql(df_region, con=eng, name="Region", schema="JKH")
except:
    print('Data Region already exists')



#pd.DataFrame.to_sql(df_energy, con=eng, name=)



#home

#credit org

