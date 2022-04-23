import math

from Extract.extractData import getDataFrame


df_main = getDataFrame(r'C:\Users\densh\Desktop\курсовая\main_df\main_file.csv')

# аргумент - регион
def getDfMun_obr(s):
    df = df_main
    df = df.loc[df['subject_rf'] == s]
    df_s = df.groupby('mun_obr')['overhaul_funds_spent_all'].sum()
    df_s = df_s[df_s > 0]
    return df_s.to_frame().reset_index()


def getDfRegion():
    df = df_main
    df_s = df.groupby('subject_rf')['overhaul_funds_spent_all'].sum()
    df_s = df_s[df_s > 3]
    df = df_s.to_frame().reset_index()
    return df


# шкала регионов по долгам
def getLoanRegion():
    df = df_main
    df = df.groupby('subject_rf')['money_ppl_collected_debts'].sum()
    return df.to_frame().reset_index()

def getCountHouse():
    df = df_main
    df = df.groupby('subject_rf')['mkd_code'].count().rename('Count_home_in_Region')
    df = df[df > 3]
    return df.to_frame().reset_index()


# шкала мунобр по долгам
def getLoanMunObr(s):
    df = df_main
    df = df.loc[df['subject_rf'] == s]
    df = df.groupby('mun_obr')['money_ppl_collected_debts'].sum()
    return df.to_frame().reset_index()

def getLoanMinMax(dataframe_loan):
    return [math.floor(min(dataframe_loan['money_ppl_collected_debts'])), math.ceil(max(dataframe_loan['money_ppl_collected_debts']))]


# классы энергоэффективности количество каждого из классов(наложить цвет классов?)
#класс энергоэфффективности

def classEnergyForRegion():
    df_s = df_main.groupby(['energy_efficiency'])['energy_efficiency'].count().rename('Count_energy_efficiency')
    return df_s.to_frame().reset_index()

def getListSb():
    return df_main['subject_rf'].unique()
