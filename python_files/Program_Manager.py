import sys
import pandas as pd
import getpass
import pyodbc
from sqlalchemy import create_engine, text
import Database_Modules
from Database_Modules import print_color, engine_setup, run_sql_scripts, create_folder, \
    get_proper_engine, error_handler, computer_dict_method, map_module_setting, ProgramCredentials
from Data_Exports.Calendar_Table import Calendar
from Data_Exports.Extract_Data import recruit_color_codes, recruit_size_breakdown, recruit_size_packs, recruit_case_breakdown, \
    recruit_po_by_size_data, recruit_inventory_data, export_data_sets, recruit_customers,recruit_images, \
    recruit_vendors, recruit_warehouses, setup_temporary_tables, recruit_style_master, recruit_purchase_order_data, \
    recruit_received_purchase_order_data, recruit_open_order_data, import_google_sheet_data, set_primary_keys, set_indexes
from Data_Imports.Imports import import_data_to_sql
from Data_Imports.generate_url_links import get_url_links, copy_jpg_png_images, recruit_image_files, get_pavo_images
from API.PowerBI import run_pbi_integration
from Diagnostic.data_diagnostic import run_diagnostic
from API.Pavo import PavoAPIClass


def modules_mapping(project_name=None, engine=None):
    scripts = []
    scripts.append(f'''CREATE TABLE if not exists `modules_performance` (
   `id` int NOT NULL AUTO_INCREMENT,
   `date` date DEFAULT NULL,
   `datetime` datetime DEFAULT NULL,
   `category` varchar(25) NOT NULL,
   `module` varchar(25) NOT NULL,
   `sub_module` varchar(50) NOT NULL,
   `data_type` varchar(50) NOT NULL,
   `executed` tinyint(1) DEFAULT NULL,
   PRIMARY KEY (`id`),
   KEY `module_map` (`category`,`module`,`sub_module`,`data_type`)
 ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci''')

    run_sql_scripts(engine=engine, scripts=scripts)

    modules_list = [
        {'category': 'project_setup', 'module': 'create_database', 'sub_module': '', 'data_type': 'project setup', 'executed': True, 'break_updated': True},
        {'category': 'calendar', 'module': 'calendar', 'sub_module': '', 'data_type': 'calendar setup','executed': True, 'break_updated': True},

        {'category': 'images', 'module': 'copy_jpg_png_images', 'sub_module': '', 'data_type': 'move images', 'executed': True, 'break_updated': False},
        {'category': 'images', 'module': 'get_url_links', 'sub_module': '', 'data_type': 'get url links', 'executed': True, 'break_updated': False},


        {'category': 'recruit files', 'module': 'recruit_customers', 'sub_module': '', 'data_type': 'customers','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_vendors', 'sub_module': '', 'data_type': 'vendors','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_warehouses', 'sub_module': '', 'data_type': 'warehouses','executed': True, 'break_updated': True},
        # {'category': 'recruit files', 'module': 'setup_temporary_tables', 'sub_module': '', 'data_type': 'temoprary tables','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_style_master', 'sub_module': '', 'data_type': 'style master','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_purchase_order_data', 'sub_module': '', 'data_type': 'purchase orders','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_received_purchase_order_data', 'sub_module': '', 'data_type': 'received purchase orders','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_open_order_data', 'sub_module': '', 'data_type': 'open orders','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_color_codes', 'sub_module': '', 'data_type': 'color codes','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_size_breakdown', 'sub_module': '', 'data_type': 'size breakdown','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_size_packs', 'sub_module': '', 'data_type': 'size packs','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_case_breakdown', 'sub_module': '', 'data_type': 'case breakdown','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_po_by_size_data', 'sub_module': '', 'data_type': 'po by size','executed': True, 'break_updated': True},
        {'category': 'recruit files', 'module': 'recruit_inventory_data', 'sub_module': '', 'data_type': 'inventory data','executed': True, 'break_updated': True},

        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'brand_reference','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'inventory_data','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'po_data_by_size','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'case_breakdown','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'color_codes','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'size_breakdown','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'size_pack','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'po_data','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'received_po_data','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'open_order_data','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'style_master','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'warehouses','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'customers','executed': True, 'break_updated': True},
        {'category': 'import files', 'module': 'import_data_to_sql', 'sub_module': '', 'data_type': 'vendors','executed': True, 'break_updated': True},

        {'category': 'sql setup', 'module': 'set_primary_keys', 'sub_module': '', 'data_type': 'set primary keys', 'executed': True, 'break_updated': True},
        {'category': 'sql setup', 'module': 'set_indexes', 'sub_module': '', 'data_type': 'set indexes', 'executed': True, 'break_updated': True},
        {'category': 'sql setup', 'module': 'set_brand_mapping', 'sub_module': '', 'data_type': 'set brand mapping', 'executed': True, 'break_updated': True},


        {'category': 'sql logic', 'module': 'executeScriptsFromFile', 'sub_module': '', 'data_type': 'Data Setup Logic.sql', 'executed': True, 'break_updated': True},
        {'category': 'sql logic', 'module': 'executeScriptsFromFile', 'sub_module': '', 'data_type': 'Comparative_Style_Logic.sql', 'executed': True, 'break_updated': True},
        {'category': 'sql logic', 'module': 'executeScriptsFromFile', 'sub_module': '', 'data_type': 'Container_Logic 2.sql', 'executed': True, 'break_updated': True},

        {'category': 'powerbi', 'module': 'run_pbi_integration', 'sub_module': 'power_bi_refresh_datasets', 'data_type': 'Main powerbi refresh triggered', 'executed': True, 'break_updated': True},
        {'category': 'powerbi', 'module': 'run_pbi_integration', 'sub_module': 'power_bi_get_refresh_history', 'data_type': 'Main powerbi refresh complete', 'executed': True, 'break_updated': True},
        {'category': 'powerbi', 'module': 'run_pbi_integration', 'sub_module': 'power_bi_refresh_datasets', 'data_type': 'Inventory powerbi refresh triggered', 'executed': True, 'break_updated': True},
        {'category': 'powerbi', 'module': 'run_pbi_integration', 'sub_module': 'power_bi_get_refresh_history', 'data_type': 'Inventory powerbi refresh complete', 'executed': True, 'break_updated': True},

    ]

    df = pd.DataFrame(modules_list)
    df = df.reset_index()
    print_color(df, color='b')

    table_name = 'modules_mapping'
    engine.connect().execute(text(f'Drop Table if exists {table_name}'))

    sql_types = Database_Modules.Get_SQL_Types(df).data_types
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=project_name, chunksize=1000, dtype=sql_types)

    engine.connect().execute(text(f'Alter Table {table_name} add primary key(category,module, sub_module, data_type )'))
    print_color(f'Modules Mapping Import to SQL', color='g')


