import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import pandas as pd
from sqlalchemy import inspect
import getpass
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# from Program_Manager import computer_dict_method
import Database_Modules
from Database_Modules import print_color, engine_setup, run_sql_scripts, create_folder, get_proper_engine, error_handler, computer_dict_method, map_module_setting


@error_handler
def recruit_images(engine, conn, data_directory, second_data_directory):
    scripts = f'''Select distinct TRIM(IMAGE_NM) AS IMAGE_FILE from INV'''
    df = pd.read_sql(scripts, con=conn)
    df.to_csv(f'{data_directory}\\images.csv', index=False)
    df.to_csv(f'{second_data_directory}\\images.csv', index=False)
    print_color(f'Image Data Exported', color='g')


@error_handler
def recruit_customers(engine, conn, data_directory, second_data_directory):
    scripts = f'''select CUS_ID AS CUSTOMER_ID, CUS_NM AS CUSTOMER_NAME, CUS_TYPE, ADDRESS, ADDRESS2, CITY, STATE, ZIP, 
        COUNTRY, PHONE, PHONE_2, PHONE_3, ATTN, CRD_LMT AS CREDIT_LIMIT from customer'''
    df = pd.read_sql(scripts, con=conn)
    df.to_csv(f'{data_directory}\\customers.csv', index=False)
    df.to_csv(f'{second_data_directory}\\customers.csv', index=False)
    print_color(f'Customer Data Exported', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_customers', sub_module='',
                       data_type='customers')

@error_handler
def recruit_vendors(engine, conn, data_directory, second_data_directory):
    scripts = f'''SELECT Ven_ID as Vendor_Id, VEN_NM as Vendor_Name, Ven_Type as Vendor_Type, Address, city, state, 
            zip, country, phone, attn  FROM venfile;'''
    df = pd.read_sql(scripts, con=conn)
    df.to_csv(f'{data_directory}\\vendors.csv', index=False)
    df.to_csv(f'{second_data_directory}\\vendors.csv', index=False)
    print_color(f'Vendor Data Exported', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_vendors', sub_module='',
                       data_type='vendors')

@error_handler
def recruit_warehouses(engine, conn, data_directory, second_data_directory):
    scripts = f'''SELECT WHS_NUM AS WAREHOUSE_ID, WHS_DESC AS WAREHOPUSE_NAME  FROM whs_file;'''
    df = pd.read_sql(scripts, con=conn)
    df.to_csv(f'{data_directory}\\warehouses.csv', index=False)
    df.to_csv(f'{second_data_directory}\\warehouses.csv', index=False)
    print_color(f'Warehouse Data Exported', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_warehouses', sub_module='',
                       data_type='warehouses')


def provide_temp_table_objects():
    temp_size_run = f'''
        (SELECT CLASS_CD, 1 AS NUMBER, 'SIZE 1' AS SIZE,RUN_SZ1  FROM def_szr WHERE RUN_SZ1 != '' UNION 
        SELECT CLASS_CD, 2 AS NUMBER,'SIZE 2' AS SIZE,RUN_SZ2  FROM def_szr WHERE RUN_SZ2 != '' UNION 
        SELECT CLASS_CD, 3 AS NUMBER,'SIZE 3' AS SIZE,RUN_SZ3  FROM def_szr WHERE RUN_SZ3 != '' UNION 
        SELECT CLASS_CD, 4 AS NUMBER,'SIZE 4' AS SIZE,RUN_SZ4  FROM def_szr WHERE RUN_SZ4 != '' UNION 
        SELECT CLASS_CD, 5 AS NUMBER,'SIZE 5' AS SIZE,RUN_SZ5  FROM def_szr WHERE RUN_SZ5 != '' UNION 
        SELECT CLASS_CD, 6 AS NUMBER,'SIZE 6' AS SIZE,RUN_SZ6  FROM def_szr WHERE RUN_SZ6 != '' UNION 
        SELECT CLASS_CD, 7 AS NUMBER,'SIZE 7' AS SIZE,RUN_SZ7  FROM def_szr WHERE RUN_SZ7 != '' UNION 
        SELECT CLASS_CD, 8 AS NUMBER,'SIZE 8' AS SIZE,RUN_SZ8  FROM def_szr WHERE RUN_SZ8 != '' UNION 
        SELECT CLASS_CD, 9 AS NUMBER,'SIZE 9' AS SIZE,RUN_SZ9  FROM def_szr WHERE RUN_SZ9 != '' UNION 
        SELECT CLASS_CD, 10 AS NUMBER,'SIZE 10' AS SIZE,RUN_SZ10  FROM def_szr WHERE RUN_SZ10 != '' UNION 
        SELECT CLASS_CD, 11 AS NUMBER,'SIZE 11' AS SIZE,RUN_SZ11  FROM def_szr WHERE RUN_SZ11 != '' UNION 
        SELECT CLASS_CD, 12 AS NUMBER,'SIZE 12' AS SIZE,RUN_SZ12  FROM def_szr WHERE RUN_SZ12 != '' UNION 
        SELECT CLASS_CD, 13 AS NUMBER,'SIZE 13' AS SIZE,RUN_SZ13  FROM def_szr WHERE RUN_SZ13 != '' UNION 
        SELECT CLASS_CD, 14 AS NUMBER,'SIZE 14' AS SIZE,RUN_SZ14  FROM def_szr WHERE RUN_SZ14 != '' UNION 
        SELECT CLASS_CD, 15 AS NUMBER,'SIZE 15' AS SIZE,RUN_SZ15  FROM def_szr WHERE RUN_SZ15 != '' UNION 
        SELECT CLASS_CD, 16 AS NUMBER,'SIZE 16' AS SIZE,RUN_SZ16  FROM def_szr WHERE RUN_SZ16 != '' UNION 
        SELECT CLASS_CD, 17 AS NUMBER,'SIZE 17' AS SIZE,RUN_SZ17  FROM def_szr WHERE RUN_SZ17 != '' UNION 
        SELECT CLASS_CD, 18 AS NUMBER,'SIZE 18' AS SIZE,RUN_SZ18  FROM def_szr WHERE RUN_SZ18 != '' UNION 
        SELECT CLASS_CD, 19 AS NUMBER,'SIZE 19' AS SIZE,RUN_SZ19  FROM def_szr WHERE RUN_SZ19 != '' UNION 
        SELECT CLASS_CD, 20 AS NUMBER,'SIZE 20' AS SIZE,RUN_SZ20  FROM def_szr WHERE RUN_SZ20 != ''
        )'''

    temp_pre_pack = f'''
        (SELECT CLASS_CD,INV_SZ, 1 AS NUMBER, 'SIZE 1' AS SIZE, SIZE_RUN1  FROM rsz_file WHERE SIZE_RUN1 != '' UNION
        SELECT CLASS_CD,INV_SZ, 2 AS NUMBER,'SIZE 2' AS SIZE,SIZE_RUN2  FROM rsz_file WHERE SIZE_RUN2 != '' UNION
        SELECT CLASS_CD,INV_SZ, 3 AS NUMBER,'SIZE 3' AS SIZE,SIZE_RUN3  FROM rsz_file WHERE SIZE_RUN3 != '' UNION
        SELECT CLASS_CD,INV_SZ, 4 AS NUMBER,'SIZE 4' AS SIZE,SIZE_RUN4  FROM rsz_file WHERE SIZE_RUN4 != '' UNION
        SELECT CLASS_CD,INV_SZ, 5 AS NUMBER,'SIZE 5' AS SIZE,SIZE_RUN5  FROM rsz_file WHERE SIZE_RUN5 != '' UNION
        SELECT CLASS_CD,INV_SZ, 6 AS NUMBER,'SIZE 6' AS SIZE,SIZE_RUN6  FROM rsz_file WHERE SIZE_RUN6 != '' UNION
        SELECT CLASS_CD,INV_SZ, 7 AS NUMBER,'SIZE 7' AS SIZE,SIZE_RUN7  FROM rsz_file WHERE SIZE_RUN7 != '' UNION
        SELECT CLASS_CD,INV_SZ, 8 AS NUMBER,'SIZE 8' AS SIZE,SIZE_RUN8  FROM rsz_file WHERE SIZE_RUN8 != '' UNION
        SELECT CLASS_CD,INV_SZ, 9 AS NUMBER,'SIZE 9' AS SIZE,SIZE_RUN9  FROM rsz_file WHERE SIZE_RUN9 != '' UNION
        SELECT CLASS_CD,INV_SZ, 10 AS NUMBER,'SIZE 10' AS SIZE,SIZE_RUN10  FROM rsz_file WHERE SIZE_RUN10 != '' UNION
        SELECT CLASS_CD,INV_SZ, 11 AS NUMBER,'SIZE 11' AS SIZE,SIZE_RUN11  FROM rsz_file WHERE SIZE_RUN11 != '' UNION
        SELECT CLASS_CD,INV_SZ, 12 AS NUMBER,'SIZE 12' AS SIZE,SIZE_RUN12  FROM rsz_file WHERE SIZE_RUN12 != '' UNION
        SELECT CLASS_CD,INV_SZ, 13 AS NUMBER,'SIZE 13' AS SIZE,SIZE_RUN13  FROM rsz_file WHERE SIZE_RUN13 != '' UNION
        SELECT CLASS_CD,INV_SZ, 14 AS NUMBER,'SIZE 14' AS SIZE,SIZE_RUN14  FROM rsz_file WHERE SIZE_RUN14 != '' UNION
        SELECT CLASS_CD,INV_SZ, 15 AS NUMBER,'SIZE 15' AS SIZE,SIZE_RUN15  FROM rsz_file WHERE SIZE_RUN15 != '' UNION
        SELECT CLASS_CD,INV_SZ, 16 AS NUMBER,'SIZE 16' AS SIZE,SIZE_RUN16  FROM rsz_file WHERE SIZE_RUN16 != '' UNION
        SELECT CLASS_CD,INV_SZ, 17 AS NUMBER,'SIZE 17' AS SIZE,SIZE_RUN17  FROM rsz_file WHERE SIZE_RUN17 != '' UNION
        SELECT CLASS_CD,INV_SZ, 18 AS NUMBER,'SIZE 18' AS SIZE,SIZE_RUN18  FROM rsz_file WHERE SIZE_RUN18 != '' UNION
        SELECT CLASS_CD,INV_SZ, 19 AS NUMBER,'SIZE 19' AS SIZE,SIZE_RUN19  FROM rsz_file WHERE SIZE_RUN19 != '' UNION
        SELECT CLASS_CD,INV_SZ, 20 AS NUMBER,'SIZE 20' AS SIZE,SIZE_RUN20  FROM rsz_file WHERE SIZE_RUN20 != ''
        )'''

    temp_open_size_run_orders = f'''(SELECT DISTINCT (ORD_NUM * 10) as ORD_NUM FROM ORD_LOG A  WHERE A.RUN_CD = 'X' and ORDER_QTY != INVS_QTY)'''

    temp_no_size_po = f'''
        (
        select PO_NUM, 'X' as class_cd, run_cd, 1 as Number, 'Size1' as Size, run_tbl1 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl1 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 2 as Number, 'Size2' as Size, run_tbl2 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl2 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 3 as Number, 'Size3' as Size, run_tbl3 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl3 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 4 as Number, 'Size4' as Size, run_tbl4 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl4 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 5 as Number, 'Size5' as Size, run_tbl5 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl5 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 6 as Number, 'Size6' as Size, run_tbl6 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl6 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 7 as Number, 'Size7' as Size, run_tbl7 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl7 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 8 as Number, 'Size8' as Size, run_tbl8 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl8 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 9 as Number, 'Size9' as Size, run_tbl9 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl9 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 10 as Number, 'Size10' as Size, run_tbl10 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl10 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 11 as Number, 'Size11' as Size, run_tbl11 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl11 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 12 as Number, 'Size12' as Size, run_tbl12 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl12 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 13 as Number, 'Size13' as Size, run_tbl13 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl13 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 14 as Number, 'Size14' as Size, run_tbl14 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl14 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 15 as Number, 'Size15' as Size, run_tbl15 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl15 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 16 as Number, 'Size16' as Size, run_tbl16 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl16 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 17 as Number, 'Size17' as Size, run_tbl17 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl17 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 18 as Number, 'Size18' as Size, run_tbl18 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl18 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 19 as Number, 'Size19' as Size, run_tbl19 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl19 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 20 as Number, 'Size20' as Size, run_tbl20 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl20 >0
        )'''

    temp_no_size_order = f'''
        (
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 1 as Number, 'Size1' as Size, run_tbl1 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl1 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 2 as Number, 'Size2' as Size, run_tbl2 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl2 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 3 as Number, 'Size3' as Size, run_tbl3 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl3 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 4 as Number, 'Size4' as Size, run_tbl4 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl4 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 5 as Number, 'Size5' as Size, run_tbl5 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl5 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 6 as Number, 'Size6' as Size, run_tbl6 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl6 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 7 as Number, 'Size7' as Size, run_tbl7 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl7 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 8 as Number, 'Size8' as Size, run_tbl8 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl8 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 9 as Number, 'Size9' as Size, run_tbl9 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl9 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 10 as Number, 'Size10' as Size, run_tbl10 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl10 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 11 as Number, 'Size11' as Size, run_tbl11 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl11 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 12 as Number, 'Size12' as Size, run_tbl12 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl12 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 13 as Number, 'Size13' as Size, run_tbl13 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl13 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 14 as Number, 'Size14' as Size, run_tbl14 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl14 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 15 as Number, 'Size15' as Size, run_tbl15 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl15 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 16 as Number, 'Size16' as Size, run_tbl16 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl16 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 17 as Number, 'Size17' as Size, run_tbl17 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl17 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 18 as Number, 'Size18' as Size, run_tbl18 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl18 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 19 as Number, 'Size19' as Size, run_tbl19 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl19 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 20 as Number, 'Size20' as Size, run_tbl20 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl20 >0
        )'''

    temp_no_size_order_shipments = f'''
            (
            select (INVS_NUM - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 1 as Number, 'Size1' as Size, run_tbl1 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl1 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 2 as Number, 'Size2' as Size, run_tbl2 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl2 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 3 as Number, 'Size3' as Size, run_tbl3 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl3 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 4 as Number, 'Size4' as Size, run_tbl4 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl4 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 5 as Number, 'Size5' as Size, run_tbl5 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl5 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 6 as Number, 'Size6' as Size, run_tbl6 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl6 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 7 as Number, 'Size7' as Size, run_tbl7 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl7 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 8 as Number, 'Size8' as Size, run_tbl8 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl8 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 9 as Number, 'Size9' as Size, run_tbl9 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl9 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 10 as Number, 'Size10' as Size, run_tbl10 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl10 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 11 as Number, 'Size11' as Size, run_tbl11 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl11 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 12 as Number, 'Size12' as Size, run_tbl12 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl12 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 13 as Number, 'Size13' as Size, run_tbl13 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl13 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 14 as Number, 'Size14' as Size, run_tbl14 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl14 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 15 as Number, 'Size15' as Size, run_tbl15 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl15 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 16 as Number, 'Size16' as Size, run_tbl16 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl16 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 17 as Number, 'Size17' as Size, run_tbl17 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl17 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 18 as Number, 'Size18' as Size, run_tbl18 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl18 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 19 as Number, 'Size19' as Size, run_tbl19 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl19 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 20 as Number, 'Size20' as Size, run_tbl20 as Qty from inszrun A inner join {temp_open_size_run_orders} B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl20 >0
            )'''

    return temp_size_run, temp_pre_pack, temp_open_size_run_orders, temp_no_size_po, temp_no_size_order, \
           temp_no_size_order_shipments

