import os
import datetime
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine, text
import csv
import dateutil
import math
import psutil
import crayons
import time
import json
import getpass



def computer_dict_method():
    computer_dict = {
        'SimpleToWork': {
            'data_directory':f'G:\\My Drive\\Simple To Work\\9 - New Projects\\Josmo\\JosmoShoes\\Data Files',
            'second_data_directory': f'G:\\My Drive\\Simple To Work\\9 - New Projects\\Josmo\\JosmoShoes\\Data Files',
            'data_folder': f'C:\\Users\\{getpass.getuser()}\\Dropbox\\Josmo Program Manager\\Data Files',
            'export_folder':f'C:\\Users\\{getpass.getuser()}\\Dropbox\\Josmo Program Manager\\Data Files',
            'client_secret_file': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\client_secret.json',
            'token_file': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\token.json',
            'image_output': f'C:\\users\\{getpass.getuser()}\\dropbox\\Josmo Program Manager\\image_data',
            'images_folder': f'C:\\users\\{getpass.getuser()}\\dropbox\\Josmo Program Manager\images',
            'dropbox_image_folder': f'C:\\users\\{getpass.getuser()}\\dropbox\\Apps\\JosmoShoes_Images\\Images',
            'image_token': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\image_token.json',
        },
        'Ricky': {
            'data_directory':f'C:\\Users\\{getpass.getuser()}\\Dropbox\\Josmo Program Manager\\Data Files',
            'second_data_directory':f'C:\\Users\\{getpass.getuser()}\\Dropbox\\Josmo Program Manager\\Data Files',
            'data_folder': f'C:\\Users\\{getpass.getuser()}\\Dropbox\\Josmo Program Manager\\Data Files',
            'export_folder':f'C:\\Users\\{getpass.getuser()}\\Dropbox\\Josmo Program Manager\\Data Files',
            'client_secret_file': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\client_secret.json',
            'token_file': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\token.json',
            'image_output': f'C:\\users\\{getpass.getuser()}\\dropbox\\Josmo Program Manager\\image_data',
            'images_folder': f'C:\\users\\{getpass.getuser()}\\dropbox\\Josmo Program Manager\images',
            'dropbox_image_folder': f'C:\\users\\{getpass.getuser()}\\dropbox\\Apps\\JosmoShoes_Images\\Images',
            'image_token': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\image_token.json',
        },
        'SIMPLE TO WORK': {
            'data_directory':f'G:\\My Drive\\Simple To Work\\9 - New Projects\\Josmo\\JosmoShoes\\Data Files',
            'second_data_directory':f'G:\\My Drive\\Simple To Work\\9 - New Projects\\Josmo\\JosmoShoes\\Data Files',
            'data_folder': f'C:\\Users\\{getpass.getuser()}\\Dropbox\\Josmo Program Manager\\Data Files',
            'export_folder':f'C:\\Users\\{getpass.getuser()}\\Dropbox\\Josmo Program Manager\\Data Files',
            'client_secret_file': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\client_secret.json',
            'token_file': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\token.json',
            'image_output': f'C:\\users\\{getpass.getuser()}\\dropbox\\Josmo Program Manager\\image_data',
            'images_folder': f'C:\\users\\{getpass.getuser()}\\dropbox\\Josmo Program Manager\images',
            'dropbox_image_folder': f'C:\\users\\{getpass.getuser()}\\dropbox\\Apps\\JosmoShoes_Images\\Images',
            'image_token': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\image_token.json',
        },
        'Administrator': {
            'data_directory': f'O:\JosmoShoes\\Data Files',
            'second_data_directory': f'C:\\Users\\{getpass.getuser()}\\Dropbox\\Josmo Program Manager\\Data Files',
            'data_folder': f'C:\\Users\\{getpass.getuser()}\\Dropbox\\Josmo Program Manager\\Data Files',
            'export_folder':f'O:\\JosmoShoes\\Data Files',
            'client_secret_file':  f'O:\JosmoShoes\\Text Files\\client_secret.json',
            'token_file':  f'O:\JosmoShoes\\token.json',
            'image_output': f'C:\\users\\{getpass.getuser()}\\dropbox\\Josmo Program Manager\\image_data',
            'images_folder': f'V:\\',
            'dropbox_image_folder':f'C:\\users\\{getpass.getuser()}\\dropbox\\Apps\\Josmo_Images\\Images',
            'image_token': f'O:\JosmoShoes\\Text Files\\image_token.json',
        }
    }

    return computer_dict


    computer_dict = {'SimpleToWork': {'client_secret_file': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\client_secret.json',
                                        'token_file' :f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\token.json'},
                     'Ricky': {'client_secret_file': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\client_secret.json',
                                        'token_file': f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\token.json'},
                     'SIMPLE TO WORK':  {'client_secret_file' : f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\client_secret.json',
                                        'token_file' :f'C:\\Users\\{getpass.getuser()}\\Desktop\\New Projects\\Josmo\\JosmoShoes\\Text Files\\token.json'},
                     'planning':  {'client_secret_file' : f'E:\\Dropbox\Projects\\Q4_Designs_Manager\\Text Files\\client_secret.json',
                                        'token_file' :f'E:\\Dropbox\Projects\\Q4_Designs_Manager\\Text Files\\token.json'}}




def get_size(bytes, suffix="B"):

    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_memory():
    p = psutil.Process(os.getpid());
    with p.oneshot():
        print_color(f"Total Memory called in other module: {get_size(p.memory_info()[0])}", color='b')
        # print(f"Launch client called in other module {p.name()}")  # execute internal routine once collecting multiple info
        print_color(f"Total CPU memory used during command run time {p.cpu_percent()}%", color='p')

    ram_size = get_size(p.memory_info()[0]).split("MB")[0]

    return ram_size


    #


def error_handler(func):
    def Inner_Function(*args, **kwargs):
        print_color('Decorator Called', color='b')
        computer = getpass.getuser()
        if computer == 'Administrator':
            computer_setting = 'Production'
        elif computer == '':
            computer_setting = 'Staging'
        else:
            computer_setting = 'Development'

        project_folder, engine, project_name, hostname, username, password, port = get_proper_engine(computer_setting)
        start_time = datetime.datetime.now()
        error_message = None
        error_type = None

        e = ""


        params = locals().get('kwargs')
        # print('params', params)
        param_string = ""
        for each_param in params:
            param_string += f'{each_param}: {params.get(each_param)}\n'


        try:

            func(*args, **kwargs)
            success = True
        except OSError as e:
            print(f"{func.__name__} Error:  {e}")
            error_message = str(e)
            error_type = "OSError"
            success = False

        data = [[0, start_time, datetime.datetime.now(),func.__module__, func.__name__,  param_string,success, error_type, error_message]]
        df = pd.DataFrame(data)
        df.columns = ['ID', 'start_time','end_time', 'Module', 'Function_Name','Arguements',  'Executed', 'Error_Type', 'Error_Message']

        table_name = 'program_function_log'
        sql_types = Get_SQL_Types(df).data_types

        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=project_name, chunksize=1000,
                  dtype=sql_types)
    return Inner_Function


def print_color(*text, color='', _type='', output_file=None):
    ''' color_choices = ['r','g','b', 'y']
        _type = ['error','warning','success','sql','string','df','list']
    '''
    color = color.lower()
    _type = _type.lower()

    if color == "g" or _type == "success":
        crayon_color = crayons.green
    elif color == "r" or _type == "error":
        crayon_color = crayons.red
    elif color == "y" or _type in ("warning", "sql"):
        crayon_color = crayons.yellow
    elif color == "b" or _type in ("string", "list"):
        crayon_color = crayons.blue
    elif color == "p" or _type == "df":
        crayon_color = crayons.magenta
    elif color == "w":
        crayon_color = crayons.normal
    else:
        crayon_color = crayons.normal


    print(*map(crayon_color, text))
    if output_file is not None:
        # print(output_file)
        # print(os.path.exists(output_file))
        if os.path.exists(output_file) is False:
            # print("Right Here")
            file1 = open(output_file, 'w')
            file1.writelines(f'#################\n')
            file1.close()
            # file1 = open(output_file, 'w')
            # file1.close()
        # print(os.path.exists(output_file))
        file1 = open(output_file, 'a')
        file1.writelines(f'{str(text)}\n')
        file1.close()
        # print("Here")


def log_sql_scripts(log_scripts=False, log_engine=None, log_database=None,  script_name=None, profile_name=None, project_name=None, company_name=None,
                    query=None, start_time=None, end_time=None, duration=None):

    if log_scripts is True:
        t = [(profile_name, project_name, company_name, script_name, query, start_time, end_time, duration)]
        df = pd.DataFrame(t)

        df.columns = ['profile_name', 'project_name', 'company_name', 'script_name', 'sql_query', 'start_time', 'end_time', 'duration']
        print(df)

        table = 'sql_runtime_scripts'
        sql_types = Get_SQL_Types(df).data_types
        Change_Sql_Column_Types(engine=log_engine, Project_name=log_database, Table_Name=table,
                                                 DataTypes=sql_types, DataFrame=df)
        df.to_sql(name=table, con=log_engine, if_exists='append', index=False, schema=log_database, chunksize=1000,dtype=sql_types)


    # pass


def run_sql_scripts(engine=None, scripts=None, tryexcept=False,
                    log_scripts=False, log_engine=None, log_database=None, script_name=None, profile_name=None, project_name=None, company_name=None):
    real_start_time = time.time()
    time_list = []
    if tryexcept is True:
        for script in scripts:
            run_method = True
            run_attempt = 0
            time_now = time.time()
            start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            while run_method is True and run_attempt < 5:
                print_color(script, color='y')
                print_color("Running", color='p')
                try:
                    engine.execute(script)
                    time_list.append(time.time() - time_now)
                    log_sql_scripts(log_scripts=log_scripts, log_engine=log_engine, log_database=log_database, script_name=script_name,
                                    profile_name=profile_name, project_name=project_name, company_name=company_name,
                                    query=script, start_time=start_time,
                                    end_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    duration=time.time() - time_now)

                    print_color(f'Script Complete -- Took {round(time.time() - time_now, 4)} seconds to Run --', color='p')
                    run_method = False
                except Exception as e:
                    print_color(str(e), color='r')
                    if "(mysql.connector.errors.DatabaseError) 1206 (HY000): The total number of locks exceeds the lock table size" in str(e)\
                            or "(mysql.connector.errors.DatabaseError) 1205 (HY000): Lock wait timeout exceeded;" in str(e)\
                            or "(mysql.connector.errors.InternalError) 1213 (40001): Deadlock found when trying to get lock;" in str(e):

                        print_color("Going To Handle Here", color='r')
                        for t in range(0, 60, 10):
                            print_color(f"Mysql Table is Locked. Waiting {60 - t} Seconds to run.", color='y')
                            time.sleep(10)
                        run_attempt +=1

                    elif "(mysql.connector.errors.InterfaceError) 2013: Lost connection to MySQL server during query" in str(e):
                        print_color("Going To Handle Here", color='r')
                        for t in range(0, 15, 5):
                            print_color(f"Mysql Lost connection;  Waiting {15 - t} Seconds to run.", color='y')
                            time.sleep(5)
                        run_attempt += 1

                    else:
                        raise ValueError('Script Broke in Runtime')
                        run_method = False
            else:
                if run_attempt >=5:
                    print_color("Number of Tries Exceeded Attempt Threshold \n Forcing Break.", color='r')
                if run_method is False:
                    print_color("Method Complete", color='g')

    else:
        with engine.connect() as connection:
            for script in scripts:
                time_now = time.time()
                start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print_color(script, color='y')

                connection.execute(text(script))
                time_list.append(time.time() - time_now)
                log_sql_scripts(log_scripts=log_scripts, log_engine=log_engine, log_database=log_database,
                                script_name=script_name,
                                profile_name=profile_name, project_name=project_name, company_name=company_name,
                                query=script, start_time=start_time,
                                end_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                duration=time.time() - time_now)
                print_color(f'Script Complete -- Took {round(time.time() - time_now,4)} seconds to Run --', color='p')
    print_color(f'Scripts Complete --All Scripts Took {time.time() - real_start_time} seconds to Run --', color='b')

    # engine.dispose()

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def engine_setup(project_name=None, hostname = None, username=None, password=None, port=None, pool_pre_ping=True, echo=False):
    if project_name is None:
        engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{hostname}:{port}',pool_pre_ping=pool_pre_ping, echo=echo)
    else:
        engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{project_name}?charset=utf8',pool_pre_ping=pool_pre_ping, echo=echo,
                               pool_size=10,
                               max_overflow=20,  # Adjust the overflow size as needed
                               pool_timeout=30,  # Adjust the timeout as needed
                               pool_recycle=1800  # Adjust the recycle time as needed
                               )
    return engine