def database_setup(engine):
    scripts = []
    scripts.append(f'''create table if not exists program_function_log(
           ID int auto_increment primary key,
           start_time datetime,
           end_time datetime,
           Module varchar(255),
           Function_Name varchar(255),
           Arguements text,
           Executed boolean,
           Error_Type varchar(65),
           Error_Message text);''')
    scripts.append(f'truncate program_function_log;')

    run_sql_scripts(engine=engine, scripts=scripts)

    map_module_setting(engine=engine, category='project_setup', module='create_database', sub_module='',
                       data_type='project setup')


def set_brand_mapping(engine):
    scripts = []
    scripts.append(f'alter table  style_master modify brand_lookup varchar(65);')


    scripts.append(f'update open_order_data set style = replace(style,"","") where locate("",style) >0')
    # scripts.append(f'update inventory_logic_by_size set style = replace(style,"","") where locate("",style) >0;')



    df = pd.read_sql(f'Select * from brand_reference', con=engine)
    for i in range(df.shape[0]):
        style_Lookup = df['Lookup'].iloc[i]
        Brand_Lookup = df['Brand'].iloc[i]
        print(style_Lookup, Brand_Lookup)
        scripts.append(f'update style_master set brand_lookup = "{Brand_Lookup}" where style like "{style_Lookup}%" and mid(style, length("{style_Lookup}")+1,1) REGEXP "^[0-9]+" ;')

    run_sql_scripts(engine=engine, scripts=scripts)

    map_module_setting(engine=engine, category='sql setup', module='set_brand_mapping', sub_module='',
                       data_type='set brand mapping')

