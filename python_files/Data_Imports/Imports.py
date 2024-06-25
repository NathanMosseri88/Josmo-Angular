import sqlalchemy
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
import crayons
import time
import getpass
import Database_Modules
from Database_Modules import print_color, engine_setup, run_sql_scripts, create_folder, get_proper_engine, error_handler, map_module_setting


# @error_handler
def import_data_to_sql(engine, project_name, data_folder, report_type):
    scripts = []
    if report_type == 'inventory_data':
        inventory_data_file = f'{data_folder}\\inventory_data.csv'
        df = pd.read_csv(inventory_data_file, low_memory=False,
             converters={'PROD_CD': str.strip,
                         'PROD_CLR': str.strip,
                         'CLASS_CD': str.strip,
                         'SZ_RUN': str.strip,
                         'IMAGE': str.strip,
                         'UPC_CD': str.strip
                         })
        df['UPC_CD'] = df['UPC_CD'].apply(lambda x: x + str((10 - (((int(x[0]) + int(x[2]) + int(x[4]) + int(
            x[6]) + int(x[8]) + int(x[10])) * 3 + (int(x[1]) + int(x[3]) + int(x[5]) + int(x[7]) + int(
            x[9]))) % 10)) % 10) if x != "" and "." not in x else x)
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("œ", ".5")
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("œ", ".5")
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("½", ".5")
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("½", ".5")
        df['PROD_CD'] = df['PROD_CD'].apply(lambda x: x.upper())
        # df['PROD_CD'] = df['PROD_CD'].apply(lambda x: x.strip())
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)


        table_name = 'inventory_data'
        engine.connect().execute(text(f'drop table if exists {table_name};'))
        sql_types = Database_Modules.Get_SQL_Types(df).data_types  ## GET THE COLUMN TYPES TO INPORT INTO SQL ALCHEMY ###
        Database_Modules.Change_Sql_Column_Types(engine=engine, Project_name=project_name, Table_Name=table_name,DataTypes=sql_types, DataFrame=df)
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=project_name, chunksize=1000, dtype=sql_types)


        scripts.append(f'Alter Table inventory_data add primary key(PROD_CD, PROD_CLR, Size_Breakdown, UPC_CD, NUMBER);')
        scripts.append(f'create index inventory_data on inventory_data(PROD_CD, PROD_CLR, Size_Breakdown, UPC_CD);')
        scripts.append(f'create index prod_cd_clr_size on inventory_data(PROD_CD, PROD_CLR, Size_Breakdown);')
        scripts.append(f'create index class_cd_sz_run on inventory_data(class_cd, SZ_RUN);')




        print_color(f'Inventory Data Imported')

    elif report_type == 'po_data_by_size':
        po_data_file = f'{data_folder}\\po_data_by_size.csv'
        df = pd.read_csv(po_data_file, low_memory=False,
                    converters={'prod_cd': str.strip,
                                'prod_clr': str.strip,
                                'Class_cd': str.strip,
                                'INV_SZ': str.strip,
                                'run_cd': str.strip,
                                'IMAGE_NM': str.strip,
                                'UPC_CD': str.strip
                                })
        df['UPC_CD'] = df['UPC_CD'].apply(lambda x: x + str((10 - (((int(x[0]) + int(x[2]) + int(x[4]) + int(
            x[6]) + int(x[8]) + int(x[10])) * 3 + (int(x[1]) + int(x[3]) + int(x[5]) + int(x[7]) + int(
            x[9]))) % 10)) % 10) if x != "" and "." not in x else x)

        df['EST_DT'] = pd.to_datetime(df['EST_DT'])
        df['EST_DT'] = df['EST_DT'].dt.strftime('%Y-%m-%d')

        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("œ", ".5")
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("œ", ".5")
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("½", ".5")
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("½", ".5")

        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        table_name = 'po_data_by_size'
        engine.connect().execute(text(f'drop table if exists {table_name};'))
        sql_types = Database_Modules.Get_SQL_Types(df).data_types  ## GET THE COLUMN TYPES TO INPORT INTO SQL ALCHEMY ###
        Database_Modules.Change_Sql_Column_Types(engine=engine, Project_name=project_name, Table_Name=table_name, DataTypes=sql_types, DataFrame=df)
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=project_name, chunksize=1000, dtype=sql_types)


        print_color(f'PO Data By Size Imported')

    elif report_type == 'case_breakdown':
        case_breakdown_file = f'{data_folder}\\case_breakdown.csv'
        df = pd.read_csv(case_breakdown_file, low_memory=False,
                                    converters={'class_cd': str.strip,
                                                'inv_sz': str.strip}
                                     )
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("œ", ".5")
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("œ", ".5")
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("½", ".5")
        df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("½", ".5")

        df['Size_Run'] = df['Size_Run'].str.replace("œ", ".5")
        df['Size_Run'] = df['Size_Run'].str.replace("œ", ".5")
        df['Size_Run'] = df['Size_Run'].str.replace("½", ".5")
        df['Size_Run'] = df['Size_Run'].str.replace("½", ".5")

        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        table_name = 'case_breakdown'
        engine.connect().execute(text(f'drop table if exists {table_name};'))
        sql_types = Database_Modules.Get_SQL_Types(df).data_types  ## GET THE COLUMN TYPES TO INPORT INTO SQL ALCHEMY ###
        Database_Modules.Change_Sql_Column_Types(engine=engine, Project_name=project_name, Table_Name=table_name, DataTypes=sql_types,DataFrame=df)
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=project_name, chunksize=1000, dtype=sql_types)
        print_color(f'Case Breakdown Imported')


        scripts.append(f'alter table case_breakdown add primary key(class_cd,inv_sz );')
        scripts.append(f'create index class_cd on case_breakdown(class_cd);')

    elif report_type == 'style_master':
        data_file = f'{data_folder}\\{report_type}.csv'
        df = pd.read_csv(data_file, low_memory=False)
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df['Size'] = df['Size'].str.replace("œ", ".5").str.replace("œ", ".5").str.replace("½", ".5").str.replace("½", ".5")
        df['Brand_Lookup'] = None
        table_name = report_type.lower().replace(" ", "_")
        engine.connect().execute(text(f'drop table if exists {table_name};'))
        sql_types = Database_Modules.Get_SQL_Types(
            df).data_types  ## GET THE COLUMN TYPES TO INPORT INTO SQL ALCHEMY ###
        # Database_Modules.Change_Sql_Column_Types(engine=engine, Project_name=project_name, Table_Name=table_name,DataTypes=sql_types, DataFrame=df)
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=project_name, chunksize=1000,
                  dtype=sql_types)
        print_color(f'{report_type.replace("_", " ").upper()} Imported', color='b')

    elif report_type == 'brand_reference':
        data_file = f'{data_folder}\\{report_type}.csv'
        df = pd.read_csv(data_file)

        df['index'] = df.index

        table_name = report_type.lower().replace(" ","_")
        engine.connect().execute(text(f'drop table if exists {table_name};'))
        sql_types = Database_Modules.Get_SQL_Types(df).data_types  ## GET THE COLUMN TYPES TO INPORT INTO SQL ALCHEMY ###
        # Database_Modules.Change_Sql_Column_Types(engine=engine, Project_name=project_name, Table_Name=table_name,DataTypes=sql_types, DataFrame=df)
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=project_name, chunksize=1000, dtype=sql_types)
        print_color(f'{report_type.replace("_"," ").upper()} Imported', color='b')

    else:
        data_file =  f'{data_folder}\\{report_type}.csv'
        df = pd.read_csv(data_file, low_memory=True)
        df = df.apply(lambda x: x.str.strip().str.replace("œ", ".5").str.replace("½", ".5") if x.dtype == "object" else x)

        # df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("œ", ".5")
        # df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("œ", ".5")
        # df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("½", ".5")
        # df['Size_Breakdown'] = df['Size_Breakdown'].str.replace("½", ".5")

        table_name = report_type.lower().replace(" ","_")
        engine.connect().execute(text(f'drop table if exists {table_name};'))
        sql_types = Database_Modules.Get_SQL_Types(df).data_types  ## GET THE COLUMN TYPES TO INPORT INTO SQL ALCHEMY ###
        # Database_Modules.Change_Sql_Column_Types(engine=engine, Project_name=project_name, Table_Name=table_name,DataTypes=sql_types, DataFrame=df)
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=project_name, chunksize=1000, dtype=sql_types)
        print_color(f'{report_type.replace("_"," ").upper()} Imported', color='b')




    run_sql_scripts(scripts=scripts, engine=engine)

    map_module_setting(engine=engine, category='import files', module='import_data_to_sql', sub_module='',
                       data_type=report_type)