@error_handler
def setup_temporary_tables(engine, conn, data_directory, second_data_directory):
    scripts = []
    scripts.append(f'drop table if exists temp_size_run;')
    scripts.append(f'''CREATE TABLE  temp_size_run (
    CLASS_CD varchar(12),
    NUMBER int,
    SIZE varchar(12),
    RUN_SZ1 varchar(12),
    primary key (CLASS_CD, NUMBER)    
    );''')
    scripts.append(f'''insert into  temp_size_run
        select * FROM
        (SELECT CLASS_CD, 1 AS NUMBER, 'SIZE 1' AS SIZE,RUN_SZ1  FROM def_szr WHERE RUN_SZ1 != '' UNION 
        SELECT CLASS_CD, 2 AS NUMBER,'SIZE 2' AS SIZE,RUN_SZ2  FROM def_szr WHERE RUN_SZ2 != '' UNION 
        SELECT CLASS_CD, 3 AS NUMBER,'SIZE 3' AS SIZE,RUN_SZ3  FROM def_szr WHERE RUN_SZ3 != '' UNION 
        SELECT CLASS_CD, 4 AS NUMBER,'SIZE 4' AS SIZE,RUN_SZ4  FROM def_szr WHERE RUN_SZ4 != '' UNION 
        SELECT CLASS_CD, 5 AS NUMBER,'SIZE 5' AS SIZE,RUN_SZ5  FROM def_szr WHERE RUN_SZ5 != '' UNION 
        SELECT CLASS_CD, 6 AS NUMBER,'SIZE 6' AS SIZE,RUN_SZ6  FROM def_szr WHERE RUN_SZ6 != '' UNION 
        SELECT CLASS_CD, 7 AS NUMBER,'SIZE 7' AS SIZE,RUN_SZ7  FROM def_szr WHERE RUN_SZ7 != '' UNION 
        SELECT CLASS_CD, 8 AS NUMBER,'SIZE 8' AS SIZE,RUN_SZ8  FROM def_szr WHERE RUN_SZ8 != '' UNION 
        SELECT CLASS_CD, 9 AS NUMBER,'SIZE 9' AS SIZE,RUN_SZ9  FROM def_szr WHERE RUN_SZ9 != '' UNION 
        SELECT CLASS_CD, 10 AS NUMBER,'SIZE 10' AS SIZE,RUN_SZ10  FROM def_szr WHERE RUN_SZ10 != '' UNION 
        SELECT CLASS_CD, 11 AS NUMBER,'SIZE 11' AS SIZE,RUN_SZ11  FROM def_szr WHERE RUN_SZ11 != '' UNION 
        SELECT CLASS_CD, 12 AS NUMBER,'SIZE 12' AS SIZE,RUN_SZ12  FROM def_szr WHERE RUN_SZ12 != '' UNION 
        SELECT CLASS_CD, 13 AS NUMBER,'SIZE 13' AS SIZE,RUN_SZ13  FROM def_szr WHERE RUN_SZ13 != '' UNION 
        SELECT CLASS_CD, 14 AS NUMBER,'SIZE 14' AS SIZE,RUN_SZ14  FROM def_szr WHERE RUN_SZ14 != '' UNION 
        SELECT CLASS_CD, 15 AS NUMBER,'SIZE 15' AS SIZE,RUN_SZ15  FROM def_szr WHERE RUN_SZ15 != '' UNION 
        SELECT CLASS_CD, 16 AS NUMBER,'SIZE 16' AS SIZE,RUN_SZ16  FROM def_szr WHERE RUN_SZ16 != '' UNION 
        SELECT CLASS_CD, 17 AS NUMBER,'SIZE 17' AS SIZE,RUN_SZ17  FROM def_szr WHERE RUN_SZ17 != '' UNION 
        SELECT CLASS_CD, 18 AS NUMBER,'SIZE 18' AS SIZE,RUN_SZ18  FROM def_szr WHERE RUN_SZ18 != '' UNION 
        SELECT CLASS_CD, 19 AS NUMBER,'SIZE 19' AS SIZE,RUN_SZ19  FROM def_szr WHERE RUN_SZ19 != '' UNION 
        SELECT CLASS_CD, 20 AS NUMBER,'SIZE 20' AS SIZE,RUN_SZ20  FROM def_szr WHERE RUN_SZ20 != ''
        ) A ORDER BY CLASS_CD, NUMBER;''')

    scripts.append(f'DROP TABLE IF EXISTS temp_pre_pack;')
    scripts.append(f'''CREATE TABLE  temp_pre_pack (
    CLASS_CD varchar(12),
	INV_SZ varchar(12),
    NUMBER int,
    SIZE varchar(12),
    SIZE_RUN1 int,
	PRIMARY KEY(CLASS_CD, INV_SZ, NUMBER)
	);''')

    scripts.append(f'''insert into temp_pre_pack
        SELECT * FROM
        (SELECT CLASS_CD,INV_SZ, 1 AS NUMBER, 'SIZE 1' AS SIZE, SIZE_RUN1  FROM rsz_file WHERE SIZE_RUN1 != '' UNION
        SELECT CLASS_CD,INV_SZ, 2 AS NUMBER,'SIZE 2' AS SIZE,SIZE_RUN2  FROM rsz_file WHERE SIZE_RUN2 != '' UNION
        SELECT CLASS_CD,INV_SZ, 3 AS NUMBER,'SIZE 3' AS SIZE,SIZE_RUN3  FROM rsz_file WHERE SIZE_RUN3 != '' UNION
        SELECT CLASS_CD,INV_SZ, 4 AS NUMBER,'SIZE 4' AS SIZE,SIZE_RUN4  FROM rsz_file WHERE SIZE_RUN4 != '' UNION
        SELECT CLASS_CD,INV_SZ, 5 AS NUMBER,'SIZE 5' AS SIZE,SIZE_RUN5  FROM rsz_file WHERE SIZE_RUN5 != '' UNION
        SELECT CLASS_CD,INV_SZ, 6 AS NUMBER,'SIZE 6' AS SIZE,SIZE_RUN6  FROM rsz_file WHERE SIZE_RUN6 != '' UNION
        SELECT CLASS_CD,INV_SZ, 7 AS NUMBER,'SIZE 7' AS SIZE,SIZE_RUN7  FROM rsz_file WHERE SIZE_RUN7 != '' UNION
        SELECT CLASS_CD,INV_SZ, 8 AS NUMBER,'SIZE 8' AS SIZE,SIZE_RUN8  FROM rsz_file WHERE SIZE_RUN8 != '' UNION
        SELECT CLASS_CD,INV_SZ, 9 AS NUMBER,'SIZE 9' AS SIZE,SIZE_RUN9  FROM rsz_file WHERE SIZE_RUN9 != '' UNION
        SELECT CLASS_CD,INV_SZ, 10 AS NUMBER,'SIZE 10' AS SIZE,SIZE_RUN10  FROM rsz_file WHERE SIZE_RUN10 != '' UNION
        SELECT CLASS_CD,INV_SZ, 11 AS NUMBER,'SIZE 11' AS SIZE,SIZE_RUN11  FROM rsz_file WHERE SIZE_RUN11 != '' UNION
        SELECT CLASS_CD,INV_SZ, 12 AS NUMBER,'SIZE 12' AS SIZE,SIZE_RUN12  FROM rsz_file WHERE SIZE_RUN12 != '' UNION
        SELECT CLASS_CD,INV_SZ, 13 AS NUMBER,'SIZE 13' AS SIZE,SIZE_RUN13  FROM rsz_file WHERE SIZE_RUN13 != '' UNION
        SELECT CLASS_CD,INV_SZ, 14 AS NUMBER,'SIZE 14' AS SIZE,SIZE_RUN14  FROM rsz_file WHERE SIZE_RUN14 != '' UNION
        SELECT CLASS_CD,INV_SZ, 15 AS NUMBER,'SIZE 15' AS SIZE,SIZE_RUN15  FROM rsz_file WHERE SIZE_RUN15 != '' UNION
        SELECT CLASS_CD,INV_SZ, 16 AS NUMBER,'SIZE 16' AS SIZE,SIZE_RUN16  FROM rsz_file WHERE SIZE_RUN16 != '' UNION
        SELECT CLASS_CD,INV_SZ, 17 AS NUMBER,'SIZE 17' AS SIZE,SIZE_RUN17  FROM rsz_file WHERE SIZE_RUN17 != '' UNION
        SELECT CLASS_CD,INV_SZ, 18 AS NUMBER,'SIZE 18' AS SIZE,SIZE_RUN18  FROM rsz_file WHERE SIZE_RUN18 != '' UNION
        SELECT CLASS_CD,INV_SZ, 19 AS NUMBER,'SIZE 19' AS SIZE,SIZE_RUN19  FROM rsz_file WHERE SIZE_RUN19 != '' UNION
        SELECT CLASS_CD,INV_SZ, 20 AS NUMBER,'SIZE 20' AS SIZE,SIZE_RUN20  FROM rsz_file WHERE SIZE_RUN20 != ''
        ) A
        ORDER BY CLASS_CD, NUMBER;''')


    scripts.append(f'DROP TABLE if exists temp_open_size_run_orders;')
    scripts.append(f'''CREATE TABLE  temp_open_size_run_orders (
        ORD_NUM varchar(12),
        PRIMARY KEY(ORD_NUM)
        );''')
    scripts.append(f'''insert into temp_open_size_run_orders
        SELECT DISTINCT (ORD_NUM * 10) FROM ORD_LOG A 
        WHERE A.RUN_CD = 'X'
        and ORDER_QTY != INVS_QTY;        
        ''')

    scripts.append(f'DROP TABLE temp_no_size_po;')
    scripts.append(f'''CREATE TABLE  temp_no_size_po (
        PO_NUM varchar(12),
        class_cd varchar(12),
        run_cd int,
        Number INT,
        SIZE varchar(12),
        Qty INT,
        PRIMARY KEY(po_num, run_cd, Number)
        );''')


    scripts.append(f'''insert into temp_no_size_po
        select * from
        (
        select PO_NUM, 'X' as class_cd, run_cd, 1 as Number, 'Size1' as Size, run_tbl1 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl1 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 2 as Number, 'Size2' as Size, run_tbl2 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl2 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 3 as Number, 'Size3' as Size, run_tbl3 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl3 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 4 as Number, 'Size4' as Size, run_tbl4 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl4 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 5 as Number, 'Size5' as Size, run_tbl5 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl5 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 6 as Number, 'Size6' as Size, run_tbl6 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl6 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 7 as Number, 'Size7' as Size, run_tbl7 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl7 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 8 as Number, 'Size8' as Size, run_tbl8 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl8 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 9 as Number, 'Size9' as Size, run_tbl9 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl9 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 10 as Number, 'Size10' as Size, run_tbl10 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl10 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 11 as Number, 'Size11' as Size, run_tbl11 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl11 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 12 as Number, 'Size12' as Size, run_tbl12 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl12 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 13 as Number, 'Size13' as Size, run_tbl13 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl13 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 14 as Number, 'Size14' as Size, run_tbl14 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl14 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 15 as Number, 'Size15' as Size, run_tbl15 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl15 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 16 as Number, 'Size16' as Size, run_tbl16 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl16 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 17 as Number, 'Size17' as Size, run_tbl17 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl17 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 18 as Number, 'Size18' as Size, run_tbl18 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl18 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 19 as Number, 'Size19' as Size, run_tbl19 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl19 >0 union
        select PO_NUM, 'X' as class_cd, run_cd, 20 as Number, 'Size20' as Size, run_tbl20 as Qty from poszrun where po_type = 0 and bch_num = 0 and run_tbl20 >0
        ) A
        order by PO_NUM,run_cd,  Number;''')

    scripts.append(f'DROP TABLE if exists temp_no_size_order;')
    scripts.append(f'''CREATE TABLE  temp_no_size_order (
        ORD_NUM varchar(12),
		RUN_CD int,
        class_cd varchar(12),
        Number INT,
        SIZE varchar(12),
        Qty INT,
        PRIMARY KEY(ORD_NUM,RUN_CD,  Number)
        );
 
''')
    scripts.append(f'''
       insert into temp_no_size_order
        select * from
        (
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 1 as Number, 'Size1' as Size, run_tbl1 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl1 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 2 as Number, 'Size2' as Size, run_tbl2 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl2 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 3 as Number, 'Size3' as Size, run_tbl3 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl3 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 4 as Number, 'Size4' as Size, run_tbl4 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl4 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 5 as Number, 'Size5' as Size, run_tbl5 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl5 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 6 as Number, 'Size6' as Size, run_tbl6 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl6 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 7 as Number, 'Size7' as Size, run_tbl7 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl7 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 8 as Number, 'Size8' as Size, run_tbl8 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl8 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 9 as Number, 'Size9' as Size, run_tbl9 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl9 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 10 as Number, 'Size10' as Size, run_tbl10 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl10 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 11 as Number, 'Size11' as Size, run_tbl11 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl11 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 12 as Number, 'Size12' as Size, run_tbl12 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl12 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 13 as Number, 'Size13' as Size, run_tbl13 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl13 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 14 as Number, 'Size14' as Size, run_tbl14 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl14 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 15 as Number, 'Size15' as Size, run_tbl15 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl15 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 16 as Number, 'Size16' as Size, run_tbl16 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl16 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 17 as Number, 'Size17' as Size, run_tbl17 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl17 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 18 as Number, 'Size18' as Size, run_tbl18 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl18 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 19 as Number, 'Size19' as Size, run_tbl19 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl19 >0 union
        select INVS_NUM / 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 20 as Number, 'Size20' as Size, run_tbl20 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM = B.ORD_NUM where INVS_TYPE = 2 and run_tbl20 >0
        ) A
        order by ORD_NUM,  Number;
''')

    scripts.append(f'DROP TABLE if exists temp_no_size_order_shipments;')
    scripts.append(f'''CREATE TABLE  temp_no_size_order_shipments (
            ORD_NUM varchar(12),
    		RUN_CD int,
            class_cd varchar(12),
            Number INT,
            SIZE varchar(12),
            Qty INT,
            PRIMARY KEY(ORD_NUM,RUN_CD,  Number)
            );

    ''')
    scripts.append(f'''
           insert into temp_no_size_order_shipments
            select * from
            (
            select (INVS_NUM - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 1 as Number, 'Size1' as Size, run_tbl1 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl1 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 2 as Number, 'Size2' as Size, run_tbl2 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl2 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 3 as Number, 'Size3' as Size, run_tbl3 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl3 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 4 as Number, 'Size4' as Size, run_tbl4 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl4 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 5 as Number, 'Size5' as Size, run_tbl5 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl5 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 6 as Number, 'Size6' as Size, run_tbl6 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl6 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 7 as Number, 'Size7' as Size, run_tbl7 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl7 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 8 as Number, 'Size8' as Size, run_tbl8 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl8 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 9 as Number, 'Size9' as Size, run_tbl9 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl9 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 10 as Number, 'Size10' as Size, run_tbl10 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl10 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 11 as Number, 'Size11' as Size, run_tbl11 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl11 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 12 as Number, 'Size12' as Size, run_tbl12 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl12 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 13 as Number, 'Size13' as Size, run_tbl13 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl13 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 14 as Number, 'Size14' as Size, run_tbl14 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl14 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 15 as Number, 'Size15' as Size, run_tbl15 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl15 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 16 as Number, 'Size16' as Size, run_tbl16 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl16 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 17 as Number, 'Size17' as Size, run_tbl17 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl17 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 18 as Number, 'Size18' as Size, run_tbl18 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl18 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 19 as Number, 'Size19' as Size, run_tbl19 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl19 >0 union
            select (INVS_NUM  - 1)/ 10  as ORD_NUM,RUN_CD, 'X' as class_cd, 20 as Number, 'Size20' as Size, run_tbl20 as Qty from inszrun A inner join temp_open_size_run_orders B on A.INVS_NUM-1 = B.ORD_NUM where INVS_TYPE = 2 and run_tbl20 >0
            ) A
            order by ORD_NUM,  Number;
    ''')

    run_sql_scripts(engine=conn, scripts=scripts)

    map_module_setting(engine=engine, category='recruit files', module='setup_temporary_tables', sub_module='',
                       data_type='temoprary tables')