class ProgramCredentials():
    def __init__(self):
        filename = __file__

        filename = filename.replace('/',"\\")
        folder_name = '\\'.join(filename.split('\\')[:-2])
        print(folder_name)
        file_name = f'{folder_name}\\secret.json'
        f = json.load(open(file_name))
        # print(f)
        self.development_project_folder = f.get('development_project_folder')
        self.staging_project_folder = f.get('staging_project_folder')
        self.production_project_folder = f.get('production_project_folder')

        self.development_username =f.get('development_username')
        self.staging_username = f.get('staging_username')
        self.production_username = f.get('production_username')

        self.development_password = f.get('development_password')
        self.staging_password = f.get('staging_password')
        self.production_password = f.get('production_password')

        self.development_hostname = f.get('development_hostname')
        self.staging_hostname = f.get('staging_hostname')
        self.production_hostname = f.get('production_hostname')

        self.port =f.get('port')
        self.program_name =f.get('program_name')
        self.pavo_api_key  =f.get('pavo_api_key')


def get_proper_engine(computer_setting):
    x = ProgramCredentials()

    development_project_folder = x.development_project_folder.replace("%USERNAME%",getpass.getuser())
    staging_project_folder = x.staging_project_folder.replace("%USERNAME%",getpass.getuser())
    production_project_folder = x.production_project_folder.replace("%USERNAME%",getpass.getuser())

    development_username = x.development_username
    staging_username = x.staging_username
    production_username = x.production_username

    development_password = x.development_password
    staging_password = x.staging_password
    production_password = x.production_password

    development_hostname = x.development_hostname
    staging_hostname = x.staging_hostname
    production_hostname = x.production_hostname

    port = x.port
    project_name = x.program_name

    # computer = getpass.getuser()
    if computer_setting == 'Staging':
        project_folder = staging_project_folder
        hostname = staging_hostname
        username = staging_username
        password = staging_password
    if computer_setting == 'Production':
        project_folder = production_project_folder
        hostname = production_hostname
        username = production_username
        password = production_password
    if computer_setting == 'Development':
        project_folder = development_project_folder
        hostname = development_hostname
        username = development_username
        password = development_password

    engine = engine_setup(project_name=project_name, hostname=hostname, username=username, password=password, port=port)

    return project_folder, engine, project_name, hostname, username, password, port


class create_folder():
    def __init__(self, foldername=""):
        if not os.path.exists(foldername):
            os.mkdir(foldername)


class Run_Status():
    def __init__(self, engine1, Project_Name="", Company_Name="", script_name=''):
        timestamp = datetime.datetime.now()
        date = datetime.datetime.strftime(timestamp, '%Y-%m-%d')
        script = f'Select * from execution_status where Project_name = "{Project_Name}" and Company_name = "{Company_Name}" and Date = "{date}" and script_name="{script_name}"'
        print(script)
        df = pd.read_sql(script, con=engine1)
        script_type = str(script_name.split(" ")[-1].split(".")[0]).upper()

        if df.shape[0] > 0:
            previous_timestamp = df['End_Time'].iloc[0]
            run = False
            print_color(f'{Project_Name} - {Company_Name}      {script_type} SCRIPT ALREADY EXECUTED ON {str(previous_timestamp)}',color='g')
        else:
            print_color(f'{Project_Name} - {Company_Name}      RUNNING {script_type} MODULE', color='g')
            run = True

        self.run = run


class Check_Prior_Run():
    def __init__(self, engine='', Project_Name="", Company_Name="", Request_Category='', Request_Type=''):
        script = f'Select * from project_log where Company_Name = "{Company_Name}" and Request_Category = "{Request_Category}" and Request_Type = "{Request_Type}" and Request_Time > curdate();'
        # print(script)
        df2 = pd.read_sql(script, con=engine)
        if df2.shape[0] > 0:
            run = False
            print_color(Request_Type, "Will Run Through = False", color='r')
        else:
            print_color(Request_Type, "Will Run Through = True", color='g')
            run = True

        self.run = run


class check_run_through_status():
    def __init__(self, engine, Project_Name="", Company_Name="", contingent_script = [], Wait_and_Retry=False, check_accounts=False):
        script = f'Select * from credentials where Project_Name = "{Project_Name}"'
        df = pd.read_sql(script, con=engine)
        account_count = df.shape[0]
        check_count = len(contingent_script)
        if check_accounts is True:
            check_count = check_count * account_count

        look_for=""
        for i, name in enumerate(contingent_script):
            if i == 0:
                look_for = f'script_name ="{name}"'
            else:
                look_for += f' or script_name ="{name}"'

        if check_accounts is True:
            script = f'''Select sum(Executed) as check_status from execution_status
                        where Project_name = "{Project_Name}"
                        and Date = curdate() and ({look_for}) ;'''
        else:
            script = f'''Select sum(Executed) as check_status from execution_status
                                    where Project_name = "{Project_Name}" and Company_name = "{Company_Name}"
                                    and Date = curdate() and ({look_for}) ;'''
        print(script)
        df = pd.read_sql(script, con=engine)

        check_status = df['check_status'].iloc[0]
        if check_status == None:
            check_status =0
        else:
            check_status = int(check_status)


        print_color(f'{check_status} {check_count}', color='b')

        run_through = False
        time_limit = 9000
        time_check = 0
        start_time = datetime.datetime.now()
        if Wait_and_Retry is True:
            while run_through is False and time_check <= time_limit:
                if check_status == check_count:
                    run_through = True
                    print_color('This Process Will Run Through: ' + str(run_through), color='y')
                else:
                    if Wait_and_Retry is True:
                        print_color(f'This Process Will Run Through: {str(run_through)} -- Time Now: {start_time} -- Waiting 5 Minutes and Will Try Again', color='y')
                        time.sleep(300)
                        time_check += 300
                        start_time = datetime.datetime.now()
                        df = pd.read_sql(script, con=engine)
                        check_status = df['check_status'].iloc[0]
        else:
            if check_status == check_count:
                run_through = True
            print_color('This Process Will Run Through: ' + str(run_through), color='y')

        self.run_through = run_through


def check_run_through_by_query(engine, Project_Name="", Company_Name="", contingent_import=''):
    script = f'''select count(*) as check_run from report_que
            where company_name = "{Company_Name}"
            and date = curdate()
            and table_name = "{contingent_import}"
            and data_imported = 1;'''
    check_run = pd.read_sql(script, con=engine)['check_run'][0]
    if check_run == 0:
        output = False
    elif check_run == 1:
        output = True

    return output


class Executed():
    def __init__(self,engine1, Project_Name="", Company_Name="", start_time="", Start_Time="", script_name="", ):

        print_color("--- Module took %s seconds to run ---" % (time.time() - start_time), color='y')

        # w = WMI('.')
        # result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
        # print(result)
        # ram = int(result[0].WorkingSet)
        # return int(result[0].WorkingSet)
        #
        # bsize = 1024
        # a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
        # r = float(ram)
        # for i in range(a['g']):
        #     r = round(r / bsize, 4)


        timestamp = datetime.datetime.now()
        date = datetime.datetime.strftime(timestamp, '%Y-%m-%d')
        script_time = time.time() - start_time
        run_time = str(datetime.timedelta(seconds=script_time))
        # print('RAM Here')
        # print(r)
        # print("ram = ", r)
        p = psutil.Process(os.getpid());

        # r = 0.00
        # print(run_time)
        r = get_memory()

        with engine1.connect() as con:
            con.execute(
                f'Insert into execution_status values("{Project_Name}", "{Company_Name}","{date}","{Start_Time}","{timestamp}","{run_time}", "{script_name}",{1},{r})')

        print_color('EXECUTED',color='g')


class write_files_to_sql():
    def __init__(self, engine="",project_name="", company_name="", report_name="", request_type="", file="",
                 start_date="", end_date="", row_count=0):
        timestamp = str(datetime.datetime.now()).split(".")[0]
        executed=1
        df = pd.DataFrame((company_name, report_name, request_type,file, timestamp, start_date,
                           end_date, row_count, executed)).transpose()
        df.columns = ['Company_Name', 'Report_Name', 'Request_Type', 'File_Name', 'Import_Date',
                      'Start_Date', 'End_Date', 'Row_Count', 'Imported']
        table_name = 'imported_file_log'
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=project_name, chunksize=1000)

        # conn = engine.connect()
        # conn.execute(f'''insert into imported_file_log values("{company_name}","{report_name}","{request_type}",
        #                 "{file}","{timestamp}","{start_date}","{end_date}",{row_count},{executed})''')


class RemoveData():
    def __init__(self, engine='', project_name='', company_name='', report_name='', table_name=''):
        if engine.dialect.has_table(engine, table_name):
            scripts = []
            # conn = engine.connect()
            scripts.append(f'Delete From {table_name} where COMPANY_NAME = "{company_name}";')
            scripts.append(f'''Delete From Imported_File_Log where COMPANY_NAME = "{company_name}"
                    and Report_Name = "{report_name}";''')
            run_sql_scripts(engine=engine, scripts=scripts, tryexcept=True)


            print_color(f'Data Removed for {company_name} from {table_name}', color='r')


class RemoveSpecifiedData():
    def __init__(self, engine="", project_name="", company_name="", report_name="", table_name="",
                 date_to_remove=[], lookup_field=''):
        for dates in date_to_remove:
            start_date = dates[0]
            end_date = dates[1]
            print(start_date, end_date)
            # end_date1 = (datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

            file_name = f'{report_name} {start_date} - {end_date}.csv'
            script = f'SELECT Table_Schema, Table_Name From information_schema.tables where TABLE_SCHEMA = "{project_name}" and TABLE_NAME = "{table_name}"'
            df1 = pd.read_sql(script, con=engine)

            if df1.shape[0] > 0:
                scripts = []
                scripts.append(f'Delete from {table_name} where {lookup_field} >="{start_date}" and {lookup_field} <= "{end_date}" and COMPANY_NAME = "{company_name}";')
                scripts.append(f'Delete from imported_file_log where COMPANY_NAME = "{company_name}" and Report_Name = "{report_name}" and File_Name = "{file_name}";')

                run_sql_scripts(engine=engine, scripts=scripts, tryexcept=True)

                print_color(f'Data for {table_name} Start Date: {start_date} End Date: {end_date} Have been Deleted', color="p")
                print_color(f'Data for imported_file_log File_Name:  {file_name} Have been Deleted',color="b")


class files_to_import():
    def __init__(self, engine="",Company_name="",Request_Category="", Report_Name="",files=""):
        script = f'Select File_Name from imported_file_log where Company_Name="{Company_name}" and Report_Name="{Report_Name}" and Request_Type="{Request_Category}";'
        df = pd.read_sql(script,con=engine)
        imported_files = df['File_Name'].tolist()
        final_files = set(files).difference(set(imported_files))

        self.final_files = final_files


