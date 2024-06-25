import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import getpass
import shutil
import pickle
import datetime
import pandas as pd
from sqlalchemy import inspect
import Database_Modules
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email, smtplib, ssl
# import time # imports the time module
# import openpyxl

from Database_Modules import print_color, engine_setup, run_sql_scripts, create_folder


def Attach_File(Output_Folder, file_name, message):
    filename = Output_Folder + "\\" + file_name
    # In same directory as script
    # TEST_NAME = "TEST NAME"
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    #Add header as key/value pair to attachment part
    part.add_header('Content-Disposition', 'attachment', filename=file_name)
# Add attachment to message and convert message to string
    message.attach(part)

    return message



def get_email_credentials(dirpath):
    print_color(f'{dirpath}\\login.pickle', color='b')
    if os.path.exists(dirpath + "/" + 'login.pickle'):
        with open(dirpath + "/" + 'login.pickle', 'rb') as token:
            info = pickle.load(token)
            sender_email = info.get("sender")
            password = info.get("password")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
               server.login(sender_email, password)
            except:
                sender_email = input("Type your email address and press enter: ")
                password = input("Type your password and press enter: ")
                some_obj = {'sender': sender_email, 'password': password}
                with open(dirpath + "/" + 'login.pickle', 'wb') as f:
                    pickle.dump(some_obj, f)

    else:
        #########
        # Confirm that the account you are sending your email from is correct!
        # For Gmail users, go into your Google account settings and go to Security
        # Go to the Less Secure App Access option and turn this on
        #########
        sender_email = input("Type your email address and press enter: ")
        # if sender_email == "":
        #     break
        password = input("Type your password and press enter: ")
        # if password == "":
        #     break

        some_obj = {'sender': sender_email, 'password': password}
        with  open(f'{dirpath}\\login.pickle', 'wb') as f:
            pickle.dump(some_obj, f)
    return sender_email, password




def email_diagnostic(computer, prod_setting, dirpath, df_list, files, log_folder, export_path):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"JosmoShoes Program Diagnostic {now}"

    print_color(f'TIMESTAMP: {now}', color='g')

    df1 = df_list[0]
    df2 = df_list[1]



    print_color(df1, color='r')


    df_modules_did_not_run = df1.query('break_updated==1 & run_status.isnull() & sub_module != "power_bi_get_refresh_history"')
    df_refresh_did_not_hit = df1.query('sub_module == "power_bi_get_refresh_history" & run_status.isnull()')

    df_refresh_status = df2['status'].iloc[0]
    df_refresh_details = df2['details'].iloc[0]



    if len(df_modules_did_not_run) > 0:
        contents = f'Hello Team,<br><br>The Josmo Shoes Manager <br><span style="color:Red;font-weight:Bold; ">Did Not Run Properly</span>.<br>'
    else:
        contents = f'Hello Team,<br><br>The Josmo Shoes Manager <br><span style="color:Green;font-weight:Bold;">Completed Properly</span>.<br>'

    if len(df_refresh_did_not_hit) > 0:
        contents += f'<span style="color:Red;font-weight:Bold; ">PowerBI was not Refreshed</span>.<br>'
    else:
        contents += f'<span style="color:Green;font-weight:Bold; ">PowerBI was Refreshed</span>.<br>'




    if len(df_modules_did_not_run)>0:
        contents += "<br><hr><br>"
        contents += f'''<p> <span style="color:Red;font-weight:Bold; text-decoration: underline;">The Following Modules did not Run:</span>'''
        for i in range(df_modules_did_not_run.shape[0]):
            category = df_modules_did_not_run['category'].iloc[i]
            module = df_modules_did_not_run['module'].iloc[i]
            sub_module = df_modules_did_not_run['sub_module'].iloc[i]
            data_type = df_modules_did_not_run['data_type'].iloc[i]
            contents += f"<tr><td>\t{category}\t\t</td><td>  -- {module}\t</td><td>{sub_module}\t</td><td>{data_type}</td></tr>"


    if df_refresh_status in ('Failed', 'None') :
        contents += "<br><hr><br>"
        contents += f'''<p> <span style="color:Red;font-weight:Bold; text-decoration: underline;">PowerBI Refresh Failed with the Following Error</span>'''
        contents += f'''<p> <span style="color:Black; ">{df_refresh_details}</span>'''



    body = contents
    sender_email = "admin@Simpletowork.com"
    cc_email = ''
    if computer == "Administrator":
        receiver_email = ["Ricky@Simpletowork.com", "oramos@josmo.com",]
        # receiver_email = ["Ricky@Simpletowork.com"]
        cc_email = ["", "", "", ""]
    else:
        receiver_email = ["ricky@Simpletowork.com"]

    # receiver_email =["ricky@Simpletowork.com"]

    # bcc_email = "rshandorf@beteshgroup.com"
    # cc_email = ["Joe@Simpletowork.com"]
    # cc_email="Joe@Simpletowork.com"

    sender_email, password = get_email_credentials(dirpath)

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = subject
    # message["Bcc"] = bcc_email  # Recommended for mass emails
    message["Cc"] = ", ".join(cc_email)
    # message["HTMLBody"] = body

    # Add body to email
    # message.attach(MIMEText(body, "plain"))

    message.attach(MIMEText(body, "html"))

    for each_file in files:
        message = Attach_File(log_folder, each_file, message)

    diagnostic_file = f'Module Logs.csv {now}.csv'
    if os.path.exists(f'{log_folder}\\{diagnostic_file}'):
        message = Attach_File(log_folder, diagnostic_file, message)

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        try:
            server.sendmail(sender_email, receiver_email, text)
        except:
            print(f'Email Could Not Be Sent')

    print("Process Complete")



def obtain_data_logs(engine, log_folder, computer, prod_setting, dirpath, export_path):

    df1 = pd.read_sql(f'''select A.*, B.executed as run_status, B.date, B.datetime
            from modules_mapping A left join
            (select * from
            (select *, row_number() over (partition by category, module, sub_module, data_type order by date, datetime desc) as ranking from modules_performance where date = curdate()) A
            where ranking = 1) B using(category,module, sub_module, data_type)
            order by `index`
            ''', con=engine)

    df2 = pd.read_sql(f'''select * from powerbi_refresh_status where id in (select max(id)
        from powerbi_refresh_status where date >= curdate()  group by `group`)''', con=engine)

    module_log = f'{log_folder}\\Module Logs.csv'
    df1.to_csv(module_log, index=False)

    df_list = [df1,df2]
    files = ['Module Logs.csv']

    print(dirpath)
    email_diagnostic(computer, prod_setting, dirpath, df_list, files, log_folder, export_path)


def run_diagnostic(engine, project_folder, prod_setting, export_path):
    # project_folder, prod_setting, project_name, hostname, username, password, port = get_project_credenitals()
    computer = getpass.getuser()
    # computer_dict = computer_dict_method()
    # export_path = computer_dict.get(computer).get('export_path')
    # print(export_path)
    log_folder = f'{export_path}\\Logs'
    now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    create_folder(log_folder)
    pickle_folder = f'{project_folder}\\Text Files'


    # engine = engine_setup(project_name=project_name, hostname=hostname, username=username, password=password,port=port)

    obtain_data_logs(engine, log_folder, computer, prod_setting, pickle_folder, export_path)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        globals()["run_diagnostic"]()
    else:
        globals()[sys.argv[1]]()