@error_handler
def recruit_style_master(engine, conn, data_directory, second_data_directory):
    temp_size_run, temp_pre_pack, temp_open_size_run_orders, temp_no_size_po, temp_no_size_order, \
    temp_no_size_order_shipments = provide_temp_table_objects()
    scripts = f'''
     SELECT 
        TRIM(A.PROD_CD) AS STYLE, 
        TRIM(A.PROD_CLR) AS COLOR_CODE,
        TRIM(F.CLR_DESC) AS COLOR,
        TRIM(A.CLASS_CD) AS CLASS,
        TRIM(A.WHS_NUM) AS WHS_NUM,
        B.Number, 
        B.RUN_SZ1 as Size,
        E.SIZE_RUN1 AS PPK_PACK,
        E.INV_SZ AS INVENTORY_SIZE,
        A.PAIRS,
        A.UPC_NUM AS STYLE_COLOR_UPC,
        D.UPC_CD AS UPC,
        D.EXPANDED_UPC,
        TRIM(A.DESCRIP) AS DESCRIPTION, 
        convert(date,cast(C.CREATE_DT- 36163 as datetime)) as CREATE_DATE,
        A.LASTRCV_QTY, 
        TRIM(C.ACTIVE) AS ACTIVE,
        TRIM(C.TAX_IND) AS TAXABLE,
        TRIM(C.IMAGE_NM) AS IMAGE_FILE,
        TRIM(A.VENDOR) AS VENDOR,
        TRIM(C.BRD_NM) AS BRAND,
        A.PRICE_BASE,
        A.FRT_CUS,
        A.HNDL_FEE,
        A.PROD_DUTY,
        A.AVG_COST,
        ISNULL(C.SALES_COST,A.SALES_COST) AS SALES_COST,
        ISNULL(C.RETAIL_PRS,a.RETAIL_PRS) AS RETAIL_PRS,
        ISNULL(C.WHOLE_PRS, A.WHOLE_PRS) AS WHOLE_PRS,
		NT_1 as NOTE
        FROM inv_data A
        LEFT JOIN {temp_size_run} B ON A.CLASS_CD = B.CLASS_CD
        LEFT JOIN {temp_pre_pack} E ON B.CLASS_CD = E.CLASS_CD AND B.NUMBER = E.NUMBER
        LEFT JOIN INV C ON A.PROD_CD = C.PROD_CD
        LEFT JOIN (SELECT *,
            concat(TRIM(UPC_CD),CASE WHEN 
            (((cast(substring(UPC_CD,1,1) as int) + cast(substring(UPC_CD,3,1) as int) 
            + cast(substring(UPC_CD,5,1) as int) + cast(substring(UPC_CD,7,1) as int) 
            + cast(substring(UPC_CD,9,1) as int) + cast(substring(UPC_CD,11,1) as int)) * 3
            + cast(substring(UPC_CD,2,1) as int) + cast(substring(UPC_CD,4,1) as int) 
            + cast(substring(UPC_CD,6,1) as int) + cast(substring(UPC_CD,8,1) as int) 
            + cast(substring(UPC_CD,10,1) as int)) % 10) = 0 
			THEN 
			 (((cast(substring(UPC_CD,1,1) as int) + cast(substring(UPC_CD,3,1) as int) 
            + cast(substring(UPC_CD,5,1) as int) + cast(substring(UPC_CD,7,1) as int) 
            + cast(substring(UPC_CD,9,1) as int) + cast(substring(UPC_CD,11,1) as int)) * 3
            + cast(substring(UPC_CD,2,1) as int) + cast(substring(UPC_CD,4,1) as int) 
            + cast(substring(UPC_CD,6,1) as int) + cast(substring(UPC_CD,8,1) as int) 
            + cast(substring(UPC_CD,10,1) as int)) % 10)
			ELSE 10-
			 (((cast(substring(UPC_CD,1,1) as int) + cast(substring(UPC_CD,3,1) as int) 
            + cast(substring(UPC_CD,5,1) as int) + cast(substring(UPC_CD,7,1) as int) 
            + cast(substring(UPC_CD,9,1) as int) + cast(substring(UPC_CD,11,1) as int)) * 3
            + cast(substring(UPC_CD,2,1) as int) + cast(substring(UPC_CD,4,1) as int) 
            + cast(substring(UPC_CD,6,1) as int) + cast(substring(UPC_CD,8,1) as int) 
            + cast(substring(UPC_CD,10,1) as int)) % 10)
			END
			) as EXPANDED_UPC
            FROM prod_upc
            ) D ON a.PROD_CD = d.PROD_CD AND A.PROD_CLR = D.PROD_CLR AND B.RUN_SZ1 = D.SIZE_NUM
        LEFT JOIN CLR_FILE F ON A.PROD_CLR = F.PROD_CLR
        order by A.PROD_CD, A.PROD_CLR,A.WHS_NUM, A.CLASS_CD, B.NUMBER;'''
    start_time = time.time()
    print_color(f'Attempting To Recruit Style Master Data', color='y')
    df = pd.read_sql(scripts, con=conn)
    df.to_csv(f'{data_directory}\\style_master.csv', index=False)
    df.to_csv(f'{second_data_directory}\\style_master.csv', index=False)

    end_time = time.time()
    print_color(f'Style Master Data Exported: Took {end_time-start_time} Seconds To Complete', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_style_master', sub_module='',
                       data_type='style master')


@error_handler
def recruit_purchase_order_data(engine, conn, data_directory, second_data_directory):
    temp_size_run, temp_pre_pack, temp_open_size_run_orders, temp_no_size_po, temp_no_size_order, \
    temp_no_size_order_shipments = provide_temp_table_objects()
    scripts = f'''
         select 'Size Run' as Type, 
            convert(date,cast(A.PUR_DT- 36163 as datetime)) AS ORDER_DATE, 
			convert(date,cast(B.LOG_DATE- 36163 as datetime)) AS LOG_DATE, 
            convert(date,cast(B.EST_DT- 36163 as datetime)) AS EST_DATE, 
             A.PUR_NUM, b.BATCH_NUM, B.NT_NUM,B.COMM_LN,  H.Pur_NT as Container_Num,
            row_number() over(partition by a.pur_num, B.prod_cd, B.prod_clr, B.BATCH_NUM, B.NT_NUM,B.COMM_LN order by  TRIM(B.PROD_CD), TRIM(B.PROD_CLR), D.NUMBER) as Purchase_ID,
            A.PUR_AMT, A.PUR_TAX, A.PAID_AMT, A.WHS_NUM, A.SALES_NUM, A.CUS_ID ,
            TRIM(b.VEN_ID) AS VENDOR, B.PUR_CD, TRIM(B.PROD_CD) AS STYLE, TRIM(B.PROD_CLR) AS COLOR_CODE, TRIM(G.CLR_DESC) AS COLOR, TRIM(B.RUN_CD) AS RUN_CD, 
            TRIM(C.CLASS_CD) AS CLASS_CD, E.RUN_SZ1 AS Size, C.PAIRS, F.PREPACK_QTY,F.Size_Count, 
            D.NUMBER, D.SIZE_RUN1, B.LOG_QTY as Total_Order_Qty, B.Hdl_chg AS Total_Receive_Qty,  b.CAN_QTY as Total_Cancel_Qty,
            ROUND(case when B.LOG_QTY >0 and F.PREPACK_QTY  >0 then  (CAST(B.LOG_QTY AS DECIMAL) / CAST(F.PREPACK_QTY AS DECIMAL)) *  CAST(D.SIZE_RUN1 AS DECIMAL)
                else B.LOG_QTY  end,2) as Order_Qty,
            B.Base_cost as Unit_Cost, 
            B.Base_cost * case when B.LOG_QTY >0 and F.PREPACK_QTY  >0 then  (CAST(B.LOG_QTY AS DECIMAL) / CAST(F.PREPACK_QTY AS DECIMAL)) *  CAST(D.SIZE_RUN1 AS DECIMAL)
                else B.LOG_QTY  end as Cost,
            ROUND(case when B.LOG_QTY >0 and F.PREPACK_QTY  >0 then  (CAST(B.Hdl_chg AS DECIMAL) / CAST(F.PREPACK_QTY AS DECIMAL)) *  CAST(D.SIZE_RUN1 AS DECIMAL)
                else B.Hdl_chg  end,2) as Received_Qty
            from pur_ord A 
            LEFT JOIN plog B ON A.PUR_NUM = B.PUR_NUM
            LEFT JOIN (select prod_cd, prod_clr, min(CLASS_CD)as CLASS_CD, max(pairs) as pairs from inv_data where WHS_NUM = '01' group by prod_cd, prod_clr) C ON B.PROD_CD = C.PROD_CD AND B.PROD_CLR = C.PROD_CLR
            LEFT JOIN {temp_pre_pack} D ON C.CLASS_CD = D.CLASS_CD AND B.RUN_CD= D.INV_SZ
            LEFT JOIN {temp_size_run} E ON D.CLASS_CD = E.CLASS_CD AND D.NUMBER = E.NUMBER
            LEFT JOIN (SELECT CLASS_CD, INV_SZ, count(a.SIZE_RUN1) as Size_Count, SUM(a.SIZE_RUN1) AS PREPACK_QTY FROM {temp_pre_pack} A GROUP BY CLASS_CD, INV_SZ) F ON D.CLASS_CD = F.CLASS_CD AND  D.INV_SZ = F.INV_SZ
            LEFT JOIN CLR_FILE G ON B.PROD_CLR = G.PROD_CLR
			left join pur_lnt H on B.PUR_NUM = H.PUR_NUM and B.NT_Num = H.nt_num
            where RUN_CD != 'X' 
            and B.pur_cd = 1
            and convert(date,cast(A.PUR_DT- 36163 as datetime)) > convert(date,(concat(year(getdate())-20,'-01-01')))
        UNION
            select 'No Size Run' as Type, 
            convert(date,cast(A.PUR_DT- 36163 as datetime)) AS ORDER_DATE, 
            convert(date,cast(B.LOG_DATE- 36163 as datetime)) AS LOG_DATE, 
            convert(date,cast(B.EST_DT- 36163 as datetime)) AS EST_DATE, 
            A.PUR_NUM, b.BATCH_NUM, B.NT_NUM,B.COMM_LN, I.Pur_NT as Container_Num,
            row_number() over(partition by a.pur_num, B.prod_cd, B.prod_clr, B.BATCH_NUM, B.NT_NUM,B.COMM_LN order by  TRIM(B.PROD_CD), TRIM(B.PROD_CLR), g.NUMBER) as Purchase_ID,
            A.PUR_AMT, A.PUR_TAX, A.PAID_AMT, A.WHS_NUM, A.SALES_NUM, A.CUS_ID ,
            TRIM(b.VEN_ID) AS VENDOR, B.PUR_CD, TRIM(B.PROD_CD) AS STYLE, TRIM(B.PROD_CLR) AS COLOR_CODE,  TRIM(H.CLR_DESC) AS COLOR,  TRIM(B.RUN_CD) AS RUN_CD, TRIM(C.CLASS_CD) AS CLASS_CD,E.RUN_SZ1 AS SIZE, C.PAIRS,  F.PREPACK_QTY, F.Size_Count,
            G.NUMBER, 0 as SIZE_RUN1, B.LOG_QTY as Total_Order_Qty, B.Hdl_chg as Total_Receive_Qty, b.CAN_QTY as Total_Cancel_Qty,
            G.QTY as Order_Qty, 
            B.Base_cost as Unit_Cost, 
            B.Base_cost  * G.QTY as Cost,
            (CAST(G.QTY as float) /  B.LOG_QTY) * B.Hdl_chg as Received_Qty
            from pur_ord A 
            LEFT JOIN plog B ON A.PUR_NUM = B.PUR_NUM
            LEFT JOIN (select prod_cd, prod_clr, min(CLASS_CD)as CLASS_CD, max(pairs) as pairs from inv_data where WHS_NUM = '01' group by prod_cd, prod_clr)  C ON B.PROD_CD = C.PROD_CD AND B.PROD_CLR = C.PROD_CLR
            -- LEFT JOIN temp_pre_pack D ON C.CLASS_CD = D.CLASS_CD
            LEFT JOIN {temp_no_size_po} G ON B.PUR_NUM = G.PO_NUM AND B.RUN_CD = G.class_cd AND B.NT_NUM = G.RUN_CD 
            LEFT JOIN {temp_size_run} E ON C.CLASS_CD = E.CLASS_CD AND G.NUMBER = E.NUMBER
            LEFT JOIN (SELECT CLASS_CD,count(a.SIZE_RUN1) as Size_Count, SUM(a.SIZE_RUN1) AS PREPACK_QTY FROM {temp_pre_pack} A GROUP BY CLASS_CD) F ON C.CLASS_CD = F.CLASS_CD
            LEFT JOIN CLR_FILE H ON B.PROD_CLR = H.PROD_CLR
			left join pur_lnt I on B.PUR_NUM = I.PUR_NUM and B.NT_Num = I.nt_num
            where b.RUN_CD = 'X' 
            and B.pur_cd = 1
            and convert(date,cast(A.PUR_DT- 36163 as datetime)) > convert(date,(concat(year(getdate())-20,'-01-01')));
'''
    start_time = time.time()
    print_color(f'Attempting To Recruit Purchase Order Data', color='y')
    df = pd.read_sql(scripts, con=conn)
    df.to_csv(f'{data_directory}\\po_data.csv', index=False)
    df.to_csv(f'{second_data_directory}\\po_data.csv', index=False)
    end_time = time.time()
    print_color(f'Purchase Order Data Exported: Took {end_time - start_time} Seconds To Complete', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_purchase_order_data', sub_module='',
                       data_type='purchase orders')