class Date_interval():
    def __init__(self, Start_date = '2018-01-01', Interval_Type = '30'):
        ## ESTABLISH TIMEFRAME OF DATAPULL  ####################################################################################
        start_date = datetime.datetime.strptime(Start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.today().date() - datetime.timedelta(days =1)
        # end_date = datetime.date(2021, 1, 6) - datetime.timedelta(days =1)
        num_days = (end_date - start_date).days
        date_list = []

        if Interval_Type == "Monthly":
            num_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
            date_list = [start_date + dateutil.relativedelta.relativedelta(months=i) for i in range(num_months)]

        elif Interval_Type == 'Quarterly':
            num_quarters = (end_date.year - start_date.year) * 4 + (round((end_date.month - start_date.month) / 3))
            date_list = [start_date + dateutil.relativedelta.relativedelta(months=i * 3) for i in range(num_quarters)]

        elif Interval_Type == 'Yearly':
            num_years = (end_date.year - start_date.year) + (math.ceil((end_date.month - start_date.month) / 12))
            date_list = [start_date + dateutil.relativedelta.relativedelta(months=i * 12) for i in range(num_years)]
        elif Interval_Type == 'All':
            x=1
            date_list = [start_date]
        elif Interval_Type == '30':
            dates_list = []
            date_list = []

            num_years = (end_date.year - start_date.year) + (math.ceil((max(end_date.month - start_date.month,1)) / 12))
            year_list = [start_date + dateutil.relativedelta.relativedelta(months=i * 12) for i in range(num_years)]

            for year_num in year_list:
                if end_date.year == year_num.year:
                    num_days = max((end_date-year_num).days - max(end_date.month - start_date.month,1),1)
                    dates_list.append([year_num + datetime.timedelta(days=31 * i) for i in range(math.ceil(num_days / 30))])
                else:
                    num_days = ((year_num + dateutil.relativedelta.relativedelta(months=12)) - year_num).days
                    dates_list.append([year_num + datetime.timedelta(days=31 * i) for i in range(int(num_days / 30))])

            for i in dates_list:
                for i1 in i:
                    date_list.append(i1)
        elif Interval_Type == '7':
            date_list = [start_date + datetime.timedelta(days=7 * i) for i in range(int(num_days / 7))]

        # print(start_date, end_date)
        date_intervals = []
        # GET DATA PERIODS FOR EACH PULL REQUEST  #############################################################################
        for i in range(len(date_list)):
            # if i + 1 < len(date_list):
            if Interval_Type == "Monthly":
                interval = [str(date_list[i]), str(date_list[i] + dateutil.relativedelta.relativedelta(months=1) - datetime.timedelta(days=1))]
            elif Interval_Type == "Quarterly":
                interval = [str(date_list[i]), str(date_list[i] + dateutil.relativedelta.relativedelta(months=3) - datetime.timedelta(days=1))]
            elif Interval_Type == "Yearly":
                interval = [str(date_list[i]), str(date_list[i] + dateutil.relativedelta.relativedelta(months=12) - datetime.timedelta(days=1))]
            elif Interval_Type == "All":
                interval = [str(start_date),str(end_date)]
            elif Interval_Type == '30':
                if date_list[i].month == 12:
                    day_diff = 31 - date_list[i].day
                    interval = [str(date_list[i]), str(date_list[i] + datetime.timedelta(days=day_diff))]
                else:
                    interval = [str(date_list[i]), str(date_list[i] + datetime.timedelta(days=30))]
            elif Interval_Type == '7':
                interval = [str(date_list[i]), str(date_list[i] + datetime.timedelta(days=7))]

            date_intervals += [interval]


        self.date_intervals = date_intervals
        self.start_date = start_date

    def __iter__(self):
        return iter(self.date_intervals)


class Remove_Blank_Files():
    def __init__(self, project_folder, Company_name, Report_Type):
        All_Orders_Main_Folder = project_folder + "Data Files\\" + Report_Type
        All_Orders_Folder = All_Orders_Main_Folder + "\\" + Company_name
        files = sorted(os.listdir(All_Orders_Folder))

        status = None
        for file in files:
            file_name =f'{All_Orders_Folder}\\{file}'
            file_size = round(os.path.getsize(file_name) /1024,0)
            # print(file, file_size)
            if file_size < 100:
                if  status is True:
                    # print("checking")
                    with open(file_name, 'r', encoding="latin9") as csvfile:
                        csv_rows = [row for row in csv.DictReader(csvfile)]

                    count_rows = len(csv_rows)
                    if count_rows == 0:
                        os.remove(file_name)
            else:
                status = True


class Remove_Files():
    def __init__(self, project_folder, Company_name, Report_Type, Month_Range=1):
        All_Orders_Main_Folder = project_folder + "Data Files\\" + Report_Type
        All_Orders_Folder = All_Orders_Main_Folder + "\\" + Company_name
        files = sorted(os.listdir(All_Orders_Folder))

        date_lookup = datetime.date.today() + dateutil.relativedelta.relativedelta(months=-Month_Range)
        print_color(f"Date To Delete Data After {date_lookup}", color='b')
        for file in files:
            start_date = file.split(".")[0].split(" - ")[0].split(" ")[-1]
            if str(start_date) > str(date_lookup):
                os.remove(f'{All_Orders_Folder}\\{file}')


class Required_Report_Dates():
    def __init__(self,project_folder,Company_name, Report_Type, Start_Date,Interval_Type):
        ## CHECK ORDERS FOLDER TO SEE WHICH REPORTS ALREADY EXISTS  ############################################################
        All_Orders_Main_Folder = project_folder + "Data Files\\" + Report_Type
        All_Orders_Folder = All_Orders_Main_Folder + "\\" + Company_name
        create_folder(All_Orders_Main_Folder)
        create_folder(All_Orders_Folder)

        Existing_Files=[]
        Final_set = []

        Remove_Blank_Files(project_folder=project_folder, Company_name=Company_name, Report_Type=Report_Type)
        files = os.listdir(All_Orders_Folder)

        for file in files:
            print(file)
            order_start_date = file.split(".")[0].split(" ")[-3].split(".")[0]
            order_end_date = file.split(".")[0].split(" ")[-1].split(".")[0]
            Existing_Files.append([order_start_date, order_end_date])


        ## COMPARE ALREADY EXISTING FILES TO THE DATES THAT WE NEED TO SEE WHICH FILES WE STILL NEED TO PULL  ##################
        date_list = Date_interval(Start_Date, Interval_Type).date_intervals
        start_date = Date_interval(Start_Date, Interval_Type).start_date

        # print(date_list)


        if len(Existing_Files) > 0:
            min_date_from_files = min(Existing_Files)[0]

            if min_date_from_files < datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=365*1.25),'%Y-%m-%d'):
                min_date = min_date_from_files
            else:
                pass
                # min_date = start_date
        else:
            pass
            # min_date = start_date

        for i in date_list:
            if ([i[0], i[1]] not in Existing_Files or [i[0], i[1]] == max(date_list)):
                Final_set.append([i[0], i[1]])

        self.Final_set = Final_set


class RequiredReportDatesForImport():
    def __init__(self,engine, project_folder, company_name, report_type, start_date, interval_type, time_range):

        date_list = Date_interval(start_date, interval_type).date_intervals
        # for d in date_list:
        #     print(d)
        replace_date = date_list[-time_range:][0][0]

        script = f'''Select Start_Date, End_Date from imported_file_log
                    where Company_Name="{company_name}" and Report_Name = "{report_type}"
                    order by Start_Date
                    '''

        print(script)
        df = pd.read_sql(script, con=engine).astype(str)

        script1 = f'''Select Start_Date, End_Date from imported_file_log
                         where Company_Name="{company_name}" and Report_Name = "{report_type}"
                         and (Import_Date - interval 1 day < End_Date
                         or Start_Date >= "{replace_date}")
                         order by Start_Date
                         '''

        # print(script)
        print(script1)

        df1 = pd.read_sql(script1, con=engine).astype(str)

        df_list = [tuple(x) for x in df.to_numpy()]
        updated_date_list = [tuple(l) for l in date_list]
        # print(updated_date_list, df_list)

        Final_List = []
        for x in updated_date_list:
            if x not in df_list:
                Final_List.append(x)

        df1_list = df1.values.tolist()

        Final_set= Final_List + df1_list

        self.Final_set = Final_set


class ConfirmDataExtract:
    def __init__(self, engine=None, extract_type=None, company_name=None,
                 request_category=None, report_name=None, request_id=None,
                 generate_report_id=None, report_processing_status=None,
                 file_name=None,
                 ):
        conn = engine.connect()
        if extract_type == "get_report_request_list":
            conn.execute(f'''Update project_log set Executed = 1 where Request_Category = "{request_category}"
                            and Request_Type = "{report_name}" and Request_ID = "{request_id}";''')


            conn.execute(f'''Update report_que set
                                report_processing_status = "{report_processing_status}",
                                generate_report_id = {generate_report_id}
                                where company_name = "{company_name}"
                                and report_name = "{report_name}"
                                and report_request_id = {request_id}''')
            conn.execute(f'''Update report_que set report_get_requested_report_list = 1
                               where company_name = "{company_name}"
                               and report_name = "{report_name}"
                               and report_request_id = {request_id}
                               and report_processing_status in ('_DONE_','_CANCELLED_','_DONE_NO_DATA_')
                               ''')


        elif extract_type == "get_report":
            script = f'''Update report_que set report_get_report = 1,
                            file_name= "{file_name}"
                            where company_name = "{company_name}"
                            and report_name = "{report_name}"
                            and generate_report_id = {generate_report_id}
                            and report_request_id = {request_id}
            '''
            # print(script)
            conn.execute(script)
            print_color(f'Report Que Updated for Get Report', color='g')
        elif extract_type == 'import_data_to_sql':
            script = f'''Update report_que set data_imported = 1
                                        where company_name = "{company_name}"
                                        and file_name= "{file_name}"
                                        and report_name = "{report_name}"
                                        and generate_report_id = {generate_report_id}
                                        and report_request_id = {request_id}
                                        ;'''
            print(script)
            conn.execute(script)
            print_color(f'Report Data Updated for Get Report', color='g')


def convert_dataframe_types(df=None):
    columnLenghts = np.vectorize(len)

    # df = pd.DataFrame({'col': [1, 2, 10, np.nan, 'a'],
    #                    'col2': ['a', 10, 30, 40, 50],
    #                    'col3': [1, 2, 3, 4.36, np.nan]})

    col_is_numeric = df.replace(np.nan, 0).replace("nan", 0).replace("Nan",0).apply(lambda s: pd.to_numeric(s, errors='coerce')).notnull().all().tolist()
    col_list = df.columns.tolist()
    df_original_types = df.dtypes.tolist()

    for i, val in enumerate(col_is_numeric):
        if val == True:
            # print(df_original_types[i], col_list[i])
            if "datetime" not in str(df_original_types[i]):
                if "float" in str(df_original_types[i]):
                    # print(df[col_list[i]].replace(np.nan, 0).replace("nan",0).astype(str).str.split(".", n=2, expand = True))
                    decimal_level = df[col_list[i]].replace(np.nan, 0).replace("nan",0).astype(str).str.split(".", n=2, expand = True)[1].unique().tolist()
                else:
                    decimal_level = ['0']
                if len(decimal_level) == 1 and decimal_level[0] == '0':
                    df[col_list[i]] = df[col_list[i]].replace(np.nan, 0)
                    df[col_list[i]] = pd.to_numeric(df[col_list[i]], errors='ignore', downcast='integer')
                else:
                    df[col_list[i]] = pd.to_numeric(df[col_list[i]], errors='ignore')

    return df


class ConvertDataFrameTypes():
    def __init__(self,DataFrame):
        DataFrame = convert_dataframe_types(df=DataFrame)
        for col in DataFrame.columns:
            Col_Type = DataFrame[col].dtypes
            # print_color(f'{col} {Col_Type}', color = 'g' )
            if Col_Type == "float64":
                if not DataFrame[col].isnull().all():
                    DataFrame[col] = DataFrame[col].fillna(0)

            if Col_Type == "object":
                try:
                    DataFrame[col] = DataFrame[col].astype(float)
                except:
                    pass

        for col in DataFrame.columns:

            Col_Type = DataFrame[col].dtypes
            if Col_Type == "float64":
                if DataFrame[col].apply(float.is_integer).all():
                    DataFrame[col] = DataFrame[col].astype(int)

            try:
                if DataFrame[col].isnull().all():
                    DataFrame[col] = DataFrame[col].astype(str)
            except:
                pass
        DataFrame.columns = [col.replace('\ufeff','') for col in DataFrame.columns]
        self.DataFrame =DataFrame


class Add_Sql_Missing_Columns():
    def __init__(self, engine='',Project_name='', Table_Name='', DataFrame=''):
        ''' CHECK IF THE TABLE EXISTS'''
        # print(Project_name, Table_Name)
        script = f'SELECT Table_Schema, Table_Name From information_schema.tables where TABLE_SCHEMA = "{Project_name}" and TABLE_NAME = "{Table_Name}"'
        df1 = pd.read_sql(script, con=engine)
        if df1.shape[0] == 1:
            ''' IF THE TABLE EXISTS GET THE FIRST ROW OF THAT TABLE'''
            script1 = f'Select column_name AS `COLUMN` From information_schema.columns b1 where b1.table_schema = "{Project_name}" And b1.table_name ="{Table_Name}" order by ORDINAL_POSITION;'

            df2 = pd.read_sql(script1, con=engine)
            # print(df2)

            ''' CONVERT COLUMN NAMES OF BOTH THE DATAFRAME BEING ASSESED AND THE TABLE IMPORTED
                MAKES THE LIST VALUES ALL LOWERCASE
            '''
            col_dict = {}
            col_one_list = [x.lower() for x in DataFrame.columns]
            for col in DataFrame.columns.tolist():
                new_col = col.lower()
                col_dict.update({new_col:col})

            col_two_list = df2['COLUMN'].str.lower().tolist()
            ''' GET THE DIFFERENCE OF COLUMNS IF THERE IS A DIFFERENCE AND INPUT INTO A LIST'''
            col_diff = list(set(col_one_list).difference(set(col_two_list)))
            # print(col_one_list)
            # print(col_two_list)
            if col_diff != []:
                print_color('Difference of Columns',col_diff, color='b')

            columnLengths = np.vectorize(len)
            for column in col_diff:
                script2 = ""
                col = col_dict.get(column)

                Col_Length = columnLengths(DataFrame[col].values.astype(str)).max(axis=0)
                Col_Type = DataFrame[col].dtypes
                # print(Col_Type, Col_Length)
                if Col_Type == "object":
                    if Col_Length > 255:
                        script2 = f'Alter Table {Table_Name} add column `{col}` TEXT'
                    elif Col_Length >= 100:
                        script2 = f'Alter Table {Table_Name} add column `{col}` VARCHAR(255)'
                    elif Col_Length >= 50:
                        script2 = f'Alter Table {Table_Name} add column `{col}` VARCHAR(100)'
                    elif Col_Length >= 25:
                        script2 = f'Alter Table {Table_Name} add column `{col}` VARCHAR(50)'
                    elif Col_Length >= 15:
                        script2 = f'Alter Table {Table_Name} add column `{col}` VARCHAR(25)'
                    elif Col_Length >= 10:
                        script2 = f'Alter Table {Table_Name} add column `{col}` VARCHAR(15)'
                    elif Col_Length >= 5:
                        script2 = f'Alter Table {Table_Name} add column `{col}` VARCHAR(10)'
                    elif Col_Length >= 0:
                        script2 = f'Alter Table {Table_Name} add column `{col}` VARCHAR(5)'
                if Col_Type == "float" or Col_Type == "float64":
                    new_data = DataFrame[col].to_frame()
                    new_data = new_data.fillna(0)
                    new_data[col] = new_data[col].astype(str)
                    new = new_data[col].str.split(".", n=1, expand=True)
                    new.columns = ["First", "Second"]
                    Decimal_Depth = columnLengths(new['Second'].values.astype(str)).max(axis=0)
                    if Decimal_Depth <= 2:
                        if Col_Length <= 10:
                            script2 = f'Alter Table {Table_Name} add column `{col}` FLOAT(12,2)'
                        elif Col_Length <= 20:
                            script2 = f'Alter Table {Table_Name} add column `{col}` FLOAT(20,2)'
                    else:
                        if Col_Length <= 10:
                            script2 = f'Alter Table {Table_Name} add column `{col}` FLOAT(12,4)'
                        elif Col_Length <= 20:
                            script2 = f'Alter Table {Table_Name} add column `{col}` FLOAT(20,4)'
                if  Col_Type == "int8" or Col_Type == "int16" or Col_Type == "int32" or Col_Type == "int64":
                    if Col_Length >= 10:
                        script2 = f'Alter Table {Table_Name} add column `{col}` BIGINT'
                    else:
                        script2 = f'Alter Table {Table_Name} add column `{col}` INT'
                if Col_Type == "datetime64[ns]" or Col_Type == "datetime64":
                    script2 = f'Alter Table {Table_Name} add column `{col}` DATE'
                if Col_Type == "bool":
                    script2 = f'Alter Table {Table_Name} add column `{col}` BOOL'
                print_color(script2, color='y')
                if script2 != "":
                    engine.connect().execute(script2)


