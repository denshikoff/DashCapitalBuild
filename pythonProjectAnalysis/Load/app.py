import plotly.express as px
from dash import Dash, html, dcc
from Transformation.Transformation import *
from dash import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd




labels_rg = {'money_ppl_collected_debts': 'Остаток задолженности по кредитам',
             'overhaul_funds_spent_all': 'Израсходовано средств по капитальному ремонту, тыс.руб.'}
labels_sb = {'mun_obr': 'Муниципальное образование',
             'overhaul_funds_spent_all': 'Израсходовано средств по капитальному ремонту, тыс.руб.'}

labels_class = { 'subject_rf': 'Субъекты',
'Count_energy_efficiency': 'Количество домов',
'energy_efficiency':'Тип класса'
}
# df регион - потрачено_средств
def_class = classEnergyForRegion()


fig_circle = px.pie(def_class, values='Count_energy_efficiency', names='energy_efficiency', labels=labels_class, width=700, height=500)

#фильтр по региону
listSb = getListSb()
Sb_select = dcc.Dropdown(listSb, id='sb_select', value=listSb[0])
# селекторы
dis_rg = getLoanMinMax(getLoanRegion())



#селектор по региону
loan_selector_rg = dcc.RangeSlider(
    id='range_slide_rg',
    min=dis_rg[0],
    max=dis_rg[1],
    marks={0: '0',
           1000000: '1000000',
           5000000: '5000000',
           10000000: '10000000',
           15000000: '15000000',
           dis_rg[1]: str(dis_rg[1])},
    step=1,
    value=[0, math.ceil(dis_rg[1])]
)

#селектор по субъекту
loan_selector_sb = dcc.RangeSlider(
    id='range_slide_sb',
    max=1000000,
    marks={0: '0',
           50000: '50000',
           150000: '150000',
           250000: '250000',
           500000: '500000',
           700000: '700000'},
    step=1,
    value=[0, 600000]
)

axis_gr2 = dcc.RadioItems(['X', 'Y'], id='radiobutt_sb', value='X')
axis_gr1 = dcc.RadioItems(['X', 'Y'], id='radiobutt_rg', value='X')

#styles
stylesGr = {'width': '600px', 'margin-bottom': '40px'}

#Region TAB график по РФ
tab1_content = [dbc.Row(html.H2('Данные по РФ')),
                dbc.Row(
                    dbc.Col([html.Div('Остаток задолженности по кредитам'),
                             html.Div(loan_selector_rg, style=stylesGr),
                             html.Div(axis_gr1)], width={'size':2})
                ),
                dbc.Row([
                        dbc.Col([html.Div('Классы энергоэффективности'),
                                 dcc.Graph(id='regions')], width={'size':6}),
                        dbc.Col([html.Div('Классы энергоэффективности'),
                                 dcc.Graph(figure=fig_circle)],
                    )],style={'margin-bottom': '60px'})
                    ]

#график по субъектам
tab2_content = [
                dbc.Row(html.H2('Данные по субъекту')),

                dbc.Row([
                    dbc.Col([html.Div('Остаток задолженности по кредитам'),
                             html.Div(loan_selector_sb, style=stylesGr),
                             html.Div(axis_gr2)], width={'size': 2}),
                    dbc.Col(html.Div(Sb_select, style={'margin-top':'40px'}), width={'size': 3, 'offset':2})
                ], style={'margin-bottom': '40px'}),
                dbc.Row(dcc.Graph(id='sb'))]


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Row(html.H1('Аналитика на основе данных реформы ЖКХ'), style={'margin-top': '20px','margin-bottom': '60px'}),
    dbc.Tabs([
        dbc.Tab(tab1_content, label='Данные по РФ'),
        dbc.Tab(tab2_content, label='Данные по субъекту'),
    ])
],
    style= {'margin-left': '80px', 'margin-right':'80px'})



def createDfFilter(df, dis):
    df = df.astype({'money_ppl_collected_debts': int}, errors='raise')
    return df[(df['money_ppl_collected_debts'] >= dis[0]) & (df['money_ppl_collected_debts'] <= dis[1])]





# фильтр по долгам по регионам
@app.callback(
    Output(component_id='regions', component_property='figure'),
    [Input(component_id='range_slide_rg', component_property='value'),
    Input(component_id='radiobutt_rg', component_property='value')]
)
def updateRegionsForLoan(dis, rb):
    df_rg = getDfRegion()
    df_loan = getLoanRegion()
    df_count_home = getCountHouse()
    df = pd.merge(df_rg, df_loan, on='subject_rf')
    df = pd.merge(df, df_count_home, on='subject_rf')
    df = createDfFilter(df, dis)
    if rb == 'X':
        X = 'overhaul_funds_spent_all'
        Y = 'money_ppl_collected_debts'
    else:
        X = 'money_ppl_collected_debts'
        Y = 'overhaul_funds_spent_all'
    fig = px.scatter(df, x=X, y=Y, hover_name='subject_rf',
                     size='Count_home_in_Region',
                 labels=labels_rg)
    return fig

# фильтры по субъекту
@app.callback(
    Output(component_id='sb', component_property='figure'),
    [Input(component_id='range_slide_sb', component_property='value'),
     Input(component_id='sb_select', component_property='value'),
     Input(component_id='radiobutt_sb', component_property='value')]
)
def updateSbForLoan(dis, sb, rb):
    df_sb = getDfMun_obr(sb)
    df_loan = getLoanMunObr(sb)
    df = pd.merge(df_sb, df_loan, on='mun_obr')
    df = createDfFilter(df, dis)
    if rb == 'X':
        X = 'overhaul_funds_spent_all'
        Y = 'mun_obr'
    else:
        X = 'mun_obr'
        Y = 'overhaul_funds_spent_all'
    fig = px.bar(df, y=Y, x=X,
                 title=sb,
                 labels=labels_sb)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