@error_handler
def recruit_received_purchase_order_data(engine, conn, data_directory, second_data_directory):
    temp_size_run, temp_pre_pack, temp_open_size_run_orders, temp_no_size_po, temp_no_size_order, \
    temp_no_size_order_shipments = provide_temp_table_objects()

    scripts = f'''
        select 'Size Run' as Type, 
            convert(date,cast(A.PUR_DT- 36163 as datetime)) AS ORDER_DATE, 
            convert(date,cast(B.LOG_DATE- 36163 as datetime)) AS LOG_DATE, 
            convert(date,cast(B.EST_DT- 36163 as datetime)) AS EST_DATE, 
            A.PUR_NUM, b.BATCH_NUM, B.NT_NUM,B.COMM_LN, 
            row_number() over(partition by a.pur_num, B.prod_cd, B.prod_clr, B.BATCH_NUM, B.NT_NUM,B.COMM_LN order by  TRIM(B.PROD_CD), TRIM(B.PROD_CLR), D.NUMBER) as Purchase_ID,
            A.PUR_AMT, A.PUR_TAX, A.PAID_AMT, A.WHS_NUM, A.SALES_NUM, A.CUS_ID ,
            TRIM(b.VEN_ID) AS VENDOR, B.PUR_CD, TRIM(B.PROD_CD) AS STYLE, TRIM(B.PROD_CLR) AS COLOR_CODE, TRIM(G.CLR_DESC) AS COLOR, TRIM(B.RUN_CD) AS RUN_CD, TRIM(C.CLASS_CD) AS CLASS_CD, E.RUN_SZ1 AS Size, C.PAIRS, F.PREPACK_QTY,F.Size_Count, 
            D.NUMBER, D.SIZE_RUN1, B.LOG_QTY as Total_Order_Qty, B.Hdl_chg AS Total_Receive_Qty,  b.CAN_QTY as Total_Cancel_Qty,
            ROUND(case when B.LOG_QTY >0 and F.PREPACK_QTY  >0 then  (CAST(B.LOG_QTY AS DECIMAL) / CAST(F.PREPACK_QTY AS DECIMAL)) *  CAST(D.SIZE_RUN1 AS DECIMAL)
                else B.LOG_QTY  end,2) as Order_Qty,
            B.Base_cost as Unit_Cost, 
            B.Base_cost * case when B.LOG_QTY >0 and F.PREPACK_QTY  >0 then  (CAST(B.LOG_QTY AS DECIMAL) / CAST(F.PREPACK_QTY AS DECIMAL)) *  CAST(D.SIZE_RUN1 AS DECIMAL)
                else B.LOG_QTY  end as Cost,
            ROUND(case when B.LOG_QTY >0 and F.PREPACK_QTY  >0 then  (CAST(B.LOG_QTY AS DECIMAL) / CAST(F.PREPACK_QTY AS DECIMAL)) *  CAST(D.SIZE_RUN1 AS DECIMAL)
                else B.LOG_QTY  end,2) as Received_Qty
            from pur_ord A 
            LEFT JOIN plog B ON A.PUR_NUM = B.PUR_NUM
            LEFT JOIN (select prod_cd, prod_clr, min(CLASS_CD)as CLASS_CD, max(pairs) as pairs from inv_data where WHS_NUM = '01' group by prod_cd, prod_clr) C ON B.PROD_CD = C.PROD_CD AND B.PROD_CLR = C.PROD_CLR
            LEFT JOIN {temp_pre_pack} D ON C.CLASS_CD = D.CLASS_CD AND B.RUN_CD= D.INV_SZ
            LEFT JOIN {temp_size_run} E ON D.CLASS_CD = E.CLASS_CD AND D.NUMBER = E.NUMBER
            LEFT JOIN (SELECT CLASS_CD, INV_SZ, count(a.SIZE_RUN1) as Size_Count, SUM(a.SIZE_RUN1) AS PREPACK_QTY FROM {temp_pre_pack} A GROUP BY CLASS_CD, INV_SZ) F ON D.CLASS_CD = F.CLASS_CD AND  D.INV_SZ = F.INV_SZ
            LEFT JOIN CLR_FILE G ON B.PROD_CLR = G.PROD_CLR
            where RUN_CD != 'X' 
            and pur_cd = 2
            and convert(date,cast(A.PUR_DT- 36163 as datetime)) > convert(date,(concat(year(getdate())-4,'-01-01')))

        UNION

        select 'No Size Run' as Type, 
            convert(date,cast(A.PUR_DT- 36163 as datetime)) AS ORDER_DATE, 
            convert(date,cast(B.LOG_DATE- 36163 as datetime)) AS LOG_DATE, 
            convert(date,cast(B.EST_DT- 36163 as datetime)) AS EST_DATE, 
            A.PUR_NUM, b.BATCH_NUM, B.NT_NUM,B.COMM_LN, 
            row_number() over(partition by a.pur_num, B.prod_cd, B.prod_clr, B.BATCH_NUM, B.NT_NUM,B.COMM_LN order by  TRIM(B.PROD_CD), TRIM(B.PROD_CLR), g.NUMBER) as Purchase_ID,
            A.PUR_AMT, A.PUR_TAX, A.PAID_AMT, A.WHS_NUM, A.SALES_NUM, A.CUS_ID ,
            TRIM(b.VEN_ID) AS VENDOR, B.PUR_CD, TRIM(B.PROD_CD) AS STYLE, TRIM(B.PROD_CLR) AS COLOR_CODE,  TRIM(H.CLR_DESC) AS COLOR,  TRIM(B.RUN_CD) AS RUN_CD, TRIM(C.CLASS_CD) AS CLASS_CD,E.RUN_SZ1 AS SIZE, C.PAIRS,  F.PREPACK_QTY, F.Size_Count,
            G.NUMBER, 0 as SIZE_RUN1, B.LOG_QTY as Total_Order_Qty, B.Hdl_chg as Total_Receive_Qty, b.CAN_QTY as Total_Cancel_Qty,
            G.QTY as Order_Qty, 
            B.Base_cost as Unit_Cost, 
            B.Base_cost  * G.QTY as Cost,
            G.QTY  as Received_Qty
            from pur_ord A 
            LEFT JOIN plog B ON A.PUR_NUM = B.PUR_NUM
            LEFT JOIN (select prod_cd, prod_clr, min(CLASS_CD)as CLASS_CD, max(pairs) as pairs from inv_data where WHS_NUM = '01' group by prod_cd, prod_clr)  C ON B.PROD_CD = C.PROD_CD AND B.PROD_CLR = C.PROD_CLR
            -- LEFT JOIN temp_pre_pack D ON C.CLASS_CD = D.CLASS_CD
            LEFT JOIN {temp_no_size_po} G ON B.PUR_NUM = G.PO_NUM AND B.RUN_CD = G.class_cd AND B.NT_NUM = G.RUN_CD 
            LEFT JOIN {temp_size_run} E ON C.CLASS_CD = E.CLASS_CD AND G.NUMBER = E.NUMBER
            LEFT JOIN (SELECT CLASS_CD,count(a.SIZE_RUN1) as Size_Count, SUM(a.SIZE_RUN1) AS PREPACK_QTY FROM {temp_pre_pack} A GROUP BY CLASS_CD) F ON C.CLASS_CD = F.CLASS_CD
            LEFT JOIN CLR_FILE H ON B.PROD_CLR = H.PROD_CLR
            where b.RUN_CD = 'X' 
            and pur_cd = 2
            and convert(date,cast(A.PUR_DT- 36163 as datetime)) > convert(date,(concat(year(getdate())-4,'-01-01')));'''
    start_time = time.time()
    print_color(f'Attempting To Recruit Purchase Order Data', color='y')
    df = pd.read_sql(scripts, con=conn)
    df.to_csv(f'{data_directory}\\received_po_data.csv', index=False)
    df.to_csv(f'{second_data_directory}\\received_po_data.csv', index=False)
    end_time = time.time()
    print_color(f'Received Purchase Orders Data Exported: Took {end_time - start_time} Seconds To Complete', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_received_purchase_order_data', sub_module='',
                       data_type='received purchase orders')


