import os
from datetime import datetime
import pandas as pd

path_folder = r'C:\Users\densh\Desktop\курсовая\csv_files'

#метод сведения файлов к единому названию
def makeFormatFile():
    list_file_source = list()
    time = datetime.now().replace(day=1)
    time = time.strftime('%Y%m%d')
    search_for1 = 'export-kr1_1-'
    search_for2 = '-' + str(time)

    with os.scandir(path=path_folder) as it:
        for entry in it:
            if entry.is_file():
                print(entry.name)
                new_name = entry.name.replace(search_for1, '').replace(search_for2, '')
            os.rename(path_folder + "\\" + entry.name, path_folder + "\\" + new_name)
            list_file_source.append(path_folder + "\\" + new_name)
        print("Names changed")
    return list_file_source


#метод формирования единого csv-файла
def makeMainFile():
    list_df = list()
    list_file_source = makeFormatFile()
    for f in list_file_source:
        list_df.append(pd.read_csv(f, delimiter=';'))
    main_df = pd.concat(list_df, axis=0)
    main_df = main_df.replace(r'(.)обл$', r' область', regex=True)
    if os.path.exists(r'C:\Users\densh\Desktop\курсовая\main_df\main_file.csv'):
        os.remove(r'C:\Users\densh\Desktop\курсовая\main_df\main_file.csv')
    main_df.to_csv(path_or_buf=r'C:\Users\densh\Desktop\курсовая\main_df\main_file.csv', sep=';', index=False)
    return main_df


#получить dataframe
def getDataFrame(path):
    return pd.read_csv(path, delimiter=';', low_memory=False, decimal=",")