class Adjust_Table_Columns():
    def __init__(self, engine1='',engine2='',  Project_name='', Table_Name=''):
        script = f'''
            select * from
            (select COLUMN_NAME, max(DATA_TYPE) as data_type, max(CHARACTER_MAXIMUM_LENGTH) as col_length
            from information_schema.columns
            where TABLE_SCHEMA in (select distinct project_name from credentials where status = "active")
            and table_name = "inbound_shipments_detail"
            group by COLUMN_NAME) A
            where COLUMN_NAME not in (select distinct COLUMN_NAME from information_schema.columns
            where TABLE_SCHEMA = "{Project_name}")
        '''


        df = pd.read_sql(script, con=engine1)
        print(df)
        scripts = []
        scripts.append(f'SET FOREIGN_KEY_CHECKS=0;')
        script1= f'Alter Table {Table_Name} '
        for i in range(df.shape[0]):
            column = df['COLUMN_NAME'].iloc[i]
            data_type =  df['data_type'].iloc[i]
            col_length =  df['col_length'].iloc[i]

            if data_type == "varchar":
                column_type = f'{data_type}({col_length})'
            else:
                column_type = data_type
            if i ==0:
                script1 += f'Add Column {column} {column_type}'
            else:
                script1 += f',\nAdd Column {column} {column_type}'

        # print(script1)
        scripts.append(script1)
        scripts.append(f'SET FOREIGN_KEY_CHECKS=1;')
        run_sql_scripts(engine=engine2, scripts=scripts)


class Get_SQL_Types():
    def __init__(self,DataFrame):
        columnLenghts = np.vectorize(len)
        # print(np.nan)
        ## CONVERT DATAFRAME TYPES TO PROPER NUMERIC OR INTERGER BASED COLUMN TYPES
        # for col in DataFrame.columns:
        #     print_color(f'Attempting to Convert {col}')
        #     DataFrame[col] = DataFrame[col] .replace(np.nan, 0).replace("nan", 0).replace("Nan", 0).apply(lambda s: pd.to_numeric(s, errors='coerce'))

        # col_is_numeric = DataFrame.notnull().all().tolist()
        col_is_numeric =  DataFrame.replace(np.nan, 0).replace("nan", 0).replace("Nan", 0).apply(lambda s: pd.to_numeric(s, errors='coerce')).notnull().all().tolist()
        # print_color(f'col_is_numeric: {col_is_numeric}' , color='p')
        col_list = DataFrame.columns.tolist()
        df_original_types = DataFrame.dtypes.tolist()
        # print(df_original_types)
        for i, val in enumerate(col_is_numeric):
            if val == True:
                # print(df_original_types[i])
                if "datetime" not in str(df_original_types[i]):
                    decimal_level = DataFrame[col_list[i]].replace(np.nan, 0).replace("nan", 0).astype(str).str.split(".", n=2, expand=True)
                    # print(decimal_level)
                    if len(decimal_level.columns) > 1:
                        decimal_level = decimal_level[1].unique().tolist()
                        if len(decimal_level) == 1 and decimal_level[0] == '0':
                            DataFrame[col_list[i]] = DataFrame[col_list[i]].replace(np.nan, 0)
                            DataFrame[col_list[i]] = pd.to_numeric(DataFrame[col_list[i]], downcast='integer')
                        else:
                            DataFrame[col_list[i]] = pd.to_numeric(DataFrame[col_list[i]])
                    else:
                        DataFrame[col_list[i]] = DataFrame[col_list[i]].replace(np.nan, 0)
                        DataFrame[col_list[i]] = pd.to_numeric(DataFrame[col_list[i]], downcast='integer')

        # print(DataFrame.dtypes)

        ## GET THE APPROPRIATE MYSQL COLUMN TYPES FOR THE DATAFRAME OBJECT
        data_types = dict()
        for col in DataFrame.columns:
            # print(col)
            Col_Length = columnLenghts(DataFrame[col].values.astype(str)).max(axis=0)
            Col_Type = DataFrame[col].dtypes
            # print("column", col, Col_Length, Col_Type)
            if Col_Type == "object":
                if Col_Length > 255:
                    column_type = {col:sqlalchemy.types.TEXT()}
                    data_types.update(column_type)
                elif Col_Length >= 100:
                    column_type = {col:sqlalchemy.types.VARCHAR(255)}
                    data_types.update(column_type)
                elif  Col_Length >= 50:
                    column_type = {col:sqlalchemy.types.VARCHAR(100)}
                    data_types.update(column_type)
                elif  Col_Length >= 25:
                    column_type = {col:sqlalchemy.types.VARCHAR(50)}
                    data_types.update(column_type)
                elif Col_Length >= 15:
                    column_type = {col:sqlalchemy.types.VARCHAR(25)}
                    data_types.update(column_type)
                elif Col_Length >= 10:
                    column_type = {col:sqlalchemy.types.VARCHAR(15)}
                    data_types.update(column_type)
                elif Col_Length >= 5:
                    column_type = {col:sqlalchemy.types.VARCHAR(10)}
                    data_types.update(column_type)
                elif Col_Length >= 1:
                    column_type = {col:sqlalchemy.types.VARCHAR(5)}
                    data_types.update(column_type)
                elif  Col_Length == 0:
                    column_type = {col: sqlalchemy.types.VARCHAR(5)}
                    data_types.update(column_type)
            if Col_Type == "float" or Col_Type == "float64":
                new_data = DataFrame[col].to_frame()
                new_data = new_data.fillna(0)
                new_data[col] = new_data[col].astype(str)
                new = new_data[col].str.split(".", n = 1, expand = True)
                new.columns = ["First","Second"]
                Integer_Depth = columnLenghts(new['First'].values.astype(str)).max(axis=0)
                Decimal_Depth = columnLenghts(new['Second'].values.astype(str)).max(axis=0)
                # print_color(col, 'Integer_Depth', Integer_Depth, color='p')
                # print_color(col, 'Decimal_Depth',Decimal_Depth,color='p')
                if Decimal_Depth <=2:

                    if Col_Length <=10:
                        column_type = {col: sqlalchemy.types.Numeric(12,2)}
                        # column_type = {col: sqlalchemy.types.FLOAT(precision=12, asdecimal=True,decimal_return_scale=3)}
                    elif Col_Length <=20:
                        column_type = {col: sqlalchemy.types.Numeric(20, 2)}
                        # column_type = {col: sqlalchemy.types.FLOAT(20, 2)}
                    data_types.update(column_type)
                else:
                    if Col_Length <=10:
                        # column_type = {col: sqlalchemy.types.FLOAT(12,4)}
                        column_type = {col: sqlalchemy.types.Numeric(12, 4)}
                    elif Col_Length <=20:
                        # column_type = {col: sqlalchemy.types.FLOAT(20, 4)}
                        column_type = {col: sqlalchemy.types.Numeric(20, 4)}
                    data_types.update(column_type)
            if Col_Type == "int32" or Col_Type == "int64" or  Col_Type == "int8" :
                if Col_Length >= 10:
                        column_type = {col: sqlalchemy.types.BIGINT()}
                else:
                    column_type = {col: sqlalchemy.types.INTEGER()}
                data_types.update(column_type)
            if "datetime64[ns]" in str(Col_Type) or "datetime64" in str(Col_Type):
                date_level = len(DataFrame[col].astype(str).str.split(" ", n=1, expand=True).columns)
                if date_level ==1:
                    column_type = {col: sqlalchemy.types.DATE()}
                    data_types.update(column_type)
                else:
                    column_type = {col: sqlalchemy.types.DATETIME()}
                    data_types.update(column_type)
            if Col_Type == "bool":
                column_type = {col: sqlalchemy.types.BOOLEAN()}
                data_types.update(column_type)

            # print("Column", col, Col_Type, column_type)

        self.data_types = data_types


class View_SQL_Column_Lengths():
    def __init__(self, engine='', Project_Name='', Table_Name=''):
        script = f'Select Ordinal_Position as "#", column_name AS `COLUMN`, upper(COLUMN_TYPE) as TYPE From information_schema.columns b1 where b1.table_schema = "{Project_Name}" And b1.table_name = "{Table_Name}" order by ORDINAL_POSITION;'
        df = pd.read_sql(script, con=engine)
        script1 =''
        count=0

        text_column_count = len(df[df['TYPE'] == 'TEXT']) -1

        for i in range(df.shape[0]):
            # print(i)
            column_name = df['COLUMN'].iloc[i]
            column_type = df['TYPE'].iloc[i]
            # print(column_name, column_type)

            # if column_type == "TEXT":

            if count == df.shape[0]-1:
                script1 = script1 + '\n(SELECT "' + column_name + '" as "Column_Name",Max(Length(`' + column_name + '`)) as Char_Length \n From ' \
                          + Table_Name + '\n limit 1);'
            else:
                script1 = script1 + '\n(SELECT "' + column_name + '" as "Column_Name",Max(Length(`' + column_name + '`)) as Char_Length \n From ' \
                          + Table_Name + '\n limit 1) \n UNION ALL'


                count += 1

        df1 = pd.DataFrame()

        if script1 !='':
            df1 = pd.read_sql(script1, con=engine)
            # print(df1)

        self.DataFrame = df1