@error_handler
def recruit_open_order_data(engine, conn, data_directory, second_data_directory):
    temp_size_run, temp_pre_pack, temp_open_size_run_orders, temp_no_size_po, temp_no_size_order, \
    temp_no_size_order_shipments = provide_temp_table_objects()

    scripts = f'''SELECT 'Size Run' AS Type,
		convert(date,cast(A.OLG_DT- 36163 as datetime)) AS ORDER_DATE,
		A.ORD_NUM AS ORDER_NUMBER,
		B.CUS_ID AS CUSTOMER_ID,
		B.CUS_NM AS CUSTOMER,
		A.PROD_CD AS STYLE,
		A.PROD_CLR AS COLOR_CODE,
		G.CLR_DESC AS COLOR,
		E.RUN_SZ1 AS SIZE,
		A.WHS_NUM AS WAREHOUSE,
		A.ORDER_QTY AS TOTAL_ORDER_QTY,
		A.CAN_QTY AS TOTAL_CANCEL_QTY ,
		A.INVS_QTY AS TOTAL_INVOICED_QTY,
		(A.ORDER_QTY / F.PREPACK_QTY)*	D.SIZE_RUN1 AS ORDER_QTY,
		(A.CAN_QTY / F.PREPACK_QTY) *	D.SIZE_RUN1 AS CANCEL_QTY,
		(A.INVS_QTY / F.PREPACK_QTY)*	D.SIZE_RUN1 AS INVOICED_QTY,
		A.UNIT_PRS AS UNIT_PRICE,
		A.LOG_COST AS COST,
		A.SALES_NUM AS SALES_ID,
		AB.COMP_NM AS SALES_REP,
		convert(date,cast(A.SHIP_DT- 36163 as datetime)) AS SHIP_DATE,
		convert(date,cast(A.CAN_DT- 36163 as datetime)) AS CANCEL_DATE,
        A.NT_Num,
		A.RUN_CD AS RUN_CODE,
		C.CLASS_CD AS CLASS_CODE,
		D.NUMBER, 
		D.SIZE_RUN1,
		F.PREPACK_QTY
		FROM ord_log A
		LEFT JOIN customer b ON a.CUS_ID = b.CUS_ID
		LEFT JOIN sls_pro ab on A.SALES_NUM = ab.SALES_NUM
		LEFT JOIN (select prod_cd, prod_clr, min(CLASS_CD)as CLASS_CD, max(pairs) as pairs from inv_data where WHS_NUM = '01' group by prod_cd, prod_clr) C  ON A.PROD_CD = C.PROD_CD AND A.PROD_CLR = C.PROD_CLR
		LEFT JOIN {temp_pre_pack} D ON C.CLASS_CD = D.CLASS_CD AND A.RUN_CD= D.INV_SZ
		LEFT JOIN {temp_size_run} E ON D.CLASS_CD = E.CLASS_CD AND D.NUMBER = E.NUMBER
		LEFT JOIN (SELECT CLASS_CD, INV_SZ, count(a.SIZE_RUN1) as Size_Count, SUM(a.SIZE_RUN1) AS PREPACK_QTY FROM {temp_pre_pack} A GROUP BY CLASS_CD, INV_SZ) F ON D.CLASS_CD = F.CLASS_CD AND  D.INV_SZ = F.INV_SZ
		LEFT JOIN CLR_FILE G ON A.PROD_CLR = G.PROD_CLR
		WHERE A.RUN_CD != 'X'
		AND ORDER_QTY != INVS_QTY and INVS_QTY < ORDER_QTY
		union
		SELECT  'No Size Run' AS Type,
		convert(date,cast(A.OLG_DT- 36163 as datetime)) AS ORDER_DATE,
		A.ORD_NUM AS ORDER_NUMBER,
        B.CUS_ID AS CUSTOMER_ID,
		B.CUS_NM AS CUSTOMER,
		A.PROD_CD AS STYLE,
		A.PROD_CLR AS COLOR_CODE,
		G.CLR_DESC AS COLOR,
	    F.RUN_SZ1 AS SIZE,
		A.WHS_NUM AS WAREHOUSE,
		A.ORDER_QTY AS TOTAL_ORDER_QTY,
		A.CAN_QTY AS TOTAL_CANCEL_QTY ,
		A.INVS_QTY AS TOTAL_INVOICED_QTY,
		D.QTY AS ORDER_QTY,
		0 as CANCEL_QTY,
		E.qty as INVOICED_QTY,
		A.UNIT_PRS AS UNIT_PRICE,
		A.LOG_COST AS COST,
		A.SALES_NUM AS SALES_ID,
		AB.COMP_NM AS SALES_REP,
		convert(date,cast(A.SHIP_DT- 36163 as datetime)) AS SHIP_DATE,
		convert(date,cast(A.CAN_DT- 36163 as datetime)) AS CANCEL_DATE,
        A.NT_Num,
		A.RUN_CD AS RUN_CODE,
		C.CLASS_CD AS CLASS_CODE,
		D.NUMBER,
		0 as SIZE_RUN1,
		0 as PREPACK_QTY
		FROM ord_log A 
		LEFT JOIN customer b ON a.CUS_ID = b.CUS_ID
		LEFT JOIN sls_pro ab on A.SALES_NUM = ab.SALES_NUM
		LEFT JOIN (select prod_cd, prod_clr, min(CLASS_CD)as CLASS_CD, max(pairs) as pairs from inv_data where WHS_NUM = '01' group by prod_cd, prod_clr) C ON A.PROD_CD = C.PROD_CD AND A.PROD_CLR = C.PROD_CLR
		left join {temp_no_size_order} D on A.ORD_NUM =D.ORD_NUM and A.NT_NUM = D.run_cd
		left join {temp_no_size_order_shipments} E on A.ORD_NUM =E.ORD_NUM and A.NT_NUM = E.run_cd and D.Number = E.number
		left join {temp_size_run} F on C.CLASS_CD = F.CLASS_CD AND D.NUMBER = F.NUMBER
		LEFT JOIN CLR_FILE G ON A.PROD_CLR = G.PROD_CLR
		WHERE 
		A.RUN_CD = 'X'
		AND a.ORDER_QTY != a.INVS_QTY
		and (E.qty < D.qty or E.qty is null);
    '''
    start_time = time.time()
    print_color(f'Attempting To Open Orders Data', color='y')
    df = pd.read_sql(scripts, con=conn)
    df.to_csv(f'{data_directory}\\open_order_data.csv', index=False)
    df.to_csv(f'{second_data_directory}\\open_order_data.csv', index=False)
    end_time = time.time()
    print_color(f'Open Orders Exported: Took {end_time - start_time} Seconds To Complete', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_open_order_data', sub_module='',
                       data_type='open orders')


@error_handler
def recruit_color_codes(engine, conn, data_directory, second_data_directory):
    scripts = f'SELECT trim(PROD_CLR) as PROD_CLR, trim(CLR_DESC) as CLR_DESC FROM clr_file;'
    start_time = time.time()
    print_color(f'Attempting To Color Codes Data', color='y')

    df = pd.read_sql(scripts, con=conn)
    df.to_csv(f'{data_directory}\\color_codes.csv', index=False)
    df.to_csv(f'{second_data_directory}\\color_codes.csv', index=False)
    print_color(f'Color Code Data Exported', color='g')
    end_time = time.time()
    print_color(f'Color Codes Data Exported: Took {end_time - start_time} Seconds To Complete', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_color_codes', sub_module='',
                       data_type='color codes')

@error_handler
def recruit_size_breakdown(engine, conn, data_directory, second_data_directory):
    start_time = time.time()
    print_color(f'Attempting To Size Breakdown Data Data', color='y')

    df = pd.read_sql(f'Select * from def_szr', con=conn)
    df.to_csv(f'{data_directory}\\size_breakdown.csv', index=False)
    df.to_csv(f'{second_data_directory}\\size_breakdown.csv', index=False)
    end_time = time.time()
    print_color(f'Size Breakdown Data Exported: Took {end_time - start_time} Seconds To Complete', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_size_breakdown', sub_module='',
                       data_type='size breakdown')


@error_handler
def recruit_size_packs(engine, conn, data_directory, second_data_directory):
    start_time = time.time()
    print_color(f'Attempting To Size Pack Data', color='y')

    df = pd.read_sql(f'Select * from rsz_file', con=conn)
    df.to_csv(f'{data_directory}\\size_pack.csv', index=False)
    df.to_csv(f'{second_data_directory}\\size_pack.csv', index=False)
    end_time = time.time()
    print_color(f'Size Pack Data Exported: Took {end_time - start_time} Seconds To Complete', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_size_packs', sub_module='',
                       data_type='size packs')


@error_handler
def recruit_case_breakdown(engine, conn, data_directory, second_data_directory):
    script = f'''select *, concat(min_size,' - ',max_size) as Size_Run from
(SELECT a.class_cd, a.inv_sz,
	a.SIZE_RUN1 + a.SIZE_RUN2 + a.SIZE_RUN3 + a.SIZE_RUN4 + a.SIZE_RUN5 +
	a.SIZE_RUN6 + a.SIZE_RUN7 + a.SIZE_RUN8 + a.SIZE_RUN9 + a.SIZE_RUN10 +
	a.SIZE_RUN11 + a.SIZE_RUN12 + a.SIZE_RUN13 + a.SIZE_RUN14 + a.SIZE_RUN15 +
	a.SIZE_RUN16 + a.SIZE_RUN17 + a.SIZE_RUN18 + a.SIZE_RUN19 + a.SIZE_RUN20	
	as Pack_Qty,
    concat(
    case when B.RUN_SZ1 != '' then concat(B.RUN_SZ1, '  ') else '' end,
    case when B.RUN_SZ2 != '' then concat(B.RUN_SZ2,'  ') else '' end,
    case when B.RUN_SZ3 != '' then concat(B.RUN_SZ3,'  ') else '' end,
    case when B.RUN_SZ4 != '' then concat(B.RUN_SZ4,'  ') else '' end,
    case when B.RUN_SZ5 != '' then concat(B.RUN_SZ5,'  ') else '' end,
    case when B.RUN_SZ6 != '' then concat(B.RUN_SZ6,'  ') else '' end,
    case when B.RUN_SZ7 != '' then concat(B.RUN_SZ7,'  ') else '' end,
    case when B.RUN_SZ8 != '' then concat(B.RUN_SZ8,'  ') else '' end,
    case when B.RUN_SZ9 != '' then concat(B.RUN_SZ9,'  ') else '' end,
    case when B.RUN_SZ10 != '' then concat(B.RUN_SZ10,'  ') else '' end,
    case when B.RUN_SZ11 != '' then concat(B.RUN_SZ11,'  ') else '' end,
    case when B.RUN_SZ12 != '' then concat(B.RUN_SZ12,'  ') else '' end,
    case when B.RUN_SZ13 != '' then concat(B.RUN_SZ13,'  ') else '' end,
    case when B.RUN_SZ14 != '' then concat(B.RUN_SZ14,'  ') else '' end,
    case when B.RUN_SZ15 != '' then concat(B.RUN_SZ15,'  ') else '' end,
    case when B.RUN_SZ16 != '' then concat(B.RUN_SZ16,'  ') else '' end,
    case when B.RUN_SZ17 != '' then concat(B.RUN_SZ17,'  ') else '' end,
    case when B.RUN_SZ18 != '' then concat(B.RUN_SZ18,'  ') else '' end,
    case when B.RUN_SZ19 != '' then concat(B.RUN_SZ19,'  ') else '' end,
    case when B.RUN_SZ20 != '' then concat(B.RUN_SZ20,'  ') else '' end
    ) as Size_Breakdown,
    concat(
    case when a.SIZE_RUN1 >0 then concat(a.SIZE_RUN1,' ') else '' end,
    case when a.SIZE_RUN2 >0 then concat(a.SIZE_RUN2,' ') else '' end,
    case when a.SIZE_RUN3 >0 then concat(a.SIZE_RUN3,' ') else '' end,
    case when a.SIZE_RUN4 >0 then concat(a.SIZE_RUN4,' ') else '' end,
    case when a.SIZE_RUN5 >0 then concat(a.SIZE_RUN5,' ') else '' end,
    case when a.SIZE_RUN6 >0 then concat(a.SIZE_RUN6,' ') else '' end,
    case when a.SIZE_RUN7 >0 then concat(a.SIZE_RUN7,' ') else '' end,
    case when a.SIZE_RUN8 >0 then concat(a.SIZE_RUN8,' ') else '' end,
    case when a.SIZE_RUN9 >0 then concat(a.SIZE_RUN9,' ') else '' end,
    case when a.SIZE_RUN10 >0 then concat(a.SIZE_RUN10,' ') else '' end,
    case when a.SIZE_RUN11 >0 then concat(a.SIZE_RUN11,' ') else '' end,
    case when a.SIZE_RUN12 >0 then concat(a.SIZE_RUN12,' ') else '' end,
    case when a.SIZE_RUN13 >0 then concat(a.SIZE_RUN13,' ') else '' end,
    case when a.SIZE_RUN14 >0 then concat(a.SIZE_RUN14,' ') else '' end,
    case when a.SIZE_RUN15 >0 then concat(a.SIZE_RUN15,' ') else '' end,
    case when a.SIZE_RUN16 >0 then concat(a.SIZE_RUN16,' ') else '' end,
    case when a.SIZE_RUN17 >0 then concat(a.SIZE_RUN17,' ') else '' end,
    case when a.SIZE_RUN18 >0 then concat(a.SIZE_RUN18,' ') else '' end,
    case when a.SIZE_RUN19 >0 then concat(a.SIZE_RUN19,' ') else '' end,
    case when a.SIZE_RUN20 >0 then concat(a.SIZE_RUN20,' ') else '' end
    ) as Pack_Breakdown,
    case when B.RUN_SZ1 != '' then B.RUN_SZ1
		when B.RUN_SZ2 != '' then B.RUN_SZ2 
		when B.RUN_SZ3 != '' then B.RUN_SZ3 
		when B.RUN_SZ4 != '' then B.RUN_SZ4 
		when B.RUN_SZ5 != '' then B.RUN_SZ5 
		when B.RUN_SZ6 != '' then B.RUN_SZ6 
		when B.RUN_SZ7 != '' then B.RUN_SZ7 
		when B.RUN_SZ8 != '' then B.RUN_SZ8 
		when B.RUN_SZ9 != '' then B.RUN_SZ9 
		when B.RUN_SZ10 != '' then B.RUN_SZ10 
		when B.RUN_SZ11 != '' then B.RUN_SZ11 
		when B.RUN_SZ12 != '' then B.RUN_SZ12 
		when B.RUN_SZ13 != '' then B.RUN_SZ13 
		when B.RUN_SZ14 != '' then B.RUN_SZ14 
		when B.RUN_SZ15 != '' then B.RUN_SZ15 
		when B.RUN_SZ16 != '' then B.RUN_SZ16 
		when B.RUN_SZ17 != '' then B.RUN_SZ17 
		when B.RUN_SZ18 != '' then B.RUN_SZ18 
		when B.RUN_SZ19 != '' then B.RUN_SZ19 
		when B.RUN_SZ20 != '' then B.RUN_SZ20 
	end as min_size,
	case when B.RUN_SZ20 != '' then B.RUN_SZ20 
		when B.RUN_SZ19 != '' then B.RUN_SZ19 
		when B.RUN_SZ18 != '' then B.RUN_SZ18 
		when B.RUN_SZ17 != '' then B.RUN_SZ17 
		when B.RUN_SZ16 != '' then B.RUN_SZ16 
		when B.RUN_SZ15 != '' then B.RUN_SZ15 
		when B.RUN_SZ14 != '' then B.RUN_SZ14 
		when B.RUN_SZ13 != '' then B.RUN_SZ13 
		when B.RUN_SZ12 != '' then B.RUN_SZ12 
		when B.RUN_SZ11 != '' then B.RUN_SZ11 
		when B.RUN_SZ10 != '' then B.RUN_SZ10 
		when B.RUN_SZ9 != '' then B.RUN_SZ9 
		when B.RUN_SZ8 != '' then B.RUN_SZ8 
		when B.RUN_SZ7 != '' then B.RUN_SZ7 
		when B.RUN_SZ6 != '' then B.RUN_SZ6 
		when B.RUN_SZ5 != '' then B.RUN_SZ5 
		when B.RUN_SZ4 != '' then B.RUN_SZ4 
		when B.RUN_SZ3 != '' then B.RUN_SZ3 
		when B.RUN_SZ2 != '' then B.RUN_SZ2 
		when B.RUN_SZ1 != '' then B.RUN_SZ1
	end as max_size
    FROM  rsz_file a left join
    def_szr b on a.class_cd = b.class_cd) A
	;    
    '''
    start_time = time.time()
    print_color(f'Case Breakdown Data', color='y')

    df = pd.read_sql(script, con=conn)
    df.to_csv(f'{data_directory}\\case_breakdown.csv', index=False)
    df.to_csv(f'{second_data_directory}\\case_breakdown.csv', index=False)
    end_time = time.time()
    print_color(f'Case Breakdown Data Exported: Took {end_time - start_time} Seconds To Complete', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_case_breakdown', sub_module='',
                       data_type='case breakdown')



