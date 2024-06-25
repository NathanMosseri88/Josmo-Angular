##INSTRUCTION-START##
##INSTRUCTION-END##

##COMMENT-START##
##COMMENT-END##

##FILE-START##
##FILE-END##

##EXIT##

import requests
import json
import sys
import csv
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import text
from lunarcalendar.festival import festivals
from datetime import datetime, date, time, timedelta
from Database_Modules import print_color, map_module_setting, run_sql_scripts



def Calendar(engine, schema):


    dy = int(datetime.now().strftime('%Y'))-4
    dy1 = int(datetime.now().strftime('%Y')) + 6

    df = pd.DataFrame()
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    a6 = []
    x1 = 0
    x2 = -1
    for fest in festivals:
        for x in range(dy, dy1):

            a = fest.get_lang('en'), fest(x)
            if a[0]=='Chinese New Year':
                x1 += 1
                x2 += 1
                a1 += [a[0]]
                a2 += [a[1]]
                a3 += [a[1] + timedelta(days=42)]
                a4 += [a[1]+ timedelta(days=43)]
                a5 += [x1]
                a6 += [x2]


    df['Holiday'] = a1
    df['Date'] = a2

    df1['Date'] = a2
    df1['CNY'] = a2
    df1['END CNY'] = a3
    df1['NEXT CNY'] = a4
    df1['INDEX'] = a5

    df2['NEW CNY'] = a2
    df2['INDEX'] = a6

    df1 = df1.merge(df2, on='INDEX', how='left')

    with engine.connect() as con:
        con.execute(text('drop table if exists cny'))

    df.to_sql(name='cny', con=engine, if_exists='replace', index=False, schema=schema,
                                     chunksize=1000, dtype={'Holiday': sqlalchemy.types.VARCHAR(35),
                                                            'Date': sqlalchemy.types.DATE()})

    start = datetime.strptime("2017-01-01", "%Y-%m-%d").date()
    end = (datetime.today()+ timedelta(days=18*365/12)).date()

    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]


    def find_quarter(x):
        return "Q"+str((x.month - 1) // 3 + 1)

    calendar_table = pd.DataFrame()
    calendar_table['Date'] = date_generated
    calendar_table['Year'] = [x.strftime('%Y') for x in date_generated]
    calendar_table['Month'] = [x.strftime('%m') for x in date_generated]
    calendar_table['Month_Name'] = [y.strftime('%B') for y in date_generated]
    calendar_table['Day_of_Month'] = [x.strftime("%d") for x in date_generated]
    calendar_table['Day_Name'] = [x.strftime("%A") for x in date_generated]
    calendar_table['Quarter'] = [find_quarter(x) for x in date_generated]
    calendar_table['Week'] = [x.strftime('%U') for x in date_generated]
    calendar_table['Year_Month'] = [str(x)[:7] for x in date_generated]

    calendar_table = calendar_table.merge(df1[['Date','CNY']], on='Date', how='left')
    calendar_table = calendar_table.merge(df1[['Date','END CNY', 'INDEX']], left_on='Date', right_on='END CNY', how='left')
    calendar_table = calendar_table.merge(df1[['NEXT CNY','NEW CNY']], left_on='Date_x',  right_on='NEXT CNY', how='left')
    calendar_table['CNY'] = calendar_table['CNY'].combine_first(calendar_table['Date_y'])
    calendar_table['CNY'] = calendar_table['CNY'].combine_first(calendar_table['NEW CNY'])
    calendar_table['CNY'] = calendar_table['CNY'].ffill(axis=0)

    calendar_table = calendar_table[['Date_x', 'Year', 'Month', 'Month_Name', 'Day_of_Month', 'Day_Name','Quarter', 'Week', 'Year_Month', 'CNY']]
    calendar_table.columns = ['Date', 'Year', 'Month', 'Month_Name', 'Day_of_Month', 'Day_Name','Quarter', 'Week', 'Year_Month', 'CNY']
    calendar_table['CNY'] = calendar_table['CNY'].replace(np.nan, "0000-00-00")

    with engine.connect() as con:
        con.execute(text('drop table if exists calendar;'))
    calendar_table.to_sql(name = 'calendar',con = engine, if_exists='replace', index=False, schema=schema,
                          dtype={'Date': sqlalchemy.types.DATE,
                                'Day_of_Month': sqlalchemy.types.INTEGER(),
                                'Week':sqlalchemy.types.INTEGER(),
                                'Month':sqlalchemy.types.INTEGER(),
                                'Month_Name':sqlalchemy.types.VARCHAR(20),
                                'Day_Name':sqlalchemy.types.VARCHAR(20),
                                'Quarter':sqlalchemy.types.VARCHAR(10),
                                'Year':sqlalchemy.types.INTEGER(),
                                'Year_Month':sqlalchemy.types.VARCHAR(50),
                                'CNY': sqlalchemy.types.DATE})


    scripts = []
    scripts.append(f'alter table calendar ADD PRIMARY KEY(`Date`);')
    scripts.append(f'alter table calendar add column Day_of_Week int after day_of_month, add column Year_week int;')
    scripts.append(f'update calendar set Day_of_Week =  DAYOFWEEK(date);')
    # scripts.append(f'''update calendar A, (SELECT date, dense_rank() over (partition by Day_of_Week order by date) as week_rank from calendar) B
    #     set A.Year_week = B.week_rank where A.date = B.date;''')

    run_sql_scripts(engine=engine, scripts=scripts)

    print_color('Calendar EXECUTED', color='g')

    map_module_setting(engine=engine, category='calendar', module='calendar', sub_module='', data_type='calendar setup')

# Calendar()