class Change_Sql_Column_Types():
    def __init__(self, engine='', Project_name='', Table_Name='', DataTypes='', DataFrame=''):

        # df3 = View_SQL_Column_Lengths(engine=engine, Project_Name=Project_name, Table_Name=Table_Name).DataFrame
        script = f'Select Ordinal_Position as "#", column_name AS `COLUMN`, upper(COLUMN_TYPE) as TYPE From information_schema.columns b1 where b1.table_schema = "{Project_name}" And b1.table_name = "{Table_Name}" order by ORDINAL_POSITION;'

        df2 = pd.read_sql(script, con=engine)
        df = DataFrame
        modify_script = ""
        DataType = {k.upper(): v for k,v in DataTypes.items()}
        # print(script)
        for i in range(df2.shape[0]):
            column = str(df2['COLUMN'].iloc[i])
            comparable_column = str(df2['COLUMN'].iloc[i]).upper()
            Column_Type = str(df2['TYPE'].iloc[i]).replace("'", '').replace('b', '')                    #THIS IS THE MYSQL COLUMN TYPE
            # sql_column_length = df3.loc[df3['Column_Name'] == column]['Char_Length'].iloc[0]
            # print_color(f'{column}, {Column_Type}, {DataType.keys()}', color='p')

            if comparable_column in DataType:
                dataframe_column_type = str(DataType[comparable_column]).replace(" ", "")                          # THIS IS THE DATAFRAME COLUMN TYPE
                # dataframe_column_type = dataframe_column_type

                # print_color(column, Column_Type, dataframe_column_type, color='p')
                if Column_Type == "FLOAT(12,4)" or Column_Type == "FLOAT(12,2)" or Column_Type == "FLOAT(20,4)" or Column_Type == "FLOAT(20,2)" or Column_Type == "VARCHAR(5)":
                    df[column] = df[column].replace(np.nan, 0)

                if Column_Type != dataframe_column_type:
                    if (Column_Type == "INT(11)" or Column_Type == "INT") and dataframe_column_type == "INTEGER":
                        pass
                    elif Column_Type == "BIGINT(20)" and dataframe_column_type == "BIGINT":
                        pass
                    elif (Column_Type == "BIGINT(20)" or Column_Type == "BIGINT") and dataframe_column_type == "INTEGER":
                        pass
                    elif Column_Type == "DATETIME" and "VARCHAR" in dataframe_column_type:
                        pass
                    elif "VARCHAR" in Column_Type and "DATETIME" in dataframe_column_type:
                        pass
                    elif Column_Type == "TIMESTAMP" and "DATETIME"  in dataframe_column_type:
                        pass
                    elif Column_Type == "DATE" and "VARCHAR" in dataframe_column_type:
                        pass
                    elif (Column_Type == "FLOAT(12,4)" or Column_Type == "FLOAT(20,4)" or Column_Type == "FLOAT(12,2)" or Column_Type == "FLOAT(20,2)") and dataframe_column_type == "INTEGER":
                        pass
                    elif Column_Type == "TINYINT(1)" and dataframe_column_type == "BOOLEAN":
                        pass
                    elif "FLOAT(20,4)" in Column_Type and "FLOAT(12,4)" in dataframe_column_type:
                        pass
                    elif "FLOAT(20,2)" in Column_Type and "FLOAT(12,2)" in dataframe_column_type:
                        pass
                    elif "DECIMAL(20,4)" in Column_Type and "DECIMAL(12,4)"in dataframe_column_type or "NUMERIC(12,4)" in dataframe_column_type:
                        pass
                    elif "DECIMAL(20,2)" in Column_Type and "DECIMAL(12,2)" in dataframe_column_type or "NUMERIC(12,2)" in dataframe_column_type:
                        pass
                    elif "NUMERIC(20,4)" in Column_Type and "NUMERIC(12,4)" in dataframe_column_type or "DECIMAL(12,4)"in dataframe_column_type:
                        pass
                    elif "NUMERIC(20,2)" in Column_Type and "NUMERIC(12,2)" in dataframe_column_type or "DECIMAL(12,2)" in dataframe_column_type:
                        pass

                    elif "VARCHAR" in Column_Type and ("NUMERIC" in dataframe_column_type or "DECIMAL" in dataframe_column_type or "FLOAT" in dataframe_column_type
                                                       or "INTEGER" in dataframe_column_type or "BIGINT" in dataframe_column_type):
                        pass
                    elif Column_Type == "DATE" and "DATETIME" in dataframe_column_type:
                        pass
                    elif "VARCHAR" in Column_Type and "BOOLEAN" in dataframe_column_type:
                        pass
                    elif "TEXT" in Column_Type and "VARCHAR" in dataframe_column_type:
                        pass
                    elif "TEXT" in Column_Type and "FLOAT" in dataframe_column_type:
                        pass
                    elif "VARCHAR" in Column_Type and "VARCHAR" in dataframe_column_type:
                        database_column_length = int(Column_Type.split("(")[1].split(")")[0])
                        dataframe_column_length = int(dataframe_column_type.split("(")[1].split(")")[0])

                        if dataframe_column_length > database_column_length:
                            # print_color(column, Column_Type, dataframe_column_type, color='y')
                            # print_color(database_column_length, dataframe_column_length, color='y')
                            # print(column, Column_Type, dataframe_column_length, database_column_length, dataframe_column_type,dataframe_column_length)
                            if modify_script == "":
                                modify_script += "MODIFY COLUMN `" + column + "` " + "VARCHAR(" + str(dataframe_column_length) + ")"
                            else:
                                modify_script += ", \nMODIFY COLUMN `" + column + "` " + "VARCHAR(" + str(dataframe_column_length) + ")"
                    elif "INT" in Column_Type and "DATETIME" in dataframe_column_type:
                        if modify_script == "":
                            modify_script += "MODIFY COLUMN `" + column + "` " + "VARCHAR(25)"
                        else:
                            modify_script += ", \nMODIFY COLUMN `" + column + "` " + "VARCHAR(25)"

                    else:
                        check_values = df[column].unique()
                        # print(check_values)
                        if len(check_values) == 1 and (check_values[0] == 0 or str(check_values[0]) == 'nan'):
                            pass
                        else:
                            # print_color(column, Column_Type, dataframe_column_type, color='y')
                            if modify_script == "":
                                modify_script += "MODIFY COLUMN `" + column + "` " + dataframe_column_type
                            else:
                                modify_script += ", \nMODIFY COLUMN `" + column + "` " + dataframe_column_type
        scripts=[]

        alter_script = "ALTER TABLE " + Table_Name + '\n'
        if modify_script != "":
            scripts.append(f'SET FOREIGN_KEY_CHECKS=0;')
            scripts.append(alter_script + modify_script)
            scripts.append(f'SET FOREIGN_KEY_CHECKS=1;')
            run_sql_scripts(engine=engine, scripts=scripts)

        self.DataFrame = DataFrame


class Fix_Table_Column_type():
    def __init__(self, engine='', Project_Name='', Table_Name=''):
        df = View_SQL_Column_Lengths(engine=engine, Project_Name=Project_Name, Table_Name=Table_Name).DataFrame
        script = f'Select Ordinal_Position as "#", column_name AS `COLUMN`, upper(COLUMN_TYPE) as TYPE From information_schema.columns b1 where b1.table_schema = "{Project_Name}" And b1.table_name = "{Table_Name}" order by ORDINAL_POSITION;'
        df2 = pd.read_sql(script, con=engine)

        for i in range(df2.shape[0]):
            column_name = df2['COLUMN'].iloc[i]
            column_type = df2['TYPE'].iloc[i]

            df3 = df.loc[df['Column_Name'] == column_name]['Column_Name'].iloc[0]
            Col_Length = df.loc[df['Column_Name'] == column_name]['Char_Length'].iloc[0]


            if column_type == "TEXT":
                # print(column_name, column_type, Col_Length)

                if Col_Length > 255:
                   Col_Length = '255+'
                elif Col_Length >= 100:
                    new_length = 255
                elif Col_Length >= 50:
                    new_length = 100
                elif Col_Length >= 25:
                    new_length = 50
                elif Col_Length >= 15:
                    new_length = 25
                elif Col_Length >= 10:
                    new_length = 15
                elif Col_Length >= 5:
                    new_length = 10
                elif Col_Length >= 1:
                    new_length = 5
                elif Col_Length == 0:
                    new_length = 5

                if Col_Length != '255+':
                    script2 = f'Alter Table {Table_Name} modify column {column_name} Varchar({new_length});'
                    print(script2)
                    engine.connect().execute(script2)


class Create_Table:
    def __init__(self, engine='', Project_name='', Sql_Types='', Table_Name=''):
        script = f'SELECT Table_Schema, Table_Name From information_schema.tables where TABLE_SCHEMA = "{Project_name}" and TABLE_NAME = "{Table_Name}"'
        df1 = pd.read_sql(script, con=engine)
        if df1.shape[0] ==0:
            print("Create Table")
            print(type(Sql_Types))

            for index, i in enumerate(Sql_Types):
                # print(type(i),i)
                # final_script=''
                data_type = Sql_Types.get(i)
                if index ==0:
                    script = 'Create Table if not exists ' + Table_Name + '(\n'
                    if i == "ID":
                        script = script + "`" + str(i) + "` " + str(data_type) + " " + "auto_increment primary key, \n"
                    else:
                        script = script + "`" + str(i) + "` " + str(data_type) + ",\n"
                elif index < len(Sql_Types)-1:
                    if i == "ID":
                        script = script + "`" + str(i) + "` " + str(data_type) + " " + "auto_increment primary key, \n"
                    else:
                        script = script + "`" + str(i) + "` " + str(data_type) + ",\n"

                elif index == len(Sql_Types)-1:
                    if i == "ID":
                        script = script + "`" + str(i) + "` " + str(data_type) + " " + "auto_increment primary key \n"
                    else:
                        script = script + "`" + str(i) + "` " + str(data_type) + "\n"

                    script = script + ');'

                    print("script", script)

        with engine.connect() as con:
            con.execute(script)


class Create_Blank_Table():
    def __init__(self, engine='', Table_Name='', Project_name='', Company_Name=''):

        script = f'SELECT Table_Schema, Table_Name From information_schema.tables where TABLE_SCHEMA = "{Project_name}" and TABLE_NAME = "{Table_Name}"'
        df1 = pd.read_sql(script, con=engine)
        if df1.shape[0] == 0:
            script = f'''select * from
            (select COLUMN_NAME, COLUMN_TYPE,COLUMN_KEY, ifnull(NUMERIC_PRECISION,0) as NUMERIC_PRECISION, ifnull(NUMERIC_SCALE,0) as NUMERIC_SCALE, CHARACTER_MAXIMUM_LENGTH,
            row_number() over (partition by COLUMN_NAME order by COLUMN_KEY desc, ORDINAL_POSITION) as ranking
             from information_schema.columns
            where TABLE_NAME = "{Table_Name}"
            and COLUMN_NAME != "ID"
            order by ORDINAL_POSITION) A
            where ranking = 1;
                    '''
            df = pd.read_sql(script, con=engine)
            scripts = []
            count=0
            create_table_script=f'CREATE TABLE IF NOT EXISTS {Table_Name} (\n'
            final_column_detail=''
            primary_key = 'Primary Key ('
            for i in range(df.shape[0]):

                COLUMN_NAME = df['COLUMN_NAME'].iloc[i]
                COLUMN_TYPE = df['COLUMN_TYPE'].iloc[i]
                NUMERIC_PRECISION = df['NUMERIC_PRECISION'].iloc[i]
                NUMERIC_SCALE = df['NUMERIC_SCALE'].iloc[i]
                CHARACTER_MAXIMUM_LENGTH = df['CHARACTER_MAXIMUM_LENGTH'].iloc[i]
                COLUMN_KEY = df['COLUMN_KEY'].iloc[i]

                if COLUMN_TYPE == "float":
                    column_detail = f'`{COLUMN_NAME}` {COLUMN_TYPE}{NUMERIC_PRECISION,NUMERIC_SCALE}'
                elif COLUMN_TYPE == "bigint":
                    column_detail = f'`{COLUMN_NAME}` {COLUMN_TYPE}({NUMERIC_PRECISION})'
                else:
                    column_detail = f'`{COLUMN_NAME}` {COLUMN_TYPE}'

                if i == df.shape[0]-1:
                    column_detail += ');'
                else:
                    column_detail += ',\n'
                final_column_detail +=column_detail

            create_table_script +=final_column_detail

            scripts.append(create_table_script)
            run_sql_scripts(engine=engine, scripts=scripts)
            print_color(f'{Table_Name} With No Data Has Been Created in Database', color='y')
        else:
            print_color(f'{Table_Name} Already Exists in Database', color='y')


class Remove_Foreign_Keys():
    def __init__(self, engine, Project_Name, Table_Name=""):
        scripts = []
        df4 = ""
        df5 = ""
        if Table_Name == "":
            script = f'''SELECT distinct CONSTRAINT_SCHEMA, CONSTRAINT_NAME, TABLE_NAME, REFERENCED_TABLE_NAME, COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = "{Project_Name}" and REFERENCED_TABLE_NAME is not null and ORDINAL_POSITION = 1;'''
            script1 = f' SELECT * from  INFORMATION_SCHEMA. STATISTICS WHERE TABLE_SCHEMA = "{Project_Name}" and INDEX_NAME != "Primary" and SEQ_IN_INDEX =1'
        else:
            script = f'''SELECT distinct CONSTRAINT_SCHEMA, CONSTRAINT_NAME, TABLE_NAME, REFERENCED_TABLE_NAME, COLUMN_NAME
                     FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = "{Project_Name}" and REFERENCED_TABLE_NAME = "{Table_Name}" and ORDINAL_POSITION = 1;'''
            script2 = f'''SELECT distinct CONSTRAINT_SCHEMA, CONSTRAINT_NAME, TABLE_NAME, REFERENCED_TABLE_NAME, COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = "{Project_Name}" and TABLE_NAME = "{Table_Name}" and REFERENCED_TABLE_NAME is not null and ORDINAL_POSITION = 1;'''

            script3 = f'SELECT * FROM  INFORMATION_SCHEMA. STATISTICS WHERE TABLE_SCHEMA = "{Project_Name}" AND TABLE_NAME = "{Table_Name}" and INDEX_NAME != "Primary" and SEQ_IN_INDEX = 1;'
            script1 = f' SELECT * from  INFORMATION_SCHEMA. STATISTICS WHERE TABLE_SCHEMA = "{Project_Name}" and INDEX_NAME != "Primary"  and SEQ_IN_INDEX =1 and TABLE_NAME = "{Table_Name}";'

            df4 = pd.read_sql(script2, con=engine)
            df5 = pd.read_sql(script3, con=engine)

        df1 = pd.read_sql(script, con=engine)
        df2 = pd.read_sql(script1, con=engine)

        if df1.shape[0]>0:
            table_list = df1['TABLE_NAME'].unique()
            print_color(script, color='y')
            print_color(table_list, color='p')

            for i in range(df1.shape[0]):
                table_name=df1['TABLE_NAME'].iloc[i]
                column_name = df1['COLUMN_NAME'].iloc[i]
                fk = df1['CONSTRAINT_NAME'].iloc[i]

                scripts.append(f'ALTER TABLE {table_name} drop FOREIGN KEY `{fk}`;')

            if Table_Name !="":
                for i in table_list:
                    # print(i)
                    index_script = f'SELECT distinct INDEX_NAME from  INFORMATION_SCHEMA. STATISTICS WHERE TABLE_SCHEMA = "{Project_Name}" and INDEX_NAME != "Primary" and TABLE_NAME = "{i}" and INDEX_NAME="{column_name}";'
                    print_color(index_script, color='p')
                    df3 = pd.read_sql(index_script, con=engine)
                    if df3.shape[0] > 0:

                        for i1 in range(df3.shape[0]):
                            index = df3['INDEX_NAME'].iloc[i1]
                            scripts.append(f'ALTER TABLE {i} drop index `{index}`;')

        if Table_Name == "":
            if df2.shape[0] > 0:
                for i in range(df2.shape[0]):
                    table_name = df2['TABLE_NAME'].iloc[i]
                    index = df2['INDEX_NAME'].iloc[i]
                    scripts.append(f'ALTER TABLE {table_name} drop index `{index}`;')

        if Table_Name != "":
            if df4.shape[0]>0:
                table_list = df4['TABLE_NAME'].unique()
                print_color(table_list, color='p')
                for i in range(df4.shape[0]):
                    table_name=df4['TABLE_NAME'].iloc[i]
                    column_name = df4['COLUMN_NAME'].iloc[i]
                    fk = df4['CONSTRAINT_NAME'].iloc[i]

                    scripts.append(f'ALTER TABLE {table_name} drop FOREIGN KEY `{fk}`;')

            if df5.shape[0] > 0:
                for i in range(df2.shape[0]):
                    table_name = df5['TABLE_NAME'].iloc[i]
                    index = df5['INDEX_NAME'].iloc[i]
                    scripts.append(f'ALTER TABLE {table_name} drop index `{index}`;')

        run_sql_scripts(engine=engine,scripts= scripts)