@error_handler
def recruit_po_by_size_data(engine, conn, data_directory, second_data_directory):

    script = f'''
    select A.*, B.INV_SZ, b.Size_Breakdown, b.Size_Pack_Qty, D.UPC_CD ,E.PAIRS, E.IMAGE_NM, E.WHOLE_PRS, F.AVG_COST, F.PRICE_BASE from
	(select * from
		(select por.*,  inv.Class_cd,             
		CASE 
		WHEN por.Number = 1 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl1  - ISNULL(poz1.run_tbl1, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run1
			end
		WHEN por.Number = 2 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl2  - ISNULL(poz1.run_tbl2, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run2
			END 
		WHEN por.Number = 3 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl3  - ISNULL(poz1.run_tbl3, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run3
			END
		WHEN por.Number = 4 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl4  - ISNULL(poz1.run_tbl4, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run4
			END
		WHEN por.Number = 5 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl5  - ISNULL(poz1.run_tbl5, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run5
			END	
		WHEN por.Number = 6 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl6  - ISNULL(poz1.run_tbl6, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run6
			END
		WHEN por.Number = 7 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl7  - ISNULL(poz1.run_tbl7, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run7
			END
		WHEN por.Number = 8 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl8  - ISNULL(poz1.run_tbl8, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run8
			END
		WHEN por.Number = 9 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl9  - ISNULL(poz1.run_tbl9, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run9
			END
		WHEN por.Number = 10 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl10 - ISNULL(poz1.run_tbl10, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run10
			END
		WHEN por.Number = 11 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl11 - ISNULL(poz1.run_tbl11, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run11
			END
		WHEN por.Number = 12 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl12 - ISNULL(poz1.run_tbl12, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run12
			END
		WHEN por.Number = 13 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl13 - ISNULL(poz1.run_tbl13, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run13
			END
		WHEN por.Number = 14 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl14 - ISNULL(poz1.run_tbl14, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run14
			END
		WHEN por.Number = 15 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl15 - ISNULL(poz1.run_tbl15, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run15
			END
		WHEN por.Number = 16 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl16 - ISNULL(poz1.run_tbl16, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run16
			END
		WHEN por.Number = 17 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl17 - ISNULL(poz1.run_tbl17, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run17
			END
		WHEN por.Number = 18 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl18 - ISNULL(poz1.run_tbl18, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run18
			END
		WHEN por.Number = 19 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl19 - ISNULL(poz1.run_tbl19, 0)
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run19
			END
		WHEN por.Number = 20 then
			CASE WHEN por.run_cd IN ('X','Y','Z') THEN
				poz.run_tbl20 - ISNULL(poz1.run_tbl20, 0) 
			ELSE
				(por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run20
			END
		end as PO_QTY

		from
			(select * from 
				(select 
				cast(LOG_DATE - 36163 as datetime) as LOG_DATE,
				cast(EST_DT - 36163 as datetime) as EST_DT,
				BATCH_NUM, 
				NT_NUM,
				pur_num,
				pur_cd,
				run_cd,
				prod_cd,
				prod_clr,
				whs_num,
				pur_lnt,
				comm_ln,
				ven_id,
				log_qty,
				hdl_chg,
				can_qty,
				log_qty - hdl_chg - can_qty as final_po_qty
				FROM plog AS por
				where pur_cd = 1 
				--and prod_cd = 'P051WB' and PROD_CLR = 'BLK' AND PUR_NUM = '30708A'
				AND log_qty - hdl_chg - can_qty > 0
				AND whs_num <= 'zzzzzz' AND whs_num >= ''
				) A
			cross join
				(select 1 as Number union select 2 union select 3
				union select 4 union select 5 union select 6
				union select 7 union select 8 union select 9
				union select 10 union select 11 union select 12
				union select 13 union select 14 union select 15
				union select 17 union select 18 union select 19
				union select 20) B) por
		INNER JOIN pur_ord AS pur ON por.pur_num = pur.pur_num
		INNER JOIN inv ON por.prod_cd = inv.prod_cd 
		LEFT JOIN rsz_file AS rsz ON rsz.class_cd = inv.class_cd AND rsz.inv_sz = por.run_cd AND por.run_cd NOT IN ('X','Y','Z') 
		LEFT JOIN poszrun AS poz ON poz.bch_num = 0  AND poz.po_type = 0 AND poz.po_num = por.pur_num AND poz.run_cd = por.nt_num 
		LEFT JOIN poszrun AS poz1 ON poz.bch_num = 0 AND poz1.po_type = 1 AND poz1.po_num = por.pur_num AND poz1.run_cd = por.nt_num
		where pur.type_cd <= 'zzzzzzzz' AND pur.type_cd >= '') A
	where PO_QTY != 0) A
	INNER JOIN
	(SELECT * FROM
            (
    select a.*,C.INV_SZ,
            case 
            when Number = 1 THEN B.RUN_SZ1 
            when Number = 2 THEN B.RUN_SZ2 
            when Number = 3 THEN B.RUN_SZ3 
            when Number = 4 THEN B.RUN_SZ4 
            when Number = 5 THEN B.RUN_SZ5
            when Number = 6 THEN B.RUN_SZ6
            when Number = 7 THEN B.RUN_SZ7
            when Number = 8 THEN B.RUN_SZ8
            when Number = 9 THEN B.RUN_SZ9 
            when Number = 10 THEN B.RUN_SZ10
            when Number = 11 THEN B.RUN_SZ11
            when Number = 12 THEN B.RUN_SZ12
            when Number = 13 THEN B.RUN_SZ13
            when Number = 14 THEN B.RUN_SZ14
            when Number = 15 THEN B.RUN_SZ15
            when Number = 16 THEN B.RUN_SZ16
            when Number = 17 THEN B.RUN_SZ17
            when Number = 18 THEN B.RUN_SZ18
            when Number = 19 THEN B.RUN_SZ19
            when Number = 20 THEN B.RUN_SZ20
            END as Size_Breakdown,
            case 
            when Number = 1 THEN C.SIZE_RUN1
            when Number = 2 THEN C.SIZE_RUN2
            when Number = 3 THEN C.SIZE_RUN3
            when Number = 4 THEN C.SIZE_RUN4
            when Number = 5 THEN C.SIZE_RUN5
            when Number = 6 THEN C.SIZE_RUN6
            when Number = 7 THEN C.SIZE_RUN7
            when Number = 8 THEN C.SIZE_RUN8
            when Number = 9 THEN C.SIZE_RUN9
            when Number = 10 THEN C.SIZE_RUN10
            when Number = 11 THEN C.SIZE_RUN11
            when Number = 12 THEN C.SIZE_RUN12
            when Number = 13 THEN C.SIZE_RUN13
            when Number = 14 THEN C.SIZE_RUN14
            when Number = 15 THEN C.SIZE_RUN15
            when Number = 16 THEN C.SIZE_RUN16
            when Number = 17 THEN C.SIZE_RUN17
            when Number = 18 THEN C.SIZE_RUN18
            when Number = 19 THEN C.SIZE_RUN19
            when Number = 20 THEN C.SIZE_RUN20
            END as Size_Pack_Qty
            from
            (select a.class_cd, b.Number from
                (select a.class_cd from def_szr a) A
                cross join 
                (select 1 as Number union select 2 union select 3
                union select 4 union select 5 union select 6
                union select 7 union select 8 union select 9
                union select 10 union select 11 union select 12
                union select 13 union select 14 union select 15
                union select 17 union select 18 union select 19
                union select 20) B
                ) A
                left join def_szr b on a.class_cd = b.class_cd
                left join 
				(SELECT * FROM (SELECT RANK() OVER (PARTITION BY CLASS_CD ORDER BY INV_SZ) AS RANKING, * FROM   rsz_file ) 
				a WHERE RANKING =1) c on a.class_cd = c.class_cd
    ) A
        WHERE NOT (Size_Breakdown= '' AND Size_Pack_Qty = 0)
		--AND CLASS_CD = '2-8 SH'
        ) B ON A.class_cd = B.class_cd AND A.NUMBER = B.NUMBER 
	LEFT JOIN prod_upc D ON A.PROD_CD = D.PROD_CD AND A.PROD_CLR = D.PROD_CLR AND B.Size_Breakdown = D.SIZE_NUM
    LEFT JOIN INV E on A.PROD_CD = E.PROD_CD
    LEFT JOIN (SELECT * FROM inv_data WHERE WHS_NUM = '01') F ON A.PROD_CD = F.PROD_CD AND A.PROD_CLR = F.PROD_CLR
	order by pur_num, prod_cd, prod_clr, comm_ln, A.NUMBER
	;'''
    start_time = time.time()
    print_color(f'PO Data By Size Data', color='y')

    df = pd.read_sql(script, con=conn)

    df.to_csv(f'{data_directory}\\po_data_by_size.csv', index=False)
    df.to_csv(f'{second_data_directory}\\po_data_by_size.csv', index=False)
    end_time = time.time()
    print_color(f'PO Data By Size Exported: Took {end_time - start_time} Seconds To Complete', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_po_by_size_data', sub_module='',
                       data_type='po by size')