@error_handler
def executeScriptsFromFile(engine, folder_name, file_name):
    # Open and read the file as a single buffer
    fd = open(f'{folder_name}\\{file_name}', 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')[:]

    sqlCommands = [x for x in sqlCommands if x.replace("\n","") != '']
    # print(sqlCommands)

    run_sql_scripts(engine=engine, scripts=sqlCommands)
    print_color(f'Sql File {file_name} Executed', color='g')

    map_module_setting(engine=engine, category='sql logic', module='executeScriptsFromFile', sub_module='',
                       data_type=file_name)


def connect_to_database():
    '''
    download the odbc driver for microsoft windows
    https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16

    '''
    server = 'rds.mastersystem.com,16866'
    database = 'JOSSHO_APW'
    username = 'josshoODBC'
    password = 'JosshoODBC16888!'
    driver = 'ODBC Driver 18 for SQL Server'
    dsn = "JOSMO CONNECTION"

    connection_string = f'DSN={dsn};DATABASE={database};UID={username};PWD={password};'
    # connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};'

    print_color(connection_string, color='y')
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        print("Connection established successfully!")
    except Exception as e:
        print_color(e, color='r')

    return cursor


def extract_data(setting):
    x = ProgramCredentials()
    if setting =='local':
        database_name = 'apwdata'
        server_name = 'OMSSERVER2019'
        oms_engine = create_engine(
            f'mssql+pyodbc://{server_name}/{database_name}?driver=SQL Server?Trusted_Connection=yes')

    elif setting == 'cloud':
        server_name = 'rds.mastersystem.com,16866'

        database = 'JOSSHO_APW'
        username = 'josshoODBC'
        password = 'JosshoODBC16888!'

        driver = 'ODBC Driver 18 for SQL Server'

        # driver = 'JOSMO CONNECTION'
        # dsn = "JOSMO CONNECTION"
        dsn = "OMS_CLOUD"
        server = 'rds.mastersystem.com'
        port = 16866
        connection_string = (
            f"mssql+pyodbc://{username}:{password}@{server_name}/{database}?driver={driver}&trusted_connection=no&encrypt=no"
        )
        # connection_string = f"mssql+pyodbc://{dsn}"




        print_color(connection_string, color='g')
        oms_engine = create_engine(connection_string)
    # print_color(oms_engine, color='y')
    #
    # try:
    #     oms_engine.connect()
    # except Exception as e:
    #     print_color(e, color='r')
    #     exit()


    computer = getpass.getuser()
    computer_dict = computer_dict_method()

    if computer =='Administrator':
        computer_setting =  'Production'
    elif computer == '':
            computer_setting = 'Staging'
    else:
        computer_setting = 'Development'

    project_folder, engine, project_name, hostname, username, password, port = get_proper_engine(computer_setting)

    data_directory = computer_dict.get(computer).get('data_directory')
    second_data_directory = computer_dict.get(computer).get('second_data_directory')

    data_folder = computer_dict.get(computer).get('data_folder')
    export_folder = computer_dict.get(computer).get('export_folder')
    images_folder = computer_dict.get(computer).get('images_folder')
    image_output = computer_dict.get(computer).get('image_output')
    dropbox_image_folder = computer_dict.get(computer).get('dropbox_image_folder')
    image_token = computer_dict.get(computer).get('image_token')

    if computer_setting not in ('Production', 'Staging'):
        data_folder = data_directory

    create_folder(data_directory)
    create_folder(second_data_directory)
    create_folder(f'{export_folder}\\proposal_data_files')
    create_folder(f'{export_folder}\\comparative_styles_files')

    create_folder(f'{second_data_directory}\\proposal_data_files')
    create_folder(f'{second_data_directory}\\comparative_styles_files')
    create_folder(export_folder)

    engine1 = engine_setup(project_name=None, hostname=hostname, username=username, password=password, port=port)
    with engine1.connect() as connection:
      connection.execute(text(f'Create Database if not exists {project_name}'))

    # modules_mapping(project_name=project_name, engine=engine)
    #
    # database_setup(engine)
    # Calendar(engine, schema=project_name)
    # copy_jpg_png_images(engine=engine, original_folder=images_folder, new_folder=dropbox_image_folder)
    #
    #
    # if computer_setting in ('Production', 'Staging'):
    #     get_url_links(engine=engine, token_file=image_token)

    # if computer_setting in ('Production', 'Staging') or setting == 'cloud':
    #     recruit_images(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_customers(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_vendors(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_warehouses(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     # setup_temporary_tables(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_style_master(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_purchase_order_data(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_received_purchase_order_data(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_open_order_data(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #
    #     recruit_color_codes(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_size_breakdown(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_size_packs(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_case_breakdown(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_po_by_size_data(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)
    #     recruit_inventory_data(engine=engine, conn=oms_engine, data_directory=data_directory, second_data_directory=second_data_directory)


    # if computer_setting in ('Production', 'Staging'):
    #     recruit_image_files(engine=engine, original_folder=images_folder, new_folder=dropbox_image_folder)
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='images')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='brand_reference')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='inventory_data')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='po_data_by_size')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='case_breakdown')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='color_codes')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='size_breakdown')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='size_pack')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='po_data')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='received_po_data')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='open_order_data')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='style_master')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='warehouses')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='customers')
    # import_data_to_sql(engine=engine, project_name=project_name, data_folder=data_folder, report_type='vendors')

    # set_primary_keys(engine=engine)
    # set_indexes(engine=engine)

    folder_name = f'{project_folder}\\SQL Files'
    set_brand_mapping(engine=engine)

    executeScriptsFromFile(engine=engine, folder_name=folder_name, file_name='Data Setup Logic.sql')
    executeScriptsFromFile(engine=engine, folder_name=folder_name, file_name='Comparative_Style_Logic.sql')
    executeScriptsFromFile(engine=engine, folder_name=folder_name, file_name='Container_Logic 2.sql')

    run_pbi_integration(engine)
    run_diagnostic(engine=engine, project_folder=project_folder, prod_setting=computer_setting, export_path=export_folder)

    export_data_sets(engine, export_folder, f'{second_data_directory}')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("hello")
        setting = 'cloud'
        methods = ["extract_data"]

        globals()["extract_data"](setting)
    else:
        method = sys.argv[1]
        setting = sys.argv[2]
        globals()[method](setting)