class Remove_ID_Columns():
    def __init__(self, engine, Project_Name, Table_Name=""):
        if Table_Name == "":
            script = f'SELECT table_schema, TABLE_NAME, COLUMN_NAME as TABLE_COLUMNS From information_schema.columns where table_schema = "{Project_Name}" and COLUMN_NAME = "ID" group by TABLE_NAME'
        else:
            script=f'SELECT table_schema, TABLE_NAME, COLUMN_NAME as TABLE_COLUMNS From information_schema.columns where table_schema = "{Project_Name}" and COLUMN_NAME = "ID" and TABLE_NAME = "{Table_Name}" group by TABLE_NAME'
        df1 = pd.read_sql(script, con=engine)
        if df1.shape[0] > 0:
            for i in range(df1.shape[0]):
                table_name = df1['TABLE_NAME'].iloc[i]
                column_name = df1['TABLE_COLUMNS'].iloc[i]
                script = f'Alter Table {table_name} drop column {column_name};'
                print_color(script, color='p')
                engine.connect().execute(script)


class Remove_Primary_Keys():
    def __init__(self, engine, Project_Name, Table_Name=""):
        if Table_Name == "":
            script = f'''select distinct concat("ALTER TABLE ", TABLE_NAME, " Drop Primary Key;") as script
                      from INFORMATION_SCHEMA.COLUMNS
                      WHERE COLUMN_KEY = "PRI"
                      AND TABLE_SCHEMA = "{Project_Name}"
                      AND EXTRA != "auto_increment";'''
        else:
            script = f'''select distinct concat("ALTER TABLE ", TABLE_NAME, " Drop Primary Key;") as script
                      from INFORMATION_SCHEMA.COLUMNS
                      WHERE COLUMN_KEY = "PRI"
                      AND TABLE_SCHEMA = "{Project_Name}"
                      AND TABLE_NAME = "{Table_Name}"
                      AND EXTRA != "auto_increment";'''

        df1 = pd.read_sql(script, con=engine)

        if df1.shape[0]>0:
            for i in range(df1.shape[0]):
                script = df1['script'].iloc[i]
                print_color(script, color='p')
                engine.connect().execute(script)



    # with engine.connect() as con:


class Primary_Key_Logic():
    def __init__(self, engine="", Project_Name="", table_name="All"):
        script = f'''select * from INFORMATION_SCHEMA.COLUMNS
                 WHERE COLUMN_KEY = "PRI"
                 AND TABLE_SCHEMA = "{Project_Name}"
                 AND TABLE_NAME = "{table_name}";'''
        df = pd.read_sql(script, con=engine)
        run_scripts=[]
        # print(script)
        if df.shape[0] == 0:
            if table_name == "calendar":
                script = 'Alter Table calendar add Primary Key(date);'
                run_scripts.append(script)
            if table_name == "exchange_rates":
                script = 'Alter Table exchange_rates add Primary Key(date, Currency);'
                run_scripts.append(script)
            if table_name == "all_listing":
                script = f'Alter Table all_listing add column ID int auto_increment primary key first;'
                # script = 'Alter Table all_listing add Primary Key(LISTING_ID);'
                run_scripts.append(script)
            if table_name == "open_inventory":
                script = f'Alter Table open_inventory add column ID int auto_increment primary key first;'
                # script = f'Alter Table open_inventory add Primary Key(COMPANY_NAME, SKU)'
                run_scripts.append(script)
            if table_name == "quality_suppressed_listings":
                script = 'Alter Table quality_suppressed_listings add Primary Key(COMPANY_NAME, sku, explanation);'
                run_scripts.append(script)
            if table_name == "fba_cancelled_listing":
                script = f'Alter Table fba_cancelled_listing add Primary Key(COMPANY_NAME, SELLER_SKU)'
                run_scripts.append(script)
            if table_name == "fba_inactive_listing":
                script = f'Alter Table fba_inactive_listing add Primary Key(COMPANY_NAME, SELLER_SKU)'
                run_scripts.append(script)
            if table_name == "fba_active_listing":
                script = f'Alter Table fba_active_listing add Primary Key(COMPANY_NAME, SELLER_SKU)'
                run_scripts.append(script)
            if table_name == "fba_all_inventory":
                script = f'Alter Table fba_all_inventory add Primary Key(COMPANY_NAME, SKU)'
                run_scripts.append(script)
            if table_name == "fba_amazon_fulfilled_inventory":
                script = f'Alter Table fba_amazon_fulfilled_inventory add Primary Key(COMPANY_NAME, SELLER_SKU,WAREHOUSE_CONDITION_CODE);'
                run_scripts.append(script)
            if table_name == "fba_multi_country_inventory_report":
                script = f'Alter Table fba_multi_country_inventory_report add Primary Key(`COMPANY_NAME`, `SELLER_SKU`);'
                run_scripts.append(script)
            if table_name == "reserved_inventory":
                script = f'Alter Table reserved_inventory add Primary Key(`COMPANY_NAME`,`sku`);'
                run_scripts.append(script)
            if table_name == "fba_inventory_health":
                script = f'Alter Table fba_inventory_health add Primary Key(`COMPANY_NAME`,`sku`);'
                run_scripts.append(script)
            if table_name == "fba_manage_inventory":
                script = f'Alter Table fba_manage_inventory add Primary Key(`COMPANY_NAME`,`sku`);'
                run_scripts.append(script)
            if table_name == "fba_stranded_inventory_report":
                script = f'Alter Table fba_stranded_inventory_report add Primary Key(`COMPANY_NAME`,`sku`);'
                run_scripts.append(script)
            if table_name == "fba_inventory_age":
                script = f'Alter Table fba_inventory_age add Primary Key(`COMPANY_NAME`,`sku`);'
                run_scripts.append(script)
            if table_name == "fba_manage_excess_inventory":
                script = f'Alter Table fba_manage_excess_inventory add Primary Key(`COMPANY_NAME`,`msku`);'
                run_scripts.append(script)
            if table_name == "all_orders":
                script = f'Alter Table All_Orders add column ID int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "returns":
                script = f'Alter Table Returns add column ID int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "fbm_returns":
                script = f'Alter Table fbm_returns add column ID int auto_increment primary key first;'
            if table_name == "fba_promotions_report":
                # script = f'Alter Table fba_promotions_report add Primary Key(ITEM_PROMOTION_ID, SHIPMENT_ITEM_ID);'
                script = f'Alter Table fba_promotions_report add column ID int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "fulfilled_shipments":
                script = f'Alter Table fulfilled_shipments add column ID int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "daily_inventory":
                script = f'Alter Table daily_inventory add Primary Key(COMPANY_NAME, SNAPSHOT_DATE, fnsku,sku, FULFILLMENT_CENTER_ID, DETAILED_DISPOSITION);'
                run_scripts.append(script)
            if table_name == "fba_storage_fees":
                script = f'Alter Table fba_storage_fees add column ID int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "fba_long_term_storage_fees":
                script = f'Alter Table fba_long_term_storage_fees add column ID int auto_increment primary key first;'
                # script = f'alter table fba_long_term_storage_fees add primary key(COMPANY_NAME, SNAPSHOT_DATE,SKU);'
                run_scripts.append(script)
            if table_name == "fba_inventory_adjustments_report":
                script = f'Alter Table fba_inventory_adjustments_report add column ID int auto_increment primary key first;'
                # script = f'Alter Table fba_inventory_adjustments_report add Primary Key(TRANSACTION_ITEM_ID,DISPOSITION,SKU, ADJUSTED_DATE, REASON);'
                run_scripts.append(script)
            if table_name == "fba_inventory_event_detail":
                script = f'Alter Table fba_inventory_event_detail add column ID int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "received_inventory":
                script = f'alter table received_inventory add column id int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "fba_reimbursements_report":
                script = f'alter table fba_reimbursements_report add column id int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "fba_removal_order_report":
                script = f'alter table fba_removal_order_report add column id int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "fba_removal_shipment_report":
                script = f'alter table fba_removal_shipment_report add column id int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "fee_preview":
                script = f'Alter Table fee_preview add column id int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "settlements":
                script = f'Alter Table settlements add column id int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "settlements_statements":
                script = f'Alter Table settlements_statements add column id int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "settlements_statements_extended":
                script = f'Alter Table settlements_statements_extended add column id int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "unshipped_orders":
                script = f'Alter Table unshipped_orders add primary key(`COMPANY_NAME`,`ORDER_ID`,`SKU`);'
                run_scripts.append(script)
            if table_name == "style_master":
                script = f'Alter Table style_master add primary key(`COMPANY_NAME`,`ASIN`);'
                run_scripts.append(script)
            if table_name == "asin_competitive_pricing":
                script = f'Alter Table asin_competitive_pricing add primary key(`COMPANY_NAME`,`ASIN`);'
                run_scripts.append(script)
            if table_name == "asin_lowest_offer_listing":
                script = f'Alter Table asin_lowest_offer_listing add primary key(`COMPANY_NAME`,`ASIN`);'
                run_scripts.append(script)
            if table_name == "asin_lowest_price_offer_listing":
                script = f'Alter Table asin_lowest_price_offer_listing add primary key(`COMPANY_NAME`,`ASIN`);'
                run_scripts.append(script)
            if table_name == "finances":
                script = f'Alter Table finances add column id int auto_increment primary key first;'
                run_scripts.append(script)
            if table_name == "inbound_shipments":
                script = f'Alter Table inbound_shipments add Primary Key(COMPANY_NAME, SHIPMENTID);'
                run_scripts.append(script)
            if table_name == "inbound_shipments_detail":
                script = f'Alter Table inbound_shipments_detail add Primary Key(COMPANY_NAME, SHIPMENTID, FULFILLMENTNETWORKSKU);'
                run_scripts.append(script)
            if table_name == "inbound_shipments_transport":
                script = f'Alter Table inbound_shipments_transport add Primary Key(COMPANY_NAME, SHIPMENTID);'
                run_scripts.append(script)

            if table_name == "advertising_campaign_reports":
                script = 'Alter Table advertising_campaign_reports add primary key (profile_id, campaignId, dates);'
                run_scripts.append(script)
            if table_name == "advertising_adgroup_report":
                script = f'Alter Table advertising_adgroup_report add primary key (profile_id, adGroupId, dates)'
                run_scripts.append(script)
            if table_name == "advertising_keywords_report":
                script = f'Alter Table advertising_keywords_report add primary key (profile_id, keywordId, dates)'
                run_scripts.append(script)
            if table_name == "advertising_product_ads_report":
                script = f'Alter Table advertising_product_ads_report add primary key (profile_id, campaignId, adGroupId,adId, sku, dates)'
                run_scripts.append(script)
            if table_name == "advertising_targets_report":
                script = f'Alter Table advertising_targets_report add primary key (profile_id, targetId, dates)'
                run_scripts.append(script)
        if run_scripts != []:
            script = f'set SqL_Mode = "";'
            run_scripts.insert(0, script)
            script= f'set foreign_key_checks = 0;'
            run_scripts.insert(0, script)
            script= f'set foreign_key_checks = 1;'
            run_scripts.append(script)
            run_sql_scripts(engine=engine, scripts=run_scripts)