@error_handler
def recruit_inventory_data(engine, conn, data_directory, second_data_directory):
    inventory_setup_script = f'''
     (select * from
            (select A.PROD_CD, A.DESCRIP,B.PROD_CLR, A.CLASS_CD, A.ACTIVE, A.TAX_IND AS TAXABLE,
            A.RETAIL_PRS, A.WHOLE_PRS, A.IMAGE_NM AS IMAGE, B.WHS_NUM, B.SZ_RUN, A.PAIRS
            from INV A
            LEFT JOIN 
            inv_data B ON A.PROD_CD = B.PROD_CD
            WHERE B.WHS_NUM = '01' 
            --AND A.PROD_CD = 'LA88046' and PROD_CLR = 'MUTL'
            ) A
        cross join
            (select 1 as Number union select 2 union select 3
            union select 4 union select 5 union select 6
            union select 7 union select 8 union select 9
            union select 10 union select 11 union select 12
            union select 13 union select 14 union select 15
            union select 17 union select 18 union select 19
            union select 20) B
            ) A'''
    size_run_breakdown_script = f'''
    select a.*,
            case 
            when Number = 1 THEN B.RUN_SZ1 
            when Number = 2 THEN B.RUN_SZ2 
            when Number = 3 THEN B.RUN_SZ3 
            when Number = 4 THEN B.RUN_SZ4 
            when Number = 5 THEN B.RUN_SZ5
            when Number = 6 THEN B.RUN_SZ6
            when Number = 7 THEN B.RUN_SZ7
            when Number = 8 THEN B.RUN_SZ8
            when Number = 9 THEN B.RUN_SZ9 
            when Number = 10 THEN B.RUN_SZ10
            when Number = 11 THEN B.RUN_SZ11
            when Number = 12 THEN B.RUN_SZ12
            when Number = 13 THEN B.RUN_SZ13
            when Number = 14 THEN B.RUN_SZ14
            when Number = 15 THEN B.RUN_SZ15
            when Number = 16 THEN B.RUN_SZ16
            when Number = 17 THEN B.RUN_SZ17
            when Number = 18 THEN B.RUN_SZ18
            when Number = 19 THEN B.RUN_SZ19
            when Number = 20 THEN B.RUN_SZ20
            END as Size_Breakdown,
            case 
            when Number = 1 THEN C.SIZE_RUN1
            when Number = 2 THEN C.SIZE_RUN2
            when Number = 3 THEN C.SIZE_RUN3
            when Number = 4 THEN C.SIZE_RUN4
            when Number = 5 THEN C.SIZE_RUN5
            when Number = 6 THEN C.SIZE_RUN6
            when Number = 7 THEN C.SIZE_RUN7
            when Number = 8 THEN C.SIZE_RUN8
            when Number = 9 THEN C.SIZE_RUN9
            when Number = 10 THEN C.SIZE_RUN10
            when Number = 11 THEN C.SIZE_RUN11
            when Number = 12 THEN C.SIZE_RUN12
            when Number = 13 THEN C.SIZE_RUN13
            when Number = 14 THEN C.SIZE_RUN14
            when Number = 15 THEN C.SIZE_RUN15
            when Number = 16 THEN C.SIZE_RUN16
            when Number = 17 THEN C.SIZE_RUN17
            when Number = 18 THEN C.SIZE_RUN18
            when Number = 19 THEN C.SIZE_RUN19
            when Number = 20 THEN C.SIZE_RUN20
            END as Size_Pack_Qty
            from
            (select a.class_cd, b.Number from
                (select a.class_cd from def_szr a) A
                cross join 
                (select 1 as Number union select 2 union select 3
                union select 4 union select 5 union select 6
                union select 7 union select 8 union select 9
                union select 10 union select 11 union select 12
                union select 13 union select 14 union select 15
                union select 17 union select 18 union select 19
                union select 20) B
                ) A
                left join def_szr b on a.class_cd = b.class_cd
                left join (SELECT * FROM (SELECT RANK() OVER (PARTITION BY CLASS_CD ORDER BY INV_SZ) AS RANKING, * FROM  rsz_file) a WHERE RANKING =1)
				c on a.class_cd = c.class_cd
    '''
    po_by_size_script = f'''
    select 
    PROD_CD,
    PROD_CLR,
    NUMBER,
    SUM(PO_QTY) AS PO_QTY
    from
        (select por.*,
        CASE 
        WHEN por.Number = 1 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl1  - ISNULL(poz1.run_tbl1, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run1
            end
        WHEN por.Number = 2 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl2  - ISNULL(poz1.run_tbl2, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run2
            END 
        WHEN por.Number = 3 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl3  - ISNULL(poz1.run_tbl3, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run3
            END
        WHEN por.Number = 4 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl4  - ISNULL(poz1.run_tbl4, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run4
            END
        WHEN por.Number = 5 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl5  - ISNULL(poz1.run_tbl5, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run5
            END	
        WHEN por.Number = 6 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl6  - ISNULL(poz1.run_tbl6, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run6
            END
        WHEN por.Number = 7 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl7  - ISNULL(poz1.run_tbl7, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run7
            END
        WHEN por.Number = 8 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl8  - ISNULL(poz1.run_tbl8, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run8
            END
        WHEN por.Number = 9 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl9  - ISNULL(poz1.run_tbl9, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run9
            END
        WHEN por.Number = 10 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl10 - ISNULL(poz1.run_tbl10, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run10
            END
        WHEN por.Number = 11 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl11 - ISNULL(poz1.run_tbl11, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run11
            END
        WHEN por.Number = 12 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl12 - ISNULL(poz1.run_tbl12, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run12
            END
        WHEN por.Number = 13 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl13 - ISNULL(poz1.run_tbl13, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run13
            END
        WHEN por.Number = 14 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl14 - ISNULL(poz1.run_tbl14, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run14
            END
        WHEN por.Number = 15 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl15 - ISNULL(poz1.run_tbl15, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run15
            END
        WHEN por.Number = 16 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl16 - ISNULL(poz1.run_tbl16, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run16
            END
        WHEN por.Number = 17 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl17 - ISNULL(poz1.run_tbl17, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run17
            END
        WHEN por.Number = 18 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl18 - ISNULL(poz1.run_tbl18, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run18
            END
        WHEN por.Number = 19 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl19 - ISNULL(poz1.run_tbl19, 0)
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run19
            END
        WHEN por.Number = 20 then
            CASE WHEN por.run_cd IN ('X','Y','Z') THEN
                poz.run_tbl20 - ISNULL(poz1.run_tbl20, 0) 
            ELSE
                (por.log_qty - por.hdl_chg - por.can_qty)/(rsz.size_run1 + rsz.size_run2 + rsz.size_run3 + rsz.size_run4 + rsz.size_run5 + rsz.size_run6 + rsz.size_run7 + rsz.size_run8 + rsz.size_run9 + rsz.size_run10 + rsz.size_run11 + rsz.size_run12 + rsz.size_run13 + rsz.size_run14 + rsz.size_run15 + rsz.size_run16 + rsz.size_run17 + rsz.size_run18 + rsz.size_run19 + rsz.size_run20) * rsz.size_run20
            END
        end as PO_QTY
    
        from
            (select * from 
                (select 
                cast(LOG_DATE - 36163 as datetime) as LOG_DATE,
                cast(EST_DT - 36163 as datetime) as EST_DT,
                BATCH_NUM, 
                NT_NUM,
                pur_num,
                pur_cd,
                run_cd,
                prod_cd,
                prod_clr,
                whs_num,
                pur_lnt,
                comm_ln,
                ven_id,
                log_qty,
                hdl_chg,
                can_qty,
                log_qty - hdl_chg - can_qty as final_po_qty
                FROM plog AS por
                where pur_cd = 1 
                --and prod_cd = 'LA88046' and PROD_CLR = 'MUTL'
                AND log_qty - hdl_chg - can_qty > 0
                AND whs_num <= 'zzzzzz' AND whs_num >= ''
                ) A
            cross join
                (select 1 as Number union select 2 union select 3
                union select 4 union select 5 union select 6
                union select 7 union select 8 union select 9
                union select 10 union select 11 union select 12
                union select 13 union select 14 union select 15
                union select 17 union select 18 union select 19
                union select 20) B) por
        INNER JOIN pur_ord AS pur ON por.pur_num = pur.pur_num
        INNER JOIN inv ON por.prod_cd = inv.prod_cd 
        LEFT JOIN rsz_file AS rsz ON rsz.class_cd = inv.class_cd AND rsz.inv_sz = por.run_cd AND por.run_cd NOT IN ('X','Y','Z') 
        LEFT JOIN poszrun AS poz ON poz.bch_num = 0  AND poz.po_type = 0 AND poz.po_num = por.pur_num AND poz.run_cd = por.nt_num 
        LEFT JOIN poszrun AS poz1 ON poz.bch_num = 0 AND poz1.po_type = 1 AND poz1.po_num = por.pur_num AND poz1.run_cd = por.nt_num
        where pur.type_cd <= 'zzzzzzzz' AND pur.type_cd >= '') A
    where PO_QTY != 0
    GROUP BY PROD_CD,PROD_CLR,NUMBER'''
    # order by PROD_CD,PROD_CLR,NUMBER

    script = f'''
    SELECT *,  AVAILABLE_QTY + SIZE_PO_QTY AS AVAILABLE_TO_SELL_QTY FROM
    (SELECT A.PROD_CD, A.DESCRIP,A.PROD_CLR, A.CLASS_CD, A.WHS_NUM, A.PAIRS, A.SZ_RUN, A.ACTIVE, A.TAXABLE, A.RETAIL_PRS, A.WHOLE_PRS, A.IMAGE, A.NUMBER, 
    B.Size_Breakdown, B.Size_Pack_Qty, 
--     ISNULL(D.UPC_CD, E.UPC_CD) AS UPC_CD,
    ISNULL(D.UPC_CD,'') AS UPC_CD,
    C.LASTRCV_DT, C.LASTRCV_QTY,C.PRICE_BASE, C.FRT_CUS, C.HNDL_FEE, C.PROD_DUTY, C.AVG_COST, C.SALES_COST, C.VENDOR, 
    CASE 
        WHEN A.NUMBER = 1 THEN SZR_QTY1 
        WHEN A.NUMBER = 2 THEN SZR_QTY2 
        WHEN A.NUMBER = 3 THEN SZR_QTY3 
        WHEN A.NUMBER = 4 THEN SZR_QTY4 
        WHEN A.NUMBER = 5 THEN SZR_QTY5 
        WHEN A.NUMBER = 6 THEN SZR_QTY6
        WHEN A.NUMBER = 7 THEN SZR_QTY7
        WHEN A.NUMBER = 8 THEN SZR_QTY8
        WHEN A.NUMBER = 9 THEN SZR_QTY9
        WHEN A.NUMBER = 10 THEN SZR_QTY10 
        WHEN A.NUMBER = 11 THEN SZR_QTY11 
        WHEN A.NUMBER = 12 THEN SZR_QTY12 
        WHEN A.NUMBER = 13 THEN SZR_QTY13 
        WHEN A.NUMBER = 14 THEN SZR_QTY14 
        WHEN A.NUMBER = 15 THEN SZR_QTY15 
        WHEN A.NUMBER = 16 THEN SZR_QTY16 
        WHEN A.NUMBER = 17 THEN SZR_QTY17 
        WHEN A.NUMBER = 18 THEN SZR_QTY18 
        WHEN A.NUMBER = 19 THEN SZR_QTY19 
        WHEN A.NUMBER = 20 THEN SZR_QTY20 
    END AS INVENTORY_QTY,
    CASE 
        WHEN A.NUMBER = 1 THEN SZR_QTY1 - SO_QTY1
        WHEN A.NUMBER = 2 THEN SZR_QTY2 - SO_QTY2
        WHEN A.NUMBER = 3 THEN SZR_QTY3 - SO_QTY3
        WHEN A.NUMBER = 4 THEN SZR_QTY4 - SO_QTY4
        WHEN A.NUMBER = 5 THEN SZR_QTY5 - SO_QTY5
        WHEN A.NUMBER = 6 THEN SZR_QTY6- SO_QTY6
        WHEN A.NUMBER = 7 THEN SZR_QTY7- SO_QTY7
        WHEN A.NUMBER = 8 THEN SZR_QTY8- SO_QTY8
        WHEN A.NUMBER = 9 THEN SZR_QTY9- SO_QTY9
        WHEN A.NUMBER = 10 THEN SZR_QTY10 - SO_QTY10
        WHEN A.NUMBER = 11 THEN SZR_QTY11 - SO_QTY11
        WHEN A.NUMBER = 12 THEN SZR_QTY12 - SO_QTY12
        WHEN A.NUMBER = 13 THEN SZR_QTY13 - SO_QTY13
        WHEN A.NUMBER = 14 THEN SZR_QTY14 - SO_QTY14
        WHEN A.NUMBER = 15 THEN SZR_QTY15 - SO_QTY15
        WHEN A.NUMBER = 16 THEN SZR_QTY16 - SO_QTY16
        WHEN A.NUMBER = 17 THEN SZR_QTY17 - SO_QTY17
        WHEN A.NUMBER = 18 THEN SZR_QTY18 - SO_QTY18
        WHEN A.NUMBER = 19 THEN SZR_QTY19 - SO_QTY19
        WHEN A.NUMBER = 20 THEN SZR_QTY20 - SO_QTY20
    END AS AVAILABLE_QTY,
    CASE 
        WHEN A.NUMBER = 1 THEN ALC_QTY1 
        WHEN A.NUMBER = 2 THEN ALC_QTY2 
        WHEN A.NUMBER = 3 THEN ALC_QTY3 
        WHEN A.NUMBER = 4 THEN ALC_QTY4 
        WHEN A.NUMBER = 5 THEN ALC_QTY5 
        WHEN A.NUMBER = 6 THEN ALC_QTY6
        WHEN A.NUMBER = 7 THEN ALC_QTY7
        WHEN A.NUMBER = 8 THEN ALC_QTY8
        WHEN A.NUMBER = 9 THEN ALC_QTY9
        WHEN A.NUMBER = 10 THEN ALC_QTY10 
        WHEN A.NUMBER = 11 THEN ALC_QTY11 
        WHEN A.NUMBER = 12 THEN ALC_QTY12 
        WHEN A.NUMBER = 13 THEN ALC_QTY13 
        WHEN A.NUMBER = 14 THEN ALC_QTY14 
        WHEN A.NUMBER = 15 THEN ALC_QTY15 
        WHEN A.NUMBER = 16 THEN ALC_QTY16 
        WHEN A.NUMBER = 17 THEN ALC_QTY17 
        WHEN A.NUMBER = 18 THEN ALC_QTY18 
        WHEN A.NUMBER = 19 THEN ALC_QTY19 
        WHEN A.NUMBER = 20 THEN ALC_QTY20 
    END AS ALLOCATED_QTY,
    CASE 
        WHEN A.NUMBER = 1 THEN RMA_QTY1 
        WHEN A.NUMBER = 2 THEN RMA_QTY2 
        WHEN A.NUMBER = 3 THEN RMA_QTY3 
        WHEN A.NUMBER = 4 THEN RMA_QTY4 
        WHEN A.NUMBER = 5 THEN RMA_QTY5 
        WHEN A.NUMBER = 6 THEN RMA_QTY6
        WHEN A.NUMBER = 7 THEN RMA_QTY7
        WHEN A.NUMBER = 8 THEN RMA_QTY8
        WHEN A.NUMBER = 9 THEN RMA_QTY9
        WHEN A.NUMBER = 10 THEN RMA_QTY10 
        WHEN A.NUMBER = 11 THEN RMA_QTY11 
        WHEN A.NUMBER = 12 THEN RMA_QTY12 
        WHEN A.NUMBER = 13 THEN RMA_QTY13 
        WHEN A.NUMBER = 14 THEN RMA_QTY14 
        WHEN A.NUMBER = 15 THEN RMA_QTY15 
        WHEN A.NUMBER = 16 THEN RMA_QTY16 
        WHEN A.NUMBER = 17 THEN RMA_QTY17 
        WHEN A.NUMBER = 18 THEN RMA_QTY18 
        WHEN A.NUMBER = 19 THEN RMA_QTY19 
        WHEN A.NUMBER = 20 THEN RMA_QTY20 
    END AS REAL_ALLOCATED_QTY,
    CASE 
        WHEN A.NUMBER = 1 THEN SO_QTY1 
        WHEN A.NUMBER = 2 THEN SO_QTY2 
        WHEN A.NUMBER = 3 THEN SO_QTY3 
        WHEN A.NUMBER = 4 THEN SO_QTY4 
        WHEN A.NUMBER = 5 THEN SO_QTY5 
        WHEN A.NUMBER = 6 THEN SO_QTY6
        WHEN A.NUMBER = 7 THEN SO_QTY7
        WHEN A.NUMBER = 8 THEN SO_QTY8
        WHEN A.NUMBER = 9 THEN SO_QTY9
        WHEN A.NUMBER = 10 THEN SO_QTY10 
        WHEN A.NUMBER = 11 THEN SO_QTY11 
        WHEN A.NUMBER = 12 THEN SO_QTY12 
        WHEN A.NUMBER = 13 THEN SO_QTY13 
        WHEN A.NUMBER = 14 THEN SO_QTY14 
        WHEN A.NUMBER = 15 THEN SO_QTY15 
        WHEN A.NUMBER = 16 THEN SO_QTY16 
        WHEN A.NUMBER = 17 THEN SO_QTY17 
        WHEN A.NUMBER = 18 THEN SO_QTY18 
        WHEN A.NUMBER = 19 THEN SO_QTY19 
        WHEN A.NUMBER = 20 THEN SO_QTY20 
    END AS SALES_ORDER_QTY,
    CASE 
        WHEN A.NUMBER = 1 THEN PO_QTY1 
        WHEN A.NUMBER = 2 THEN PO_QTY2 
        WHEN A.NUMBER = 3 THEN PO_QTY3 
        WHEN A.NUMBER = 4 THEN PO_QTY4 
        WHEN A.NUMBER = 5 THEN PO_QTY5 
        WHEN A.NUMBER = 6 THEN PO_QTY6
        WHEN A.NUMBER = 7 THEN PO_QTY7
        WHEN A.NUMBER = 8 THEN PO_QTY8
        WHEN A.NUMBER = 9 THEN PO_QTY9
        WHEN A.NUMBER = 10 THEN PO_QTY10 
        WHEN A.NUMBER = 11 THEN PO_QTY11 
        WHEN A.NUMBER = 12 THEN PO_QTY12 
        WHEN A.NUMBER = 13 THEN PO_QTY13 
        WHEN A.NUMBER = 14 THEN PO_QTY14 
        WHEN A.NUMBER = 15 THEN PO_QTY15 
        WHEN A.NUMBER = 16 THEN PO_QTY16 
        WHEN A.NUMBER = 17 THEN PO_QTY17 
        WHEN A.NUMBER = 18 THEN PO_QTY18 
        WHEN A.NUMBER = 19 THEN PO_QTY19 
        WHEN A.NUMBER = 20 THEN PO_QTY20 
    END AS PO_QTY,
    ISNULL(F.PO_QTY,0) AS SIZE_PO_QTY
    FROM
       {inventory_setup_script}
       INNER JOIN       
        (SELECT * FROM
            ({size_run_breakdown_script}) A
        WHERE NOT (Size_Breakdown= '' AND Size_Pack_Qty = 0)
        ) B ON A.class_cd = B.class_cd AND A.NUMBER = B.NUMBER
        LEFT JOIN (SELECT * FROM inv_data WHERE WHS_NUM = '01') C ON A.PROD_CD = C.PROD_CD AND A.PROD_CLR = C.PROD_CLR
        LEFT JOIN prod_upc D ON A.PROD_CD = D.PROD_CD AND A.PROD_CLR = D.PROD_CLR AND B.Size_Breakdown = D.SIZE_NUM
--         LEFT JOIN prod_upc E ON A.PROD_CD = LEFT(E.PROD_CD,LEN(E.PROD_CD)-1) AND A.PROD_CLR = E.PROD_CLR AND B.Size_Breakdown = E.SIZE_NUM
        LEFT JOIN ({po_by_size_script}) F ON A.PROD_CD = F.PROD_CD AND A.PROD_CLR = F.PROD_CLR AND A.NUMBER = F.NUMBER
        ) A
--         WHERE NOT (INVENTORY_QTY = 0 AND AVAILABLE_QTY = 0 AND ALLOCATED_QTY=0 AND REAL_ALLOCATED_QTY=0 AND SALES_ORDER_QTY=0 AND PO_QTY = 0 AND SIZE_PO_QTY=0)
--         order by A.PROD_CD, A.PROD_CLR, A.class_cd, A.Number asc;     
        '''

    script1 = f'''select * from ({script}) A inner join
        (SELECT * FROM (Select PROD_CD, PROD_CLR, 
        SUM(INVENTORY_QTY) as INVENTORY_QTY,
        SUM(AVAILABLE_QTY) as AVAILABLE_QTY,
        SUM(ALLOCATED_QTY) as ALLOCATED_QTY,
        SUM(REAL_ALLOCATED_QTY) as REAL_ALLOCATED_QTY,
        SUM(SALES_ORDER_QTY) as SALES_ORDER_QTY,        
        SUM(PO_QTY) as PO_QTY,
        SUM(SIZE_PO_QTY) as SIZE_PO_QTY        
        from ({script}) A GROUP BY PROD_CD, PROD_CLR) Q  
        WHERE NOT (INVENTORY_QTY = 0 AND AVAILABLE_QTY = 0 AND ALLOCATED_QTY=0 
        AND REAL_ALLOCATED_QTY=0 AND SALES_ORDER_QTY=0 AND PO_QTY = 0 AND SIZE_PO_QTY=0)) B 
        on A.PROD_CD = B.PROD_CD and A.PROD_CLR = B.PROD_CLR'''
    start_time = time.time()
    print_color(f'Attempting to Import Inventory  Data', color='y')
    df = pd.read_sql(script1, con=conn)
    # print_color(script1, color='y')

    # df1 =  pd.read_sql(script1, con=conn)

    # print(df1)
    #
    df.to_csv(f'{data_directory}\\inventory_data.csv', index=False)
    df.to_csv(f'{second_data_directory}\\inventory_data.csv', index=False)
    end_time = time.time()
    print_color(f'Inventory Data Exported: Took {end_time - start_time} Seconds To Complete', color='g')

    map_module_setting(engine=engine, category='recruit files', module='recruit_inventory_data', sub_module='',
                       data_type='inventory data')


