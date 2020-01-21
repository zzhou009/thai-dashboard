# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 18:27:46 2019

@author: ZHOUZH
"""

#import library

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table


import pandas as pd

import numpy as np

from datetime import datetime,timedelta

#define function for producing date list

def datelist(beginDate, endDate): 
    date_l=[datetime.strftime(x,'%Y-%m-%d') for x in pd.date_range(start=beginDate, end=endDate).tolist()]
    return date_l


daily_data = pd.read_csv("https://raw.githubusercontent.com/zzhou009/thai-dashboard/master/daily_NEW_20200121.csv?token=AMCDFYEY24OUEIJXKWD5WRC6E2HGA&_sm_au_=iVVF7vrZTHJnvk40pFW0jKQL3FMFC",index_col=0, skipinitialspace=True)


pd.options.mode.chained_assignment = None  # default='warn'




#input data, split data into 7 dataframes

daily_data.replace(0, np.nan, inplace=True)
daily_data = daily_data.drop(pd.Timestamp('2016-02-29'), axis = 0)
daily_data = daily_data.drop(pd.Timestamp('2020-02-29'), axis = 0)
item = list(daily_data)
daterange = datelist('2016-11-01', '2017-06-15')
daterange = [datetime.strptime(x,'%Y-%m-%d') for x in daterange]

df=list()

for i in range(0,len(daily_data.columns)):

    data1 = daily_data.loc['2012-11-01':'2013-06-15',[item[i]]].reset_index(drop=True) 
    data1.columns = ['']

    data2 = daily_data.loc['2013-11-01':'2014-06-15',[item[i]]].reset_index(drop=True) 
    data2.columns = ['']

    data3 = daily_data.loc['2014-11-01':'2015-06-15',[item[i]]].reset_index(drop=True) 
    data3.columns = ['']

    data4 = daily_data.loc['2015-11-01':'2016-06-15',[item[i]]].reset_index(drop=True) 
    data4.columns = ['']

    data5 = daily_data.loc['2016-11-01':'2017-06-15',[item[i]]].reset_index(drop=True) 
    data5.columns = ['']

    data6 = daily_data.loc['2017-11-01':'2018-06-15',[item[i]]].reset_index(drop=True) 
    data6.columns = ['']

    data7 = daily_data.loc['2018-11-01':'2019-06-15',[item[i]]].reset_index(drop=True) 
    data7.columns = ['']

    data8 = daily_data.loc['2019-11-01':'2020-06-15',[item[i]]].reset_index(drop=True) 
    data8.columns = ['']

    data = {'2012': data1.iloc[:,0].tolist(), '2013': data2.iloc[:,0].tolist(),'2014': data3.iloc[:,0].tolist(),'2015': data4.iloc[:,0].tolist(),'2016': data5.iloc[:,0].tolist(),'2017': data6.iloc[:,0].tolist(),'2018': data7.iloc[:,0].tolist(),'2019': data8.iloc[:,0].tolist()}

    dataframe0 = pd.DataFrame(data, index =daterange)
    df.append(dataframe0)
    

newsugaridx = df[5].copy()    
newrawidx = df[6].copy()

    
# for indicators, omit outliners
df[5].loc['2016-12-29':'2017-01-03',:] = np.nan
df[5].loc['2017-04-01':'2017-06-15',:] = np.nan
df[6].loc['2017-01-01':'2017-01-03',:] = np.nan
df[6].loc['2017-04-01':'2017-06-15',:] = np.nan
    


#-----------------------------------------------

def generate_table(dataframe, max_rows=8):
    indexlist=list(dataframe.index.strftime("%m-%d"))   
    date = datetime.today().strftime('%m-%d')
    enddate = indexlist.index(date)
    dataframe = dataframe.round(1)
    dataframe = dataframe.reset_index()
    dataframe["index"] = pd.to_datetime(dataframe["index"]).dt.strftime('%m-%d')
    dataframe.columns = ['Date','2012','2013','2014','2015','2016','2017','2018']
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(enddate-10, enddate)]
    )
    

#-----------------------------------------------    
    
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


#-----------------------------------------------

#create table list showing on the page (40lines)

indexlist=list(df[0].index.strftime("%m-%d"))
date = datetime.today().strftime('%m-%d')
enddate = indexlist.index(date)
startend = range(enddate-40, enddate+1)

showdf0 = list()

for i in range(0,len(df)):

    showdf = df[i].iloc[startend,:]
    showdf = showdf.round(1)
    showdf = showdf.reset_index()
    showdf["index"] = pd.to_datetime(showdf["index"]).dt.strftime('%m-%d')
    showdf.columns = ['Date','2012','2013','2014','2015','2016','2017','2018','2019']
    showdf0.append(showdf)

#-----------------------------------------------

indexlist0 = indexlist

markdown_text = '### Daily Crush & Production Data'

draw_line = '---'

#-----------------------------------------------

#deal with crush data
crushidx = df[0].copy()

for i in range(0,len(crushidx.columns)):

    crushidx.iloc[:,i] = crushidx.iloc[:,i]/crushidx.iloc[:,i].max(axis=0)      

crushidx['Max'] = crushidx.iloc[:,0:7].max(axis=1)

#calculate last 5-day avg ratio
ncount = 0
ratiocount = 0
avgratio = 0

for i in range(0,10):
    if ncount < 5:     
        idate = crushidx.loc[:,'2019'].last_valid_index() - timedelta(days=i)
        if idate not in pd.date_range('2016-12-29','2017-01-02').tolist():
            ncount = ncount + 1
            ratiocount = ratiocount + crushidx.loc[idate,'2019']/crushidx.loc[idate,'Max']
avgratio = ratiocount/ncount
avgratio = round(avgratio*100,1)    


crushidx1 = crushidx.iloc[0:61,:]

crushidx2 = crushidx.iloc[61:151,:]

crushidx3 = crushidx.iloc[151:227,:]

crush0 = list()

for i in range(0,len(crushidx.columns)-1):

    crush11 = crushidx.ix[crushidx.iloc[:,i].first_valid_index():'2016-12-31',i].tolist()

    crushdiff = 61-len(crush11)

    crush11 = np.append(crush11, np.zeros(crushdiff) + np.nan).tolist()

    crush0.append(crush11)


daterange2 = datelist('2016-11-01','2016-12-31')
daterange2 = [datetime.strptime(x,'%Y-%m-%d') for x in daterange2]

crushidx1 = pd.DataFrame(crush0, columns = range(1,62),dtype = float).transpose()

crushidx1.columns = ['2012','2013','2014','2015','2016','2017','2018','2019'] 

crushidx1['Max'] = crushidx1.iloc[:,0:7].max(axis=1)

crushidx1.loc[32:61,'Max']=np.nan



indexcrush1=list(range(1,62))
indexcrush2=list(crushidx2.index.strftime("%m-%d"))
indexcrush3=list(crushidx3.index.strftime("%m-%d"))




#______deal with indicators: sugar/crush (kg/mt)________

sugaridx = df[5].copy()


sugar2019max = sugaridx.loc[:,'2019'].max(axis=0) 

for i in range(0,len(sugaridx.columns)):

    sugaridx.iloc[:,i] = sugaridx.iloc[:,i]/sugaridx.iloc[:,i].max(axis=0)
    
sugaridx.loc[:,'2019'].max(axis=0)     

sugaridx['Max'] = sugaridx.iloc[:,0:7].max(axis=1)

sugaridxratio = sugaridx.loc[sugaridx.loc[:,'2019'].last_valid_index(),'2019']/sugaridx.loc[sugaridx.loc[:,'2019'].last_valid_index(),'Max']

sugaridx2019 = sugaridx.loc[:,'2019'].last_valid_index() + timedelta(days=1)

sugaridx.loc[(sugaridx.loc[:,'2019'].last_valid_index() + timedelta(days=1)):'2017-03-31','2019'] = sugaridxratio*sugaridx.loc[(sugaridx.loc[:,'2019'].last_valid_index() + timedelta(days=1)):'2017-03-31','Max']




newsugaridx.loc[sugaridx2019:'2017-03-31','2019'] = sugaridx.loc[sugaridx2019:'2017-03-31','2019'] * sugar2019max 

newsugaridx_f = newsugaridx.copy()

newsugaridx_f.loc['2016-12-29':'2017-01-03',:] = np.nan
newsugaridx_f.loc['2017-04-01':'2017-06-15',:] = np.nan




#---------deal with indicators: raws/sugar 
rawidx = df[6].copy()



raw2019max = rawidx.loc[:,'2019'].max(axis=0) 

for i in range(0,len(rawidx.columns)):

    rawidx.iloc[:,i] = rawidx.iloc[:,i]/rawidx.iloc[:,i].max(axis=0)
    
rawidx.loc[:,'2019'].max(axis=0)     

rawidx['Max'] = rawidx.iloc[:,0:7].max(axis=1)

rawidxratio = rawidx.loc[rawidx.loc[:,'2019'].last_valid_index(),'2019']/rawidx.loc[rawidx.loc[:,'2019'].last_valid_index(),'Max']

rawidx2019 = rawidx.loc[:,'2019'].last_valid_index() + timedelta(days=1)

rawidx.loc[(rawidx.loc[:,'2019'].last_valid_index() + timedelta(days=1)):'2017-03-31','2019'] = rawidxratio*rawidx.loc[(rawidx.loc[:,'2019'].last_valid_index() + timedelta(days=1)):'2017-03-31','Max']




newrawidx.loc[rawidx2019:'2017-03-31','2019'] = rawidx.loc[rawidx2019:'2017-03-31','2019'] * raw2019max 

newrawidx_f = newrawidx.copy()

newrawidx_f.loc['2016-12-29':'2017-01-03',:] = np.nan
newrawidx_f.loc['2017-04-01':'2017-06-15',:] = np.nan




#==================================================

#---------------------------------------------------

#deal with other sugar production
othersidx = df[3].copy()

othersidx[othersidx<0] = 0

for i in range(0,len(othersidx.columns)):

    othersidx.iloc[:,i] = othersidx.iloc[:,i]/othersidx.iloc[:,i].max(axis=0)      

othersidx['Max'] = othersidx.iloc[:,0:7].max(axis=1)



#calculate last 5-day avg ratio
ncount_o = 0
ratiocount_o = 0
avgratio_o = 0

for i in range(0,10):
    if ncount_o < 5:     
        idate_o = othersidx.loc[:,'2019'].last_valid_index() - timedelta(days=i)
        if idate_o not in pd.date_range('2016-12-29','2017-01-02').tolist():
            ncount_o = ncount_o + 1
            ratiocount_o = ratiocount_o + othersidx.loc[idate_o,'2019']/othersidx.loc[idate_o,'Max']
avgratio_o = ratiocount_o/ncount_o
avgratio_o = round(avgratio_o*100,1)    





othersidx1 = othersidx.iloc[0:61,:]

othersidx2 = othersidx.iloc[61:151,:]

othersidx3 = othersidx.iloc[151:227,:]

others0 = list()



for i in range(0,len(othersidx.columns)-1):

    others11 = othersidx.ix[othersidx.iloc[:,i].first_valid_index():'2016-12-31',i].tolist()

    othersdiff = 61-len(others11)

    others11 = np.append(others11, np.zeros(othersdiff) + np.nan).tolist()

    others0.append(others11)
    
    

othersidx1 = pd.DataFrame(others0, columns = range(1,62),dtype = float).transpose()

othersidx1.columns = ['2012','2013','2014','2015','2016','2017','2018','2019'] 

othersidx1['Max'] = othersidx1.iloc[:,0:7].max(axis=1)

othersidx1.loc[32:61,'Max']=np.nan



#==============Given a total crush number===========================



setcrush = 102400000

clicknum=None








#-----------------------------------------------

app.layout = html.Div([
    
    html.Div([
        html.Div("_",style={'backgroundColor':'rgb(50,85,110)','color':'rgb(50,85,110)'}),
        html.Img(src=r'http://mars/SUGAR/Content/img/logo.png', height='55%'),
        html.Div("_____",style={'backgroundColor':'rgb(50,85,110)','color':'rgb(50,85,110)'}),
        html.Div("  Thailand Sugar Crush & Production Dashboard", className='banner',style={'backgroundColor':'rgb(50,85,110)','height':'80px','color':'white','font-size':'36px','display':'flex','align-items':'center'})  
    ],
        style={'backgroundColor':'rgb(50,85,110)','height':'80px','color':'white','margin-top':'0','display':'flex','align-items':'center'}),     
        
    dcc.Markdown(
        children = markdown_text,
        style = {'margin-left':'400px'}
    ),    

    dcc.Dropdown(
                id='filter',
                options=[{'label': daily_data.columns[i], 'value': i} for i in range(0,len(daily_data.columns))],
                value=0,
                style = {
                'width':'30%',
                'margin-left':'200px'
                
                        
                }
    ),
    
    html.Br(),
    
    dash_table.DataTable(
        id='loading-states-table',
        columns=[{"name": i, "id": i,'deletable':True,'renamable':True} for i in showdf.columns],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_table={
            'margin-left':'400px',    

            'width':'900px',                             
            'maxHeight': '300px'

        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'Date'},
                'width':'100px'
            },
 
            {
                'if': {'column_id': '2012'},
                'width':'100px'
            },

            {
                'if': {'column_id': '2013'},
                'width':'100px'
            },
            
            {
                'if': {'column_id': '2014'},
                'width':'100px'
            },            
            
            {
                'if': {'column_id': '2015'},
                'width':'100px'
            }, 

            {
                'if': {'column_id': '2016'},
                'width':'100px'
            }, 

            {
                'if': {'column_id': '2017'},
                'width':'100px'
            }, 

            {
                'if': {'column_id': '2018'},
                'width':'100px'
            }, 

            {
                'if': {'column_id': '2019'},
                'width':'100px'
            } 
              
        ],

        style_data_conditional=[
            {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
            },
                
            {
            'if': {'column_id': 'Date'},
            'fontWeight': 'bold',
            }
        ],
        editable=False    
    ),
    

    html.Br(),

    
    dcc.Graph(
        id = 'basic-interactions',
        style={'margin-left':'200px'}
            
    ),
    


    html.Br(),
    dcc.Markdown(children = draw_line),

  
    html.Div([

        dcc.Markdown(
            children = '### Daily Crush Index (compared with yearly max quantity) & Historical Max Ratio'
        ),           
        
        html.Br(),
        
        dcc.Markdown(
            children = 'Enter the estimated total crush quantity (mmt) below:'
        ),   
                
        dcc.Input(
        id='input_crush',
        placeholder='Enter a number ...',
        type='number',
        value=102.4
        ),  

        html.Button('Submit', id='button'),

        html.Br(),
        html.Br(),
        html.Div(

        dcc.Markdown(
            children = 'The average daily crush ratio/max during past 5 days is {}% (excluding 29th Dec-2nd Jan).'.format(avgratio)
        )
        ),  


        html.Div(id='slider-output-container'),
        
     
        
        
        
        dcc.Slider(
            id='crush-slider',
            min=0,
            max=1,
            step=0.01,
            value=1,
            marks={
                0:'0%',
                0.5:'50%',
                0.8:'80%',
                0.85:'85%',
                0.9:'90%',
                0.95:'95%',
                1:'100%'                
            },
              
        ),
        html.Div(id='slider-output-container2'),                
                
                
    ],
        style={
            'width':'40%'                  
        }  
    ),   
    
    html.Br(),    


    html.Div(id='crush1-inter', style={'display': 'none'}),
    html.Div(id='crush2-inter', style={'display': 'none'}),
    html.Div(id='crush3-inter', style={'display': 'none'}),



    
    html.Div([
        html.Div(
            dcc.Graph(
                id = 'crush1',
            ),

            style = {'width':'33%','display':'inline-block'}
    
        ),
    

        html.Div(
            dcc.Graph(
                id = 'crush2', 
            ),
            style = {'width':'33%','display':'inline-block'}
    
        ),


         html.Div(
            dcc.Graph(
                id = 'crush3',
        
                figure={
                    'data':[
                        {
                            'x':indexcrush3,
                            'y':crushidx3['2012'].tolist(),
                            'name':'2012',
                            'mode':'lines',
                            'line':{'width':3}         
                        },

                        {
                            'x':indexcrush3,
                            'y':crushidx3['2013'].tolist(),
                            'name':'2013',
                            'mode':'lines',
                            'line':{'width':3}         
                        },                
            
                        {
                            'x':indexcrush3,
                            'y':crushidx3['2014'].tolist(),
                            'name':'2014',
                            'mode':'lines',
                            'line':{'width':3}         
                        },                    
    
                        {
                            'x':indexcrush3,
                            'y':crushidx3['2015'].tolist(),
                            'name':'2015',
                            'mode':'lines',
                            'line':{'width':3}         
                        },

                        {
                            'x':indexcrush3,
                            'y':crushidx3['2016'].tolist(),
                            'name':'2016',
                            'mode':'lines',
                            'line':{'width':3}         
                        },

                        {
                            'x':indexcrush3,
                            'y':crushidx3['2017'].tolist(),
                            'name':'2017',
                            'mode':'lines',
                            'line':{'width':3}         
                        },
    
                        {
                            'x':indexcrush3,
                            'y':crushidx3['2018'].tolist(),
                            'name':'2018',
                            'mode':'lines',
                            'line':{'width':3}         
                        },

                        {
                            'x':indexcrush3,
                            'y':crushidx3['2019'].tolist(),
                            'name':'2019',
                            'mode':'lines',
                            'line':{
                                'width':3
                        
                            }         
                        },
    
                        {
                            'x':indexcrush3,
                            'y':crushidx3['Max'].tolist(),
                            'name':'Max',
                            'mode':'lines',
                            'line':{
                                'width':1.5,
                                'dash':'dash',
                                'color':'rgb(0,0,0)'
                            
                            }         
                        }                    
        
        
                    ],       
                    'layout':{
                        'title':'Crush - 3rd Section - After 1st Apr',
                        'showlegend':'false',
                        
                        'height':600,
                        'xaxis':{
                            'type':'category'
                            
                        },
                        'hovermode':'closest'
                    }
                
     
                }    
            ),
            style = {'width':'33%','display':'inline-block'}
    
        )
    
    ]),


#===========================
    html.Br(),


    dcc.Graph(

        id = 'sugar crush absolute',
        style={'margin-left':'200px'},
    ),    
        
#=======================

    html.Br(),
    dcc.Markdown(children = draw_line),
 
    html.Div(id='sugar-inter', style={'display': 'none'}),
 #   
    html.Div([

        dcc.Markdown(
            children = '### Total Sugar Production Estimate'
        ),
        
        dcc.Markdown(
            children = 'Latest ER of historical maximum ER is {}%'.format(round(sugaridxratio*100),2)
        )                
                
    ]),

    dcc.Graph(
        id = 'sugar production index',
        style={'margin-left':'200px'},
        figure = {
            'data':[
            {
                'x':indexlist0,
                'y':newsugaridx_f['2012'].tolist(),
                'name':'2012',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':newsugaridx_f['2013'].tolist(),
                'name':'2013',
                'mode':'lines',
                'line':{'width':3}         
            },                
            
            {
                'x':indexlist0,
                'y':newsugaridx_f['2014'].tolist(),
                'name':'2014',
                'mode':'lines',
                'line':{'width':3}         
            },                    

            {
                'x':indexlist0,
                'y':newsugaridx_f['2015'].tolist(),
                'name':'2015',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':newsugaridx_f['2016'].tolist(),
                'name':'2016',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':newsugaridx_f['2017'].tolist(),
                'name':'2017',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':newsugaridx_f['2018'].tolist(),
                'name':'2018',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':newsugaridx_f['2019'].tolist(),
                'name':'2019-estimate',
                'mode':'lines',
                'line':{'width':1.8,'dash':'dot','color':'rgb(0,0,0)'}         
            }
                    
        ],       
        'layout':{
            'title':'Tel quel Extraction Rate (with estimated 2019)',
            'showlegend':'false',
            'width':1500,
            'height':600,
            'xaxis':{
                'type':'category'
                    
            },
            'hovermode':'closest'
                
        }                    
                
                
        }

        
    ),



    dcc.Graph(
        id = 'sugar production',
        style={'margin-left':'200px'}
        
    ),
    
    
    html.Div(id='sugar production output'),

#=======================Raws/Sugar

    html.Br(),
    dcc.Markdown(children = draw_line),
 
    html.Div(id='raw-inter', style={'display': 'none'}),
 #   
    html.Div([

        dcc.Markdown(
            children = '### Raw Sugar Production Estimate'
        ),
        
        dcc.Markdown(
            children = 'Latest raws as percent of total sugar of historical maximum is {}%'.format(round(rawidxratio*100),2)
        )                
                
    ]),

    dcc.Graph(
        id = 'raw production index',
        style={'margin-left':'200px'},
        figure = {
            'data':[
            {
                'x':indexlist0,
                'y':newrawidx_f['2012'].tolist(),
                'name':'2012',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':newrawidx_f['2013'].tolist(),
                'name':'2013',
                'mode':'lines',
                'line':{'width':3}         
            },                
            
            {
                'x':indexlist0,
                'y':newrawidx_f['2014'].tolist(),
                'name':'2014',
                'mode':'lines',
                'line':{'width':3}         
            },                    

            {
                'x':indexlist0,
                'y':newrawidx_f['2015'].tolist(),
                'name':'2015',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':newrawidx_f['2016'].tolist(),
                'name':'2016',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':newrawidx_f['2017'].tolist(),
                'name':'2017',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':newrawidx_f['2018'].tolist(),
                'name':'2018',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':newrawidx_f['2019'].tolist(),
                'name':'2019-estimate',
                'mode':'lines',
                'line':{'width':1.8,'dash':'dot','color':'rgb(0,0,0)'}         
            }
                    
        ],       
        'layout':{
            'title':'Raws As Percent of Total Sugar (with estimated 2019)',
            'showlegend':'false',
            'width':1500,
            'height':600,
            'xaxis':{
                'type':'category'
                    
            },
            'hovermode':'closest'
                
        }                    
                
                
        }

        
    ),



    dcc.Graph(
        id = 'raw production',
        style={'margin-left':'200px'}
        
    ),
    
    
    html.Div(id='raw production output'),














#=======================
    html.Br(),
 

    dcc.Markdown(children = draw_line),    


    
    html.Div(

        dcc.Markdown(
            children = '### Other Sugar Production Estimate'
        )
    ),




#====================================
    html.Div([       
        
        dcc.Markdown(
            children = 'The average daily other sugar ratio/max during past 5 days is {}% (excluding 29th Dec-2nd Jan).'.format(avgratio_o)
        ),
        


        html.Div(id='slider-output-container_other'),
        
     
        
        
        
        dcc.Slider(
            id='other-slider',
            min=0,
            max=1,
            step=0.01,
            value=1,
            marks={
                0:'0%',
                0.25:'25%',
                0.5:'50%',
                0.75:'75%',
                1:'100%'

                
            },
              
        ),
        html.Div(id='slider-output-container2_other'),                
                
                
    ],
        style={
            'width':'45%'                  
        }  
    ),           



    



    html.Div([
        html.Div(
            dcc.Graph(
                id = 'others1'





            ),

            style = {'width':'33%','display':'inline-block'}
    
        ),
    

        html.Div(
            dcc.Graph(
                id = 'others2'



            ),
            style = {'width':'33%','display':'inline-block'}
    
        ),


         html.Div(
            dcc.Graph(
                id = 'others3'
        

            ),
            style = {'width':'33%','display':'inline-block'}
    
        )
    
    ]),
            
    dcc.Graph(
            
        id = 'others absolute',
        style={'margin-left':'200px'},    
            
    ),
  
#===============        
    html.Br(),
 

    dcc.Markdown(children = draw_line),    

           
            
    html.Div(

        dcc.Markdown(
            children = '###  White Sugar Production Estimate'
        )
    ),
    
    dcc.Graph(
            
        id = 'white production absolute',
        style={'margin-left':'200px'},    
            
    ),           
            

    html.Div(id='white output')

     

])







@app.callback(
    dash.dependencies.Output('basic-interactions', 'figure'),
    [dash.dependencies.Input('filter', 'value')])
def update_graph(datatype):

    return {

        'data':[
            {
                'x':indexlist0,
                'y':df[datatype]['2012'].tolist(),
                'name':'2012',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0[indexlist0.index('02-09'):indexlist0.index('02-15')],
                'y':df[datatype].loc['2017-02-09':'2017-02-14','2012'].tolist(),
                'showlegend':'False',
                'mode':'lines',
                'line':{'width':1.5,'color':'yellow'}         
            },

            {
                'x':indexlist0,
                'y':df[datatype]['2013'].tolist(),
                'name':'2013',
                'mode':'lines',
                'line':{'width':3}         
            },                
            
            {
                'x':indexlist0,
                'y':df[datatype]['2014'].tolist(),
                'name':'2014',
                'mode':'lines',
                'line':{'width':3}         
            },                    

            {
                'x':indexlist0,
                'y':df[datatype]['2015'].tolist(),
                'name':'2015',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':df[datatype]['2016'].tolist(),
                'name':'2016',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':df[datatype]['2017'].tolist(),
                'name':'2017',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':df[datatype]['2018'].tolist(),
                'name':'2018',
                'mode':'lines',
                'line':{'width':3}         
            },

            {
                'x':indexlist0,
                'y':df[datatype]['2019'].tolist(),
                'name':'2019',
                'mode':'lines',
                'line':{'width':3}         
            }
                    
        ],       
        'layout':{
            'title':'Seasonal Line Chart',
            'showlegend':'false',
            'width':1500,
            'height':600,
            'xaxis':{
                'type':'category'
                    
            },
            'hovermode':'closest'
                
        }    
                       
                
    }


@app.callback(
    dash.dependencies.Output('loading-states-table', 'data'),
    [dash.dependencies.Input('filter', 'value')])
def update_table(datatype):
    return showdf0[datatype].to_dict('records')


@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('crush-slider', 'value')])
def update_output(value):
    return 'Show {}% of maximum daily crush capacity.'.format(value*100)



#---- for sugar production


@app.callback(
    [dash.dependencies.Output('crush1', 'figure'),
     dash.dependencies.Output('crush2', 'figure'),
     dash.dependencies.Output('sugar-inter', 'children'),
     dash.dependencies.Output('sugar production output', 'children'),
     dash.dependencies.Output('sugar production', 'figure'),
     dash.dependencies.Output('raw production output', 'children'),
     dash.dependencies.Output('raw production', 'figure'),
     dash.dependencies.Output('slider-output-container2', 'children'),
     dash.dependencies.Output('sugar crush absolute', 'figure'),
     dash.dependencies.Output('others1', 'figure'),
     dash.dependencies.Output('others2', 'figure'),
     dash.dependencies.Output('others3', 'figure'),
     dash.dependencies.Output('slider-output-container2_other', 'children'),
     dash.dependencies.Output('others absolute', 'figure'),
     dash.dependencies.Output('white production absolute', 'figure'),
     dash.dependencies.Output('white output', 'children'),],
    [dash.dependencies.Input('crush-slider', 'value'),
     dash.dependencies.Input('button', 'n_clicks'),
     dash.dependencies.Input('input_crush','value'),
     dash.dependencies.Input('other-slider', 'value')])
            
def update_crush1_inter(value,n_clicks,inputcrush,value2):
    global clicknum,setcrush
    if n_clicks != clicknum:
        setcrush = (inputcrush)*1000000
        clicknum = n_clicks
        
    rationum = str(round(value,2)*100)+'% of Max capacity'
    rationum2 = 'Sugar Production (with estimated 2019) - under '+str(value*100)+'% of Max crush capacity scenario'
    rationum3 = 'Raw Sugar Production (with estimated 2019) - under '+str(value*100)+'% of Max crush capacity scenario'
    crushidx1_op = crushidx1.copy()
    crushidx1_op['RatioMax'] = crushidx1_op.loc[:,'2019']
    
    for i in range(crushidx1_op.loc[:,'2019'].isna().idxmax(),62):
        crushidx1_op.loc[i,'RatioMax'] = crushidx1_op.loc[i,'Max']*value    

    
    crushidx2_op = crushidx2.copy()
    crushidx2_op['RatioMax'] = crushidx2_op.loc[:,'2019']
    
    for i in datelist(crushidx2_op.loc[:,'2019'].isna().idxmax(),'2017-03-31'):
        crushidx2_op.loc[i,'RatioMax'] = crushidx2_op.loc[i,'Max']*value
 
    
    newcrush = df[0].copy()

    for i in range(0,32):
        newcrush.loc[newcrush.index.strftime("%Y-%m-%d").tolist()[30+i],'2019'] = crushidx1_op.loc[i+1,'RatioMax']
        
    
    for i in range(0,len(crushidx2_op.index.strftime("%Y-%m-%d").tolist())):
        newcrush.loc[crushidx2_op.index.strftime("%Y-%m-%d").tolist()[i],'2019'] = crushidx2_op.loc[crushidx2_op.index.strftime("%Y-%m-%d").tolist()[i],'RatioMax']
    
    newcrush['2019'] = newcrush['2019']* df[0].loc[:,'2019'].max(axis=0)
    
    newcrush.loc['2017-01-24','2019'] = newcrush.loc['2017-01-24','2019']*0.893
    newcrush.loc['2017-01-25','2019'] = newcrush.loc['2017-01-25','2019']*0.813
    newcrush.loc['2017-01-26','2019'] = newcrush.loc['2017-01-26','2019']*0.878
    



    totalsum0 = list()
    tsum = df[0].loc[:,'2019'].sum()
    for i in range(0,len(datelist(df[0].loc[:,'2019'].last_valid_index(),'2017-03-31'))):

        tdate = df[0].loc[:,'2019'].last_valid_index() + timedelta(days=i)
        
        hsum = newcrush.loc[(df[0].loc[:,'2019'].last_valid_index()+ timedelta(days=1)):(tdate- timedelta(days=1)),'2019'].sum()
        lsum = newcrush.loc[tdate,'2019'] *((datetime(2017,3,31) - tdate).days+1)*0.5
        totalsum = tsum+hsum+lsum
        totalsum0.append(totalsum)
    
    totalsum0 = np.array(totalsum0)-setcrush

    totalsum0=totalsum0[~np.isnan(totalsum0)]
    
    totalsum0 = np.absolute(totalsum0)
    #downdate = datelist(df[0].loc[:,'2019'].last_valid_index(),'2017-03-31')[np.where(totalsum0 < 0, totalsum0, -np.inf).argmax()]    
    downdate = datelist(df[0].loc[:,'2019'].last_valid_index(),'2017-03-31')[totalsum0.argmin()]

    downdaily = newcrush.loc[downdate,'2019']/(datetime(2017,3,31) - datetime.strptime(downdate,"%Y-%m-%d")).days
    downstart = newcrush.loc[downdate,'2019']

    for i in datelist((datetime.strptime(downdate,"%Y-%m-%d")+timedelta(days=1)).strftime("%Y-%m-%d"),'2017-03-31'):
        if ((downstart-downdaily) > 0) or ((downstart-downdaily) == 0):            
            downstart = downstart - downdaily
            newcrush.loc[i,'2019'] = downstart
        else:
            newcrush.loc[i,'2019'] = 0
    
    totalcrush = newcrush['2019'].sum()
    totalcrush=round(totalcrush/1000,2)

#***************    

    
    newcrushidx = newcrush.copy()

    newcrushidx.loc[:,'2019'] = newcrushidx.loc[:,'2019']/newcrushidx.loc[:,'2019'].max(axis=0)      


    for i in range(0,31):
        crushidx1_op.loc[i,'RatioMax'] = newcrushidx.loc[datelist('2016-12-01','2016-12-31')[i],'2019']
    
    for i in range(0,len(crushidx2.index)):
        crushidx2_op.loc[crushidx2.index[i],'RatioMax'] = newcrushidx.loc[crushidx2.index[i],'2019']
           
    
    newsugar = df[4].copy()

    newsugar['2019'] = newcrush['2019'] * newsugaridx['2019']/1000        
    
    totalsugar =  newsugar['2019'].sum()     
 
    totalsugar = round(totalsugar/1000,2)

    newraw = df[2].copy()
    newraw['2019'] = newsugar['2019'] * newrawidx['2019']
    totalraw = newraw['2019'].sum()
    totalraw = round(totalraw/1000,2)       


#oooooooooooooooooooooooooooooooooooooooooooooooooo
    rationum_o = str(round(value2,2)*100)+'% of Max capacity'
    rationum2_o = 'Other Sugar Production (with estimated 2019) - under '+str(value2*100)+'% of Max others produced capacity scenario'

    othersidx1_op = othersidx1.copy()
    othersidx1_op['RatioMax'] = othersidx1_op.loc[:,'2019']
    
    for i in range(othersidx1_op.loc[:,'2019'].isna().idxmax(),62):
        othersidx1_op.loc[i,'RatioMax'] = othersidx1_op.loc[i,'Max']*value2    

    
    othersidx2_op = othersidx2.copy()
    othersidx2_op['RatioMax'] = othersidx2_op.loc[:,'2019']
    
    for i in datelist(othersidx2_op.loc[:,'2019'].isna().idxmax(),'2017-03-31'):
        othersidx2_op.loc[i,'RatioMax'] = othersidx2_op.loc[i,'Max']*value2
        
    othersidx3_op = othersidx3.copy()
    othersidx3_op['RatioMax'] = othersidx3_op.loc[:,'2019']

    for i in datelist(othersidx3_op.loc[:,'2019'].isna().idxmax(),'2017-06-15'):
        othersidx3_op.loc[i,'RatioMax'] = othersidx3_op.loc[i,'Max']*value2        
 
    
    newothers = df[3].copy()

    for i in range(0,32):
        newothers.loc[newothers.index.strftime("%Y-%m-%d").tolist()[30+i],'2019'] = othersidx1_op.loc[i+1,'RatioMax']
        
    
    for i in range(0,len(othersidx2_op.index.strftime("%Y-%m-%d").tolist())):
        newothers.loc[othersidx2_op.index.strftime("%Y-%m-%d").tolist()[i],'2019'] = othersidx2_op.loc[othersidx2_op.index.strftime("%Y-%m-%d").tolist()[i],'RatioMax']

    for i in range(0,len(othersidx3_op.index.strftime("%Y-%m-%d").tolist())):
        newothers.loc[othersidx3_op.index.strftime("%Y-%m-%d").tolist()[i],'2019'] = othersidx3_op.loc[othersidx3_op.index.strftime("%Y-%m-%d").tolist()[i],'RatioMax']

    
    newothers['2019'] = newothers['2019']* df[3].loc[:,'2019'].max(axis=0)
 
    

    
    totalothers = newothers.loc['2016-12-1':'2017-3-31','2019'].sum()
    totalothers=round(totalothers/1000,2)

    newwhite = df[1].copy()
    
    for i in newothers.index.strftime("%Y-%m-%d").tolist():
        newwhite.loc[i,'2019'] = newsugar.loc[i,'2019'] - newraw.loc[i,'2019'] - newothers.loc[i,'2019']

    totalwhite = newwhite.loc['2016-12-1':'2017-3-31','2019'].sum()
    totalwhite=round(totalwhite/1000,2)    
    
    
    return( 
        {
            'data':[
                    {
                        'x':indexcrush1,
                        'y':crushidx1_op['2012'].tolist(),
                        'name':'2012',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexcrush1,
                        'y':crushidx1_op['2013'].tolist(),
                        'name':'2013',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                
                
                    {
                        'x':indexcrush1,
                        'y':crushidx1_op['2014'].tolist(),
                        'name':'2014',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                    
        
                    {
                        'x':indexcrush1,
                        'y':crushidx1_op['2015'].tolist(),
                        'name':'2015',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush1,
                        'y':crushidx1_op['2016'].tolist(),
                        'name':'2016',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush1,
                        'y':crushidx1_op['2017'].tolist(),
                        'name':'2017',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexcrush1,
                        'y':crushidx1_op['2018'].tolist(),
                        'name':'2018',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush1,
                        'y':crushidx1_op['2019'].tolist(),
                        'name':'2019',
                        'mode':'lines',
                        'line':{
                        'width':3
                            
                        }         
                    },
        
                    {
                        'x':indexcrush1,
                        'y':crushidx1_op['Max'].tolist(),
                        'name':'Max',
                        'mode':'lines',
                        'line':{
                                'width':1.5,
                                'dash':'dash',
                                'color':'rgb(0,0,0)'
                                
                        },
                    },    
                    {
                        'x':indexcrush1,
                        'y':crushidx1_op['RatioMax'].tolist(),
                        'name':rationum,
                        'mode':'lines',
                        'line':{
                                'width':1.5,
                                'dash':'dot',
                                'color':'rgb(255,0,0)'
                                
                        }                       
                    
                    }                    
        
        
            ],       
            'layout':{
                'title':'Crush - 1st Section - till 31st Dec',
                'showlegend':'false',
                        
                'height':600,
                'xaxis':{
                    'type':'category'
                            
                },
            'hovermode':'closest'
            },
                
     
        },    
       
        {
            'data':[
                    {
                        'x':indexcrush2,
                        'y':crushidx2_op['2012'].tolist(),
                        'name':'2012',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexcrush2,
                        'y':crushidx2_op['2013'].tolist(),
                        'name':'2013',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                
            
                    {
                        'x':indexcrush2,
                        'y':crushidx2_op['2014'].tolist(),
                        'name':'2014',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                    
    
                    {
                        'x':indexcrush2,
                        'y':crushidx2_op['2015'].tolist(),
                        'name':'2015',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush2,
                        'y':crushidx2_op['2016'].tolist(),
                        'name':'2016',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush2,
                        'y':crushidx2_op['2017'].tolist(),
                        'name':'2017',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexcrush2,
                        'y':crushidx2_op['2018'].tolist(),
                        'name':'2018',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush2,
                        'y':crushidx2_op['2019'].tolist(),
                        'name':'2019',
                        'mode':'lines',
                        'line':{
                        'width':3
                            
                        }         
                    },
    
                    {
                        'x':indexcrush2,
                        'y':crushidx2_op['Max'].tolist(),
                        'name':'Max',
                        'mode':'lines',
                        'line':{
                                'width':1.5,
                                'dash':'dash',
                                'color':'rgb(0,0,0)'
                            
                        },
                    },    
                    {
                        'x':indexcrush2,
                        'y':crushidx2_op['RatioMax'].tolist(),
                        'name':rationum,
                        'mode':'lines',
                        'line':{
                                'width':1.5,
                                'dash':'dot',
                                'color':'rgb(255,0,0)'
                            
                        }                       
                    
                    }                    
        
        
            ],       
            'layout':{
                'title':'Crush - 2nd Section - 1st Jan to 31st Mar',
                'showlegend':'false',
                        
                'height':600,
                'xaxis':{
                    'type':'category'
                            
                },
            'hovermode':'closest'
            },
                
     
        },        

        newsugar.to_json(date_format='iso', orient='split'),
        'Totally {}kmt tel quel of sugar would be produced till the end of March.'.format(totalsugar),

        {
            'data':[
                    {
                        'x':indexlist0,
                        'y':newsugar['2012'].tolist(),
                        'name':'2012',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexlist0,
                        'y':newsugar['2013'].tolist(),
                        'name':'2013',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                
                
                    {
                        'x':indexlist0,
                        'y':newsugar['2014'].tolist(),
                        'name':'2014',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                    
    
                    {
                        'x':indexlist0,
                        'y':newsugar['2015'].tolist(),
                        'name':'2015',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newsugar['2016'].tolist(),
                        'name':'2016',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newsugar['2017'].tolist(),
                        'name':'2017',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexlist0,
                        'y':newsugar['2018'].tolist(),
                        'name':'2018',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newsugar['2019'].tolist(),
                        'name':'2019-estimate',
                        'mode':'lines',
                        'line':{'width':1.8,'dash':'dot','color':'rgb(0,0,0)'}         
                    }        
        
            ],       
            'layout':{
                'title':rationum2,
                'showlegend':'false',
                        
                'height':600,
                'xaxis':{
                    'type':'category'
                            
                },
            'hovermode':'closest'
            },
                
     
        }, 
                
                
        'Totally {}kmt of raw sugar would be produced till the end of March.'.format(totalraw),

        {
            'data':[
                    {
                        'x':indexlist0,
                        'y':newraw['2012'].tolist(),
                        'name':'2012',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexlist0,
                        'y':newraw['2013'].tolist(),
                        'name':'2013',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                
                
                    {
                        'x':indexlist0,
                        'y':newraw['2014'].tolist(),
                        'name':'2014',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                    
    
                    {
                        'x':indexlist0,
                        'y':newraw['2015'].tolist(),
                        'name':'2015',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newraw['2016'].tolist(),
                        'name':'2016',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newraw['2017'].tolist(),
                        'name':'2017',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexlist0,
                        'y':newraw['2018'].tolist(),
                        'name':'2018',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newraw['2019'].tolist(),
                        'name':'2019-estimate',
                        'mode':'lines',
                        'line':{'width':1.8,'dash':'dot','color':'rgb(0,0,0)'}         
                    }        
        
            ],       
            'layout':{
                'title':rationum3,
                'showlegend':'false',
                        
                'height':600,
                'xaxis':{
                    'type':'category'
                            
                },
            'hovermode':'closest'
            },
                
     
        },
        'Crush would start to decrease from {}. Totally {}kmt of cane would be crushed till the end of March.'.format(downdate[5:],totalcrush),
        
        {
            'data':[
                    {
                        'x':indexlist0,
                        'y':newcrush['2012'].tolist(),
                        'name':'2012',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexlist0,
                        'y':newcrush['2013'].tolist(),
                        'name':'2013',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                
                
                    {
                        'x':indexlist0,
                        'y':newcrush['2014'].tolist(),
                        'name':'2014',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                    
        
                    {
                        'x':indexlist0,
                        'y':newcrush['2015'].tolist(),
                        'name':'2015',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newcrush['2016'].tolist(),
                        'name':'2016',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newcrush['2017'].tolist(),
                        'name':'2017',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexlist0,
                        'y':newcrush['2018'].tolist(),
                        'name':'2018',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newcrush['2019'].tolist(),
                        'name':'2019-estimate',
                        'mode':'lines',
                        'line':{'width':1.5,'dash':'dot','color':'rgb(0,0,0)'}       
                    }
        
                          
        
            ],       
            'layout':{
                'title':'Cane Crush - with estimation',
                'showlegend':'false',
                        
                'height':600,
                'xaxis':{
                    'type':'category'
                            
                },
            'hovermode':'closest'
            }
                
     
        },
        {
            'data':[
                    {
                        'x':indexcrush1,
                        'y':othersidx1_op['2012'].tolist(),
                        'name':'2012',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexcrush1,
                        'y':othersidx1_op['2013'].tolist(),
                        'name':'2013',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                
                
                    {
                        'x':indexcrush1,
                        'y':othersidx1_op['2014'].tolist(),
                        'name':'2014',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                    
        
                    {
                        'x':indexcrush1,
                        'y':othersidx1_op['2015'].tolist(),
                        'name':'2015',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush1,
                        'y':othersidx1_op['2016'].tolist(),
                        'name':'2016',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush1,
                        'y':othersidx1_op['2017'].tolist(),
                        'name':'2017',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexcrush1,
                        'y':othersidx1_op['2018'].tolist(),
                        'name':'2018',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush1,
                        'y':othersidx1_op['2019'].tolist(),
                        'name':'2019',
                        'mode':'lines',
                        'line':{
                        'width':3
                            
                        }         
                    },
        
                    {
                        'x':indexcrush1,
                        'y':othersidx1_op['Max'].tolist(),
                        'name':'Max',
                        'mode':'lines',
                        'line':{
                                'width':1.5,
                                'dash':'dash',
                                'color':'rgb(0,0,0)'
                                
                        },
                    },    
                    {
                        'x':indexcrush1,
                        'y':othersidx1_op['RatioMax'].tolist(),
                        'name':rationum_o,
                        'mode':'lines',
                        'line':{
                                'width':1.5,
                                'dash':'dot',
                                'color':'rgb(255,0,0)'
                                
                        }                       
                    
                    }                    
        
        
            ],       
            'layout':{
                'title':'Others Index - 1st Section - till 31st Dec',
                'showlegend':'false',
                        
                'height':600,
                'xaxis':{
                    'type':'category'
                            
                },
            'hovermode':'closest'
            },
                
     
        },                


        {
            'data':[
                    {
                        'x':indexcrush2,
                        'y':othersidx2_op['2012'].tolist(),
                        'name':'2012',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexcrush2,
                        'y':othersidx2_op['2013'].tolist(),
                        'name':'2013',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                
                
                    {
                        'x':indexcrush2,
                        'y':othersidx2_op['2014'].tolist(),
                        'name':'2014',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                    
        
                    {
                        'x':indexcrush2,
                        'y':othersidx2_op['2015'].tolist(),
                        'name':'2015',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush2,
                        'y':othersidx2_op['2016'].tolist(),
                        'name':'2016',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush2,
                        'y':othersidx2_op['2017'].tolist(),
                        'name':'2017',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexcrush2,
                        'y':othersidx2_op['2018'].tolist(),
                        'name':'2018',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush2,
                        'y':othersidx2_op['2019'].tolist(),
                        'name':'2019',
                        'mode':'lines',
                        'line':{
                        'width':3
                            
                        }         
                    },
        
                    {
                        'x':indexcrush2,
                        'y':othersidx2_op['Max'].tolist(),
                        'name':'Max',
                        'mode':'lines',
                        'line':{
                                'width':1.5,
                                'dash':'dash',
                                'color':'rgb(0,0,0)'
                                
                        },
                    },    
                    {
                        'x':indexcrush2,
                        'y':othersidx2_op['RatioMax'].tolist(),
                        'name':rationum_o,
                        'mode':'lines',
                        'line':{
                                'width':1.5,
                                'dash':'dot',
                                'color':'rgb(255,0,0)'
                                
                        }                       
                    
                    }                    
        
        
            ],       
            'layout':{
                'title':'Others Index - 2nd Section - 1st Jan to 31st Mar',
                'showlegend':'false',
                        
                'height':600,
                'xaxis':{
                    'type':'category'
                            
                },
            'hovermode':'closest'
            },
                
     
        },                


        {
            'data':[
                    {
                        'x':indexcrush3,
                        'y':othersidx3_op['2012'].tolist(),
                        'name':'2012',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexcrush3,
                        'y':othersidx3_op['2013'].tolist(),
                        'name':'2013',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                
                
                    {
                        'x':indexcrush3,
                        'y':othersidx3_op['2014'].tolist(),
                        'name':'2014',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                    
        
                    {
                        'x':indexcrush3,
                        'y':othersidx3_op['2015'].tolist(),
                        'name':'2015',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush3,
                        'y':othersidx3_op['2016'].tolist(),
                        'name':'2016',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush3,
                        'y':othersidx3_op['2017'].tolist(),
                        'name':'2017',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexcrush3,
                        'y':othersidx3_op['2018'].tolist(),
                        'name':'2018',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexcrush3,
                        'y':othersidx3_op['2019'].tolist(),
                        'name':'2019',
                        'mode':'lines',
                        'line':{
                        'width':3
                            
                        }         
                    },
        
                    {
                        'x':indexcrush3,
                        'y':othersidx3_op['Max'].tolist(),
                        'name':'Max',
                        'mode':'lines',
                        'line':{
                                'width':1.5,
                                'dash':'dash',
                                'color':'rgb(0,0,0)'
                                
                        },
                    },    
                    {
                        'x':indexcrush3,
                        'y':othersidx3_op['RatioMax'].tolist(),
                        'name':rationum_o,
                        'mode':'lines',
                        'line':{
                                'width':1.5,
                                'dash':'dot',
                                'color':'rgb(255,0,0)'
                                
                        }                       
                    
                    }                    
        
        
            ],       
            'layout':{
                'title':'Others Index - 3rd Section - After 1st Apr',
                'showlegend':'false',
                        
                'height':600,
                'xaxis':{
                    'type':'category'
                            
                },
            'hovermode':'closest'
            },
                
     
        },


        'We expect totally {}kmt of other sugar would be produced till the end of Mar, under {}% of max daily capacity.'.format(totalothers,round(value2,2)*100),
        
        
        {
            'data':[
                    {
                        'x':indexlist0,
                        'y':newothers['2012'].tolist(),
                        'name':'2012',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexlist0,
                        'y':newothers['2013'].tolist(),
                        'name':'2013',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                
                
                    {
                        'x':indexlist0,
                        'y':newothers['2014'].tolist(),
                        'name':'2014',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                    
        
                    {
                        'x':indexlist0,
                        'y':newothers['2015'].tolist(),
                        'name':'2015',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newothers['2016'].tolist(),
                        'name':'2016',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newothers['2017'].tolist(),
                        'name':'2017',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexlist0,
                        'y':newothers['2018'].tolist(),
                        'name':'2018',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newothers['2019'].tolist(),
                        'name':'2019-estimate',
                        'mode':'lines',
                        'line':{'width':1.5,'dash':'dot','color':'rgb(0,0,0)'}       
                    }
        
                          
        
            ],       
            'layout':{
                'title':rationum2_o,
                'showlegend':'false',
                        
                'height':600,
                'xaxis':{
                    'type':'category'
                            
                },
            'hovermode':'closest'
            }
                
     
        },

        {
            'data':[
                    {
                        'x':indexlist0,
                        'y':newwhite['2012'].tolist(),
                        'name':'2012',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexlist0,
                        'y':newwhite['2013'].tolist(),
                        'name':'2013',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                
                
                    {
                        'x':indexlist0,
                        'y':newwhite['2014'].tolist(),
                        'name':'2014',
                        'mode':'lines',
                        'line':{'width':3}         
                    },                    
        
                    {
                        'x':indexlist0,
                        'y':newwhite['2015'].tolist(),
                        'name':'2015',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newwhite['2016'].tolist(),
                        'name':'2016',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newwhite['2017'].tolist(),
                        'name':'2017',
                        'mode':'lines',
                        'line':{'width':3}         
                    },
    
                    {
                        'x':indexlist0,
                        'y':newwhite['2018'].tolist(),
                        'name':'2018',
                        'mode':'lines',
                        'line':{'width':3}         
                    },

                    {
                        'x':indexlist0,
                        'y':newwhite['2019'].tolist(),
                        'name':'2019-estimate',
                        'mode':'lines',
                        'line':{'width':1.5,'dash':'dot','color':'rgb(0,0,0)'}       
                    }
        
                          
        
            ],       
            'layout':{
                'title':'Whites',
                'showlegend':'false',
                        
                'height':600,
                'xaxis':{
                    'type':'category'
                            
                },
            'hovermode':'closest'
            }
                
     
        },

        'Totally {}kmt of white sugar would be produced till the end of March.'.format(totalwhite)                   
                
                
    )


















if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    

    
    