class Foreign_Key_Logic():
    def __init__(self, engine="", Project_Name="", table_name="All"):
        script = f''' SELECT distinct CONSTRAINT_SCHEMA, CONSTRAINT_NAME, TABLE_NAME, REFERENCED_TABLE_NAME, COLUMN_NAME
                        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = "{Project_Name}"
                        and TABLE_NAME = "{table_name}" and REFERENCED_TABLE_NAME is not null and ORDINAL_POSITION = 1;'''
        df = pd.read_sql(script, con=engine)
        script = f'''
            select concat("Alter table ",TABLE_NAME," add foreign key (`", COLUMN_NAME, "`) references ", REFERENCED_TABLE_NAME, "(`",REFERENCED_COLUMN_NAME,"`);") as `Query` from
            (SELECT CONSTRAINT_SCHEMA, CONSTRAINT_NAME, TABLE_NAME, REFERENCED_TABLE_NAME, Group_concat(distinct COLUMN_NAME order by ORDINAL_POSITION separator "`, `") as COLUMN_NAME,
            Group_concat(distinct REFERENCED_COLUMN_NAME order by ORDINAL_POSITION separator "`, `") as REFERENCED_COLUMN_NAME
            FROM
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = "{Project_Name}"   and TABLE_NAME = "{table_name}" and REFERENCED_TABLE_NAME is not null
            group by CONSTRAINT_SCHEMA, CONSTRAINT_NAME, TABLE_NAME, REFERENCED_TABLE_NAME
            order by ORDINAL_POSITION asc
            ) A;'''
        # print(script)
        df1 = pd.read_sql(script, con=engine)
        queries = df1['Query'].tolist()

        foreign_keys=[]

        if table_name == "all_listing":
            script = f'alter table all_listing add foreign key (`company_name`, `seller_sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
        if table_name == "open_inventory":
            script = f'alter table open_inventory add foreign key (`company_name`, `sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
        if table_name == "quality_suppressed_listings":
            script = f'alter table quality_suppressed_listings add foreign key (`company_name`, `sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
        if table_name == "unshipped_orders":
            script = f'Alter table unshipped_orders add foreign key (`COMPANY_NAME`,`SKU`) references product_data(`COMPANY_NAME`,`SKU`);'
            foreign_keys.append(script)


        if table_name == "fba_cancelled_listing":
            script = f'Alter table fba_cancelled_listing add foreign key (`COMPANY_NAME`,`SELLER_SKU`) references product_data(`COMPANY_NAME`,`sku`);'
            foreign_keys.append(script)
        if table_name == "fba_inactive_listing":
            script = f'alter table fba_inactive_listing add foreign key (`company_name`, `seller_sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
        if table_name == "fba_active_listing":
            script = f'Alter table fba_active_listing add foreign key (`COMPANY_NAME`, `SELLER_SKU`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
        if table_name == "fba_all_inventory":
            script = f'Alter table fba_all_inventory add foreign key (`COMPANY_NAME`, `SKU`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
        if table_name == "fba_amazon_fulfilled_inventory":
            script = f'alter table fba_amazon_fulfilled_inventory add foreign key (`company_name`, `seller_sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
        if table_name == "fba_multi_country_inventory_report":
            script = f'alter table fba_multi_country_inventory_report add foreign key (`company_name`, `seller_sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
        if table_name == "reserved_inventory":
            script = f'alter table reserved_inventory add foreign key (`company_name`, `sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
        if table_name == "fba_inventory_health" or table_name == "all":
            script = f'alter table fba_inventory_health add foreign key (`company_name`, `sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
        if table_name == "fba_manage_inventory":
            script = f'Alter table fba_manage_inventory add foreign key (`COMPANY_NAME`, `sku`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
        if table_name == "fba_stranded_inventory_report":
            script = f'Alter table fba_stranded_inventory_report add foreign key (`COMPANY_NAME`, `sku`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
        if table_name == "fba_inventory_age":
            script = f'Alter table fba_inventory_age add foreign key (`COMPANY_NAME`, `sku`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
        if table_name == "fba_manage_excess_inventory":
            script = f'Alter table fba_manage_excess_inventory add foreign key (`COMPANY_NAME`, `msku`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
        if table_name == "all_orders":
            script = f'Alter table all_orders add foreign key (`COMPANY_NAME`, `SKU`) references product_data(`COMPANY_NAME`, `Sku`);'
            foreign_keys.append(script)
            # script = f'Alter table all_orders add foreign key (`DATE`) references calendar(`DATE`);'
            script = f'Alter table all_orders add foreign key (`DATE`, `CURRENCY`) references exchange_rates(`DATE`, `CURRENCY`);'

            foreign_keys.append(script)
        if table_name == "returns":
            script = f'Alter table returns add foreign key (`COMPANY_NAME`, `SKU`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
            script = f'Alter table returns add foreign key (`DATE`) references calendar(`DATE`);'
            foreign_keys.append(script)
        if table_name == "fba_promotions_report":
            # script = f'Alter table fba_promotions_report add foreign key (`AMAZON_ORDER_ID`) references Amazon_Order_IDs(`ORDER_ID`);'
            # foreign_keys.append(script)
            script = f'Alter table fba_promotions_report add foreign key (`DATE`) references calendar(`DATE`);'
            foreign_keys.append(script)
        if table_name == "fulfilled_shipments":
            script = f'Alter table fulfilled_shipments add foreign key (`COMPANY_NAME`, `SKU`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
            script = f'Alter table fulfilled_shipments add foreign key (`SHIPMENT_DATE_1`) references calendar(`DATE`);'
            foreign_keys.append(script)
        if table_name == "daily_inventory":
            script = f'Alter table daily_inventory add foreign key (`COMPANY_NAME`, `sku`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
            script = f'Alter table daily_inventory add foreign key (`Date`) references calendar(`DATE`);'
            foreign_keys.append(script)
        if table_name == "fba_storage_fees":
            script = f'Alter table fba_storage_fees add foreign key (`Date`) references calendar(`DATE`);'
            foreign_keys.append(script)

        if table_name == "fba_long_term_storage_fees":
            script = f'Alter table fba_long_term_storage_fees add foreign key (`COMPANY_NAME`, `SKU`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
            script = f'Alter table fba_long_term_storage_fees add foreign key (`Date`) references calendar(`DATE`);'
            foreign_keys.append(script)
        if table_name == "fba_inventory_adjustments_report":
            script = f'Alter table fba_inventory_adjustments_report add foreign key (`COMPANY_NAME`, `sku`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
            script = f'Alter table fba_inventory_adjustments_report add foreign key (`Date`) references calendar(`DATE`);'
            foreign_keys.append(script)
        if table_name == "fba_inventory_event_detail":
            script = f'Alter table fba_inventory_event_detail add foreign key (`COMPANY_NAME`, `SKU`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
            script = f'Alter table fba_inventory_event_detail add foreign key (`DATE`) references calendar(`DATE`);'
            foreign_keys.append(script)
        if table_name == "received_inventory":
            script = f'Alter table received_inventory add foreign key (`COMPANY_NAME`, `SKU`) references product_data(`COMPANY_NAME`, `SKU`);'
            foreign_keys.append(script)
            script = f'Alter table received_inventory add foreign key (`DATE`) references calendar(`DATE`);'
            foreign_keys.append(script)
        if table_name == "fba_reimbursements_report":
            script = f'Alter table fba_reimbursements_report add foreign key (`COMPANY_NAME`, `SKU`) references product_data(`COMPANY_NAME`, `SKU`);'
            foreign_keys.append(script)
            script = f'Alter table fba_reimbursements_report add foreign key (`DATE`) references calendar(`DATE`);'
            foreign_keys.append(script)
        if table_name == "fba_removal_order_report":
            script = f'Alter table fba_removal_order_report add foreign key (`COMPANY_NAME`, `SKU`) references product_data(`COMPANY_NAME`, `SKU`);'
            foreign_keys.append(script)
            script = f'Alter table fba_removal_order_report add foreign key (`DATE`) references calendar(`DATE`);'
            foreign_keys.append(script)
        if table_name == "fba_removal_shipment_report":
            script = f'Alter table fba_removal_shipment_report add foreign key (`COMPANY_NAME`, `SKU`) references product_data(`COMPANY_NAME`, `sku`);'
            foreign_keys.append(script)
            script = f'Alter table fba_removal_shipment_report add foreign key (`DATE`) references calendar(`DATE`);'
            foreign_keys.append(script)
        # if table_name == "fee_preview":
        #     script = f'Alter table fee_preview add foreign key (`COMPANY_NAME`,`sku`) references product_data(`COMPANY_NAME`,`sku`);'
        #     foreign_keys.append(script)
        if table_name == "settlements_statements":
            script = f'alter table settlements_statements add foreign key (`transaction_type`, `fee_category`, `fee_type`) references settlements_reference(`transaction_type`, `fee_category`, `fee_type`);'
            foreign_keys.append(script)
            script = f'alter table settlements_statements add foreign key (`posted_date_1`) references calendar(`date`);'
            foreign_keys.append(script)
            script = f'alter table settlements_statements add foreign key (`company_name`, `sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
        if table_name == "settlements_statements_extended":
            script = f'alter table settlements_statements_extended add foreign key (`transaction_type`, `fee_category`, `fee_type`) references settlements_reference(`transaction_type`, `fee_category`, `fee_type`);'
            foreign_keys.append(script)
            script = f'alter table settlements_statements_extended add foreign key (`posted_date_1`) references calendar(`date`);'
            foreign_keys.append(script)
            script = f'alter table settlements_statements_extended add foreign key (`company_name`, `sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
            # script = f'ALTER TABLE settlements_statements ADD INDEX `SKU` (`SKU` ASC) VISIBLE;'
            # foreign_keys.append(script)
            # script = f'create index settlements_orders_index on settlements_Statements(order_id);'
            # foreign_keys.append(script)
        if table_name == "inbound_shipments_detail":
            script = f'Alter table inbound_shipments_detail add foreign key (`COMPANY_NAME`, `SELLERSKU`) references product_data(`Company_Name`, `Sku`);'
            foreign_keys.append(script)
        # if table_name == "inbound_shipments_transport":
        #     script = f'alter table inbound_shipments_transport add foreign key (company_name, `sellersku`) references product_data(company_name, `sku`);'
        #     foreign_keys.append(script)
        if table_name == "available_inventory_report":
            script = f'alter table available_inventory_report add foreign key (`company_name`, `sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)


        if table_name == "advertising_campaign_reports":
            # script = f'Alter table advertising_campaign_reports add foreign key (`campaignId`) references advertising_campaign_key(`campaignId`);'
            # foreign_keys.append(script)
            script = f'Alter table advertising_campaign_reports add foreign key (`dates`) references calendar(`Date`);'
            foreign_keys.append(script)
        if table_name == "advertising_adgroup_report":
            # script = f'Alter table advertising_campaign_reports add foreign key (`campaignId`) references advertising_campaign_key(`campaignId`);'
            # foreign_keys.append(script)
            script = f'Alter table advertising_adgroup_report add foreign key (`dates`) references calendar(`Date`);'
            foreign_keys.append(script)

        if table_name == "purchase_order_report" or table_name == "all":
            script = f'Alter table purchase_order_report add foreign key (`company_name`, `sellersku`) references Product_Data(`company_name`, `sku`);'
            foreign_keys.append(script)

        if table_name == "purchase_order_data" or table_name == "all":
            script = f'Alter table purchase_order_data add foreign key (`company_name`, `sellersku`) references Product_Data(`company_name`, `sku`);'
            foreign_keys.append(script)
            script = f'Alter table purchase_order_data add foreign key (`outbound_date`) references calendar(`date`);'
            foreign_keys.append(script)

        if table_name == "settlement_orders" or table_name == "all":
            script = f'Alter table settlement_orders add foreign key (`company_name`, `sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
            script = f'Alter table settlement_orders add foreign key (`POSTED_DATE`) references calendar(`Date`);'
            foreign_keys.append(script)
        if table_name == "asin_performance_report" or table_name == "all":
            script = f'Alter table asin_performance_report add foreign key (`company_name`, `sku`) references product_data(`company_name`, `sku`);'
            foreign_keys.append(script)
            script = f'Alter table asin_performance_report add foreign key (`date`) references calendar(`Date`);'
            foreign_keys.append(script)

        foreign_keys = [x.lower() for x in foreign_keys]
        queries = [x.lower() for x in queries]
        final_foreign_keys = list(set(foreign_keys).difference(set(queries)))
        print_color(foreign_keys, color='b')
        print_color(queries, color='p')
        print_color(final_foreign_keys, color='b')
        if final_foreign_keys != []:
            script = f'SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;'
            final_foreign_keys.insert(0, script)
            script = f'SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;'
            final_foreign_keys.insert(1, script)
            script = f'SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE="ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION";'
            final_foreign_keys.insert(2, script)

            script = f'SET SQL_MODE=@OLD_SQL_MODE;'
            final_foreign_keys.append(script)
            script = f'SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;'
            final_foreign_keys.append(script)
            script = f'SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;'
            final_foreign_keys.append(script)

            run_sql_scripts(engine=engine, scripts=final_foreign_keys, tryexcept=True)