@error_handler
def get_data_from_sheet(SAMPLE_RANGE_NAME, SAMPLE_SPREADSHEET_ID):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    computer = getpass.getuser()
    computer_dict = computer_dict_method()
    client_secret_file = computer_dict.get(computer).get('client_secret_file')
    token_file = computer_dict.get(computer).get('token_file')
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    token_file_works = False
    # while token_file_works is False:
    if os.path.exists(token_file):
        print_color(f'Credentials Already Exists', color='g')
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            token_file_works = True
            print_color(creds.valid, color='y')
        except:
            creds =None
            os.remove(token_file)

        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    df = pd.DataFrame(values)
    new_header = df.iloc[0]
    df.columns = new_header
    df = df[1:]

    return df


@error_handler
def import_google_sheet_data(project_name=None, engine=None, table_name=None, range=None):
    SAMPLE_SPREADSHEET_ID = '1yON-8mYKkQ5Fcy1mqJKn6Rk_Vx7KQfv9EdxLb1fZOGI'
    SAMPLE_RANGE_NAME = f'{table_name}!{range}'
    print_color(f'https://docs.google.com/spreadsheets/d/{SAMPLE_SPREADSHEET_ID}/edit#gid=0')

    df = get_data_from_sheet(SAMPLE_RANGE_NAME, SAMPLE_SPREADSHEET_ID)
    df.columns = [x.replace(" ", "_").lower() for x in df.columns]
    print(df)

    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col])


    table_name = 'containers'

    # if inspect(engine).has_table(table_name):
    engine.connect().execute(f'drop table if exists {table_name}')

    sql_types = Database_Modules.Get_SQL_Types(df).data_types
    Database_Modules.Change_Sql_Column_Types(engine=engine, Project_name=project_name, Table_Name=table_name, DataTypes=sql_types, DataFrame=df)
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False, schema=project_name, chunksize=1000, dtype=sql_types)

    engine.connect().execute(f'Create index container on containers(`container_number`)')
    print_color(f'Data For {table_name} Has Been Imported', color='b')


@error_handler
def export_data_sets(engine, export_folder, second_data_directory):
    # # NO SIZE RUN BY STYLE COLOR
    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='no_size_run_data_setup', table= 'no_size_run_data_setup',
                query=f'Select * from no_size_run_data_setup',
                extract_type='proposal_data_files')

    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='no_size_run_data_setup_all', table='no_size_run_data_setup_all',
                query=f'Select * from no_size_run_data_setup_all',
                extract_type='proposal_data_files')

    # NO SIZE RUN BY STYLE COLOR SIZE
    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='no_size_run_data_by_size_setup', table='no_size_run_data_setup_by_size where quantity >0',
                query=f'Select * from no_size_run_data_setup_by_size where quantity >0',
                extract_type='proposal_data_files')

    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='no_size_run_data_by_size_setup_all', table='no_size_run_data_setup_by_size',
                query=f'Select * from no_size_run_data_setup_by_size',
                extract_type='proposal_data_files')

    # SIZE RUN BY STYLE COLOR
    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='size_run_data_setup',
                table='size_run_data_setup',
                query=f'Select * from size_run_data_setup order by Core_Style, core_color, id',
                extract_type='proposal_data_files')

    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='size_run_data_setup_all',
                table='size_run_data_setup_all',
                query=f'Select * from size_run_data_setup_all order by Core_Style, core_color, id',
                extract_type='proposal_data_files')

    # # ALL UPC DATA
    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='upc_data',
                table='upc_data',
                query=f'Select * from upc_data',
                extract_type='proposal_data_files')

    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='upc_data_active',
                table='upc_data where status = "Y"',
                query=f'Select * from upc_data where status = "Y"',
                extract_type='proposal_data_files')

    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='upc_data_ats',
                table='upc_data where   ATS >0',
                query=f'Select * from upc_data where ATS >0',
                extract_type='proposal_data_files')

    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='upc_data_active_ats',
                table='upc_data where status = "Y" AND  ATS >0;',
                query=f'Select * from upc_data where status = "Y" AND  ATS >0',
                extract_type='proposal_data_files')

    # SIZE RUN BY STYLE COLOR SIZE
    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='size_run_by_size_data_setup',
                table='size_run_data_setup_by_size WHERE Lookup_Quantity >0',
                query=f'Select * from size_run_data_setup_by_size WHERE Lookup_Quantity >0 order by Core_Style, core_color, id',
                extract_type='proposal_data_files')

    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='size_run_by_size_data_setup_all',
                table='size_run_data_setup_by_size',
                query=f'Select * from size_run_data_setup_by_size order by Core_Style, core_color, id',
                extract_type='proposal_data_files')

    # COMPARATIVE STYLE REPORT BY STYLE - COLOR
    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='comparative_style_report',
                table='COMPARATIVE_STYLE_REPORT',
                query=f'Select * from COMPARATIVE_STYLE_REPORT',
                extract_type='comparative_styles_files')

    query_setup(engine=engine, export_folder=export_folder, second_data_directory=second_data_directory,
                export_name='comparative_style_report_by_size',
                table='COMPARATIVE_STYLE_REPORT_BY_SIZE',
                query=f'Select * from COMPARATIVE_STYLE_REPORT_BY_SIZE',
                extract_type='comparative_styles_files')


@error_handler
def query_setup(engine, export_folder, second_data_directory, export_name, table, query, extract_type):
    # SIZE RUN BY STYLE COLOR

    file_path_1 = f'{export_folder}\\{extract_type}\\{export_name}.csv'
    file_path_2 = f'{second_data_directory}\\{extract_type}\\{export_name}.csv'
    count_of_rows = int(
        pd.read_sql(f'''SELECT count(*) as count_rows from {table};''', con=engine)['count_rows'].iloc[0])

    for i in range(0, count_of_rows, 5000):
        print(i, i + 4999)
        df = pd.read_sql(f'{query} limit {i}, {5000}',
                         con=engine)
        if i == 0:
            df.to_csv(file_path_1, index=False)
            df.to_csv(file_path_2, index=False)
        else:
            df.to_csv(file_path_1, mode='a', header=False, index=False)
            df.to_csv(file_path_2, index=False)

    print_color(f'{export_name} In Stock Exported', color='p')


@error_handler
def set_primary_keys(engine):
    primary_key_dict = {
        'inventory_data': {'table_name': 'inventory_data', 'primary_key': 'prod_cd, prod_clr, Size_Breakdown'},
        'color_codes': {'table_name': 'color_codes', 'primary_key': 'prod_clr'}
        # 'amazon_data': {'table_name': 'amazondata_edi', 'primary_key': 'id'},amazon_direct_exclusions
        # 'returns': {'table_name': 'returns', 'primary_key': 'id'},
        # 'purchase_orders': {'table_name': 'purchase_orders', 'primary_key': 'id'},
        # 'production_wip': {'table_name': 'production_wip', 'primary_key': 'id'},
        # 'inventory_transfers': {'table_name': 'inventory_transfers', 'primary_key': 'id'},
        # 'inventory_transactions': {'table_name': 'invtransactions', 'primary_key': 'id'},
        # 'past_18_week': {'table_name': 'week18_date', 'primary_key': 'id'},
    }

    scripts = []
    for each_key in primary_key_dict.keys():
        table_name = primary_key_dict.get(each_key).get('table_name')
        primary_key_fields = primary_key_dict.get(each_key).get('primary_key')

        df = pd.read_sql(f'''SELECT *
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE table_schema = schema()
            AND   table_name   = '{table_name}'
            AND   INDEX_NAME   = 'PRIMARY';''', con=engine)

        if df.shape[0]==0:
            scripts.append(f'Alter Table {table_name} add Primary key({primary_key_fields});')

    run_sql_scripts(engine=engine, scripts=scripts)

    map_module_setting(engine=engine, category='sql setup', module='set_primary_keys', sub_module='',
                       data_type='set primary keys')


def set_indexes(engine):
    index_dict = {
        'style_master':[{'table_name':'style_master','index_name':'style_color_size', 'field_name': ['style','color_code', 'size']},
                        {'table_name':'style_master','index_name':'class_size', 'field_name': ['CLASS','INVENTORY_SIZE']}],
        'po_data_by_size': [{'table_name': 'po_data_by_size', 'index_name': 'style_color', 'field_name': ['prod_cd', 'prod_clr']}],
        'customers': [
            {'table_name': 'customers', 'index_name': 'customer_id', 'field_name': ['customer_id']}],


                  }
    scripts = []
    for each_key in index_dict.keys():
        index_list = index_dict.get(each_key)
        for each_item in index_list:
            table_name = each_item.get('table_name')
            index_name = each_item.get('index_name')
            index_fields = each_item.get('field_name')


            df = pd.read_sql(f'''SELECT * FROM information_schema.statistics 
                  WHERE table_schema = schema()
                    AND table_name = "{table_name}"
                    and INDEX_NAME = "{index_name}"
                    ''', con=engine)
            print(table_name, index_name, df.shape[0])

            if df.shape[0] == 0:
                if type(index_fields) is list:
                    new_index_fields = str(index_fields).replace("[","").replace("]","").replace("'","`")
                    scripts.append(f'Create Index {index_name} on {table_name}({new_index_fields})')
                else:
                    scripts.append(f'Create Index {index_name} on {table_name}({index_fields})')

    print(scripts)
    run_sql_scripts(engine=engine, scripts=scripts)

    map_module_setting(engine=engine, category='sql setup', module='set_indexes', sub_module='',
                       data_type='set indexes')
