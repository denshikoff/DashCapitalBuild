from pandas import DataFrame
from Connection.connection_v2 import getEngine
from Load.app import *
from sqlalchemy import insert

#form data


#table Source_Finance
df_way = makeMainFile()
df_way = DataFrame(df_obr['money_collecting_way'].unique())


#create connect
engine = getEngine()
'''
#add data in DB
try:
    DataFrame.to_sql(data_region, "Region", engine, "JKH", if_exists='append', index_label="Id_region")
except:
    print("Data 'Region' already exists")


#DataFrame.to_sql(df_way[0], "Source_finance", engine, "JKH", if_exists='replace', index_label="Id_variant")
df.to_excel()
'''