class Feed_Values_To_Foreign_Tables():
    def __init__(self, engine, Project_name, Company_name, Table_Name, DataFrame):
        '''
        Objective of this class is to push missing data values for foreign key relationships into
        the respective data table. As well can adjust null values of key parameters to default values so the
        relationship doesn't carry a null value.
        This ensures the program will not break when new data is fed into
        the program. As well the foreign keys can remain constant without being stripped, so the front-end user
        experience is never paused.

        :param engine:
        :param Project_name:
        :param Company_name:
        :param Table_Name:
        :param DataFrame:
        '''

        ### PRODUCT DATA ###
        script = f'Select distinct lower(COMPANY_NAME) as company_name, lower(sku) as sku from product_data where COMPANY_NAME = "{Company_name}";'

        pri_keys  = {"all_listing":["COMPANY_NAME", "SELLER_SKU"],
                     "open_inventory":["COMPANY_NAME", "SKU"],
                     "quality_suppressed_listings":["COMPANY_NAME", "SKU"],
                     "unshipped_orders":["COMPANY_NAME", "SKU"],
                     "fba_cancelled_listing":["COMPANY_NAME","SELLER_SKU"],
                     "fba_amazon_fulfilled_inventory":["COMPANY_NAME", "SELLER_SKU"],
                     "fba_multi_country_inventory_report":["COMPANY_NAME","SELLER_SKU"],
                     "reserved_inventory":["COMPANY_NAME","SKU"],
                     "fba_inventory_health":["COMPANY_NAME","SKU"],
                     "fba_manage_inventory":["COMPANY_NAME","SKU"],
                     "fba_stranded_inventory_report":["COMPANY_NAME","SKU"],
                     "fba_inventory_age":["COMPANY_NAME","SKU"],
                     "fba_manage_excess_inventory":["COMPANY_NAME","MSKU"],
                     "all_orders":["COMPANY_NAME","SKU"],
                     "returns":["COMPANY_NAME","SKU"],
                     "fulfilled_shipments":["COMPANY_NAME", "SKU"],
                     "daily_inventory":["COMPANY_NAME", "SKU"],
                     'fba_long_term_storage_fees':["COMPANY_NAME", "SKU"],
                     "fba_inventory_adjustments_report":["COMPANY_NAME", "SKU"],
                     "fba_inventory_event_detail":["COMPANY_NAME", "SKU"],
                     "received_inventory":["COMPANY_NAME", "SKU"],
                     "fba_reimbursements_report":["COMPANY_NAME", "SKU"],
                     "fba_removal_order_report": ["COMPANY_NAME", "SKU"],
                     "fba_removal_shipment_report": ["COMPANY_NAME", "SKU"],
                     # "fee_preview":["COMPANY_NAME", "SKU"],
                     "settlements":["COMPANY_NAME","SKU"],
                     "settlements_statements":["COMPANY_NAME","SKU"],
                     "settlements_statements_extended": ["COMPANY_NAME","SKU"],
                     "fba_inactive_listing": ["COMPANY_NAME" , "SELLER_SKU"],
                     "fba_active_listing":["COMPANY_NAME","SELLER_SKU"],
                     "fba_all_inventory":["COMPANY_NAME", "SKU"],
                     "inbound_shipments_detail":["COMPANY_NAME", "SELLERSKU"],
                     "finances": ["COMPANY_NAME", "SELLERSKU"],
                     }

        integrity_keys = {'all_orders':{'field_name':['CURRENCY'], 'values':[0]}}
        if Table_Name in integrity_keys.keys():
            # print(DataFrame.columns)
            for i, j in enumerate(integrity_keys.get(Table_Name).get('field_name')):
                # print(i, j)
                DataFrame[j] = DataFrame[j].replace(np.nan,integrity_keys.get(Table_Name).get('values')[i])


        if Table_Name in pri_keys.keys():
            df = pd.read_sql(script, con=engine)

            # script = f'''select max(decimal_count) as precision_level from
            #           (SELECT length(sku) - locate('.', sku) as decimal_count FROM product_data WHERE concat('',sku * 1) = sku and  sku like '%.%') A ;'''
            script = f'''select max(decimal_count) as precision_level from
                                (SELECT length(sku) - locate('.', sku) as decimal_count FROM product_data WHERE sku like '%.%' and sku NOT REGEXP '[A-Z]') A ;'''
            precision_level = pd.read_sql(script, con=engine)['precision_level'].iloc[0]
            # print(precision_level)
            precision_level = int(precision_level) if precision_level != None else 0
            pd.set_option('display.float_format', lambda x: '%.3f' % x)
            pd.set_option("display.precision", precision_level)
            # pd.options.display.float_format = '${:,.9f}'.format
            df['item_list'] = df[['company_name', 'sku']].apply(tuple, axis=1)
            product_data_sku_list = df['item_list'].tolist()

            lookup_col = pri_keys.get(Table_Name)

            updated_DataFrame = DataFrame
            columnLenghts = np.vectorize(len)
            from decimal import Decimal


            for col in lookup_col:
                print_color(updated_DataFrame[col])
                col_type = str(updated_DataFrame[col].dtype)
                # print(col_type)
                if col_type == 'float64':
                    updated_DataFrame[col] = updated_DataFrame[col].astype(str)
                    updated_DataFrame[col] = updated_DataFrame[col].apply(lambda x: x.split('.')[0] + "." +
                                                                                    x.split('.')[1][:precision_level])
                else:
                    updated_DataFrame[col] = updated_DataFrame[col].astype(str)
                    items_to_replace={
                        'nan':"",
                        '\xa0':'â',
                        '\x82â':'',
                        '\x82':''
                    }
                    for item in list(items_to_replace.keys()):
                        print(item, items_to_replace.get(item))
                        updated_DataFrame[col] = updated_DataFrame[col].str.replace(item, items_to_replace.get(item))
                        print(updated_DataFrame[col].unique())
                    updated_DataFrame[col]=updated_DataFrame[col].str.lower()



            # updated_DataFrame['sku'] = updated_DataFrame['sku'].replace('Nan', "")

            updated_DataFrame['item_list'] = updated_DataFrame[lookup_col].apply(tuple, axis=1)
            # print(updated_DataFrame[lookup_col])
            # print(updated_DataFrame[lookup_col].values.tolist())
            # updated_DataFrame['item_list'] = tuple(updated_DataFrame[lookup_col].tolist())


            dataframe_sku_list = updated_DataFrame['item_list'].unique().tolist()
            # print_color(dataframe_sku_list, color='p')
            for i, j in enumerate(dataframe_sku_list):
                if "v." in j[1]:
                    if isfloat(j[1]):
                        DataFrame[lookup_col[1]] = DataFrame[lookup_col[1]].replace(j[1], str(float(j[1])))

                        # dataframe_sku_list[i]
                        new_tuple = (j[0], str(float(j[1])))

                        dataframe_sku_list.remove(j)
                        dataframe_sku_list.append(new_tuple)

                        # print_color(f'{j[1]} {isfloat(j[1])} {new_tuple}', color='b')

            # print_color(dataframe_sku_list, color='g')
            # print_color(product_data_sku_list, color='y')
            # print(dataframe_sku_list)
            # print(product_data_sku_list)
            update_skus = list(set(dataframe_sku_list).difference(set(product_data_sku_list)))
            print_color(update_skus, color='p')
            # print_color(list(set(product_data_sku_list).difference(set(dataframe_sku_list))),color='y')



            for col in lookup_col:
                col_type = str(DataFrame[col].dtype)
                if "float" in col_type:
                    pass
                else:
                    DataFrame[col] = DataFrame[col].str.title()


            if len(update_skus) > 0:

                df_update = pd.DataFrame(update_skus)
                df_update.columns = ['company_name', 'Sku']
                df_update['company_name'] = df_update['company_name'].str.title()
                df_update['Sku'] = df_update['Sku'].astype(str)
                df_update['Sku'] = df_update['Sku'].str.title()
                print_color(df_update, color='g')
                sql_types = Get_SQL_Types(df_update).data_types
                Change_Sql_Column_Types(engine=engine, Project_name=Project_name, Table_Name='product_data', DataTypes=sql_types, DataFrame=df_update)
                df_update.to_sql(name="product_data", con=engine, if_exists='append', index=False, schema=Project_name,chunksize=1000)


        ### SETTLEMENT REFERENCES ###
        script = f'Select distinct TRANSACTION_TYPE, FEE_CATEGORY, FEE_TYPE from settlements_reference'
        pri_keys_1 = {"settlements_statements":["TRANSACTION_TYPE", "FEE_CATEGORY", "FEE_TYPE"]}
        if Table_Name in pri_keys_1.keys():
            print("Made it Here")
            df = pd.read_sql(script, con=engine)
            data = []
            updated_DataFrame = DataFrame

            for i in range(df.shape[0]):
                trans_type = df['TRANSACTION_TYPE'].iloc[i].lower()
                cat_type = df['FEE_CATEGORY'].iloc[i].lower()
                fee_type = df['FEE_TYPE'].iloc[i].lower()
                data.append([trans_type,cat_type,fee_type])
            data_1 = []
            for i in range(updated_DataFrame.shape[0]):
                print(updated_DataFrame.columns)
                trans_type = updated_DataFrame['TRANSACTION_TYPE'].iloc[i].lower()
                cat_type = updated_DataFrame['FEE_CATEGORY'].iloc[i].lower()
                fee_type = str(updated_DataFrame['FEE_TYPE'].iloc[i]).lower()
                data_1.append([trans_type, cat_type, fee_type])

            data_1 = tuple(tuple(sub) for sub in data_1)
            data = tuple(tuple(sub) for sub in data)
            # print(set(data))
            update_data = list(set(data_1).difference(set(data)))
            # print(update_data)
            df_update = pd.DataFrame(update_data)
            if df_update.shape[0] > 0:
                df_update.columns = ['TRANSACTION_TYPE','FEE_CATEGORY','FEE_TYPE']
                df_update.insert(3,"Old_Group_Key",0)
                df_update.insert(4, "Group_Key", 0)
                Sql_Types = Get_SQL_Types(df_update).data_types
                table_name = 'settlements_reference'
                df_update = ConvertDataFrameTypes(df_update).DataFrame
                Change_Sql_Column_Types(engine=engine, Project_name=Project_name, Table_Name=table_name, DataTypes=Sql_Types, DataFrame=df_update)
                df_update.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=Project_name, chunksize=1000, dtype=Sql_Types)



        if 'item_list' in DataFrame.columns:
            DataFrame = DataFrame.drop(columns=['item_list'])
        # print(DataFrame.columns)

        self.dataframe = DataFrame
        # ### ADVERTISING CAMPAIGN KEYS ###
        # script = f'Select distinct CampaignId, campaignName from product_data where Company = "{Company_name}";'


class Check_Primary_Key_Drop_Duplicates():
    def __init__(self, engine="", Project_Name="", table_name="All", Dataframe=pd.DataFrame()):
        '''
        If Table has Primary Key associations, then drop the duplicate values for the incoming data.
        Additionally if a table has primary keys, check if the default column types are null and modify
        so data doesn't get stopped from coming in when values are null.
        :param engine:
        :param Project_Name:
        :param table_name:
        :param Dataframe:
        '''
        pri_keys = {"all_listing": ["COMPANY_NAME","SELLER_SKU"],
                    "open_inventory": ["COMPANY_NAME", "SKU"],
                    "quality_suppressed_listings":["COMPANY_NAME", "SKU","EXPLANATION"],
                    "unshipped_orders":["COMPANY_NAME","ORDER_ID", "SKU"],
                    "fba_amazon_fulfilled_inventory":["COMPANY_NAME", "SELLER_SKU","WAREHOUSE_CONDITION_CODE"],
                    "fba_multi_country_inventory_report":["COMPANY_NAME","SELLER_SKU"],
                    "reserved_inventory":["COMPANY_NAME","SKU"],
                    "fba_cancelled_listing": ["COMPANY_NAME", "SELLER_SKU"],
                    "fba_inventory_health":["COMPANY_NAME","SKU"],
                    "fba_manage_inventory":["COMPANY_NAME","SKU"],
                    "fba_stranded_inventory_report":["COMPANY_NAME","SKU"],
                    "fba_inventory_age":["COMPANY_NAME","SKU"],
                    "fba_manage_excess_inventory":["COMPANY_NAME","MSKU"],
                    "fba_inactive_listing":["COMPANY_NAME", "SELLER_SKU"],
                    "fba_active_listing":["COMPANY_NAME", "SELLER_SKU"],
                    "fba_all_inventory":["COMPANY_NAME", "SKU"]

                    }

        if table_name in pri_keys.keys():
            primary_keys = pri_keys.get(table_name)
            for pri_key in primary_keys:
                Dataframe[pri_key] = Dataframe[pri_key].str.lower()
                Dataframe[pri_key] = Dataframe[pri_key].replace(np.nan, "")
            Dataframe.drop_duplicates(subset=primary_keys, keep='first', inplace=True)

            script = f'''select TABLE_NAME, COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH,
                COLUMN_DEFAULT from INFORMATION_SCHEMA.COLUMNS
                WHERE COLUMN_KEY = "PRI"
                AND TABLE_SCHEMA = "{Project_Name}"
                AND TABLE_NAME = "{table_name}";'''
            df = pd.read_sql(script, con=engine)

            for i in range(df.shape[0]):
                column_default = str(df['COLUMN_DEFAULT'].iloc[i])
                column_name = str(df['COLUMN_NAME'].iloc[i])
                data_type = str(df['DATA_TYPE'].iloc[i])
                char_length = str(df['CHARACTER_MAXIMUM_LENGTH'].iloc[i])
                script1 = ""
                if column_default == "None":

                    if data_type == "varchar":
                        new_data_type = f'varchar({char_length})'
                        script1 = f'Alter Table {table_name} modify {column_name} {new_data_type} Default ""'

                    if script1 != "":
                        engine.connect().execute(script1)

        self.df = Dataframe




def map_module_setting(engine=None,
    category=None, module=None, sub_module=None, data_type=None):

    engine.connect().execute(text(f'''insert into modules_performance values
    (null, curdate(), current_timestamp(), "{category}", "{module}", "{sub_module}", "{data_type}", {True})'''))



if __name__=="__main__":
   pass
