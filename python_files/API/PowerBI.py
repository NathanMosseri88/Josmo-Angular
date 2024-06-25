import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import adal
import requests
import json
import pandas
from Database_Modules import print_color, map_module_setting, run_sql_scripts
import time

application_id = '2c3240f2-671e-4163-8506-d65e315405a7'
application_secret = 'RAPmVDbkqvT5eUuwB+ZSbtwgvV/EVr8ShoJVUJsAl5g='


def power_bi_get_header(header_type=None):
    authority_url = 'https://login.windows.net/common'
    # authority_url = 'https://login.microsoftonline.com/'
    resource_url = 'https://analysis.windows.net/powerbi/api'
    client_id = '2c3240f2-671e-4163-8506-d65e315405a7'
    username = 'Rschweky@Josmo.com'
    password = 'Sammyapbi1234#'
    context = adal.AuthenticationContext(authority=authority_url,
                                         validate_authority=True,
                                         api_version=None)

    token = context.acquire_token_with_username_password(resource=resource_url,
                                                         client_id=client_id,
                                                         username=username,
                                                         password=password)

    # token = context.acquire_token_with_client_credentials(resource=resource_url,
    #                                                       client_id=client_id,
    #                                                         client_secret=client_secret)

    access_token = token.get('accessToken')
    if header_type == 'mutlipart-form':
        header = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'multipart/form-data'}
    else:
        header = {'Authorization': f'Bearer {access_token}'}

    return header


def powerbi_get_group_id():
    # authority_url = 'https://login.windows.net/common'
    # resource_url = 'https://analysis.windows.net/powerbi/api'
    # client_id = 'b40519f2-64b6-48ae-ab90-655232eb2da5'
    # username = 'joeh@q4designs.com'
    # password = 'Simple123'
    # context = adal.AuthenticationContext(authority=authority_url,
    #                                      validate_authority=True,
    #                                      api_version=None)
    # token = context.acquire_token_with_username_password(resource=resource_url,
    #                                                      client_id=client_id,
    #                                                      username=username,
    #                                                      password=password)
    # access_token = token.get('accessToken')
    # print(access_token)
    #
    # header = {'Authorization': f'Bearer {access_token}'}

    header = power_bi_get_header()
    groups_request_url = 'https://api.powerbi.com/v1.0/myorg/groups'

    print(requests.get(url=groups_request_url, headers=header))
    groups_request = json.loads(requests.get(url=groups_request_url, headers=header).content)

    groups = groups_request.get('value')
    for group in groups:
        print(group.get("name"), group.get('id'))


def power_bi_get_gateways():
    header = power_bi_get_header()
    request_url = f'https://api.powerbi.com/v1.0/myorg/gateways'
    r = json.loads(requests.get(url=request_url, headers=header).content)
    print_color(r)
    gateways = r.get('value')

    gateway_dict = {}
    for each_gateway in gateways:
        print(each_gateway.get('name'))
        print_color(each_gateway, color='y')
        print_color(each_gateway.get("publicKey"), color='b')
        print_color(each_gateway.get("gatewayStatus"), color='b')

        gateway_dict.update({each_gateway.get('name'):each_gateway.get('id')})

    # print(gateway_dict)
    return gateway_dict


def power_bi_get_data_sources(gatewayId):
    header = power_bi_get_header()
    request_url = f'https://api.powerbi.com/v1.0/myorg/gateways/{gatewayId}/datasources'
    r = json.loads(requests.get(url=request_url, headers=header).content)
    datsources = r.get('value')


    datsources_dict = {}
    for each_datasource in datsources:
        print_color(each_datasource, color='y')
        datsources_dict.update({each_datasource.get('datasourceName'): each_datasource.get('id')})

    print_color(datsources_dict, color='r')
    return datsources_dict

def power_bi_get_dataset(groupId):
    header = power_bi_get_header()
    # params = {'groupId':groupId}
    request_url = f'https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets'

    groups_request = json.loads(requests.get(url=request_url, headers=header).content)
    dataset_dict = {}
    for each_dataset in groups_request.get('value'):
        dataset_dict.update({each_dataset.get('name'):each_dataset.get('id')})
        # datasets.append(dataset_dict)
        # print(each_dataset.get('name'))
    # pprint(groups_request)

    # print(datasets)
    return dataset_dict




def power_bi_refresh_datasets(engine, groupId, datasetId, group):
    scripts = []
    scripts.append(f'''Create table if not exists powerbi_refresh_status(
          id int auto_increment primary key,
          date datetime,
          `group` varchar(65),
          status varchar(65),
          details text    
      )''')
    run_sql_scripts(engine=engine, scripts=scripts)


    header = power_bi_get_header()
    requst_url = f'https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes'

    body = {}

    r = requests.post(url=requst_url, json=body, headers=header)
    print(r.status_code, r.reason, r.text, r.content)

    last_refresh = None
    details = r.text
    if details is not None:
        details = str(details).replace('"', "'")



    if r.status_code == 429:
        scripts.append(
            f'Insert into powerbi_refresh_status values (null, current_timestamp(), "{group}", "{last_refresh}", "{details}")')
    run_sql_scripts(engine=engine, scripts=scripts)

    map_module_setting(engine=engine, category='powerbi', module='run_pbi_integration', sub_module='power_bi_refresh_datasets',
                       data_type=f'{group} powerbi refresh triggered')

    return r.status_code
# header = power_bi_get_gateways()

def power_bi_get_refresh_history(engine, groupId, datasetId, group):
    header = power_bi_get_header()
    # groups_request_url = 'https://api.powerbi.com/v1.0/myorg/groups'

    scripts = []
    request_url = f'https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes?$top={1}'
    r = json.loads(requests.get(url=request_url, headers=header).content)

    refreshes = r.get('value')
    print_color( refreshes[0], color='b')
    last_refresh = refreshes[0].get('status')
    details = ''
    while last_refresh == 'Unknown':

        print_color(f'Refresh Still Processing Waiting 60 seconds and will check again', color='r')
        for i in range(0, 5):
            print_color(f'Waiting {60 - i*10} Seconds to check again', color='y')
            time.sleep(10)

        r = json.loads(requests.get(url=request_url, headers=header).content)

        refreshes = r.get('value')
        print_color(refreshes[0], color='b')
        last_refresh = refreshes[0].get('status')

        details = str(refreshes[0].get('serviceExceptionJson'))
        if details is not None:
            details= details.replace('"', "'")


    if last_refresh == 'Completed':
        map_module_setting(engine=engine, category='powerbi', module='run_pbi_integration', sub_module='power_bi_get_refresh_history',
                           data_type=f'{group} powerbi refresh complete')

    scripts.append( f'Insert into powerbi_refresh_status values (null, current_timestamp(),"{group}", "{last_refresh}", "{details}")')
    run_sql_scripts(engine=engine, scripts=scripts)
    # else:
    #     map_module_setting(engine=engine, category='powerbi', module='run_pbi_integration',
    #                        sub_module='power_bi_refresh_datasets',
    #                        data_type='powerbi refresh triggered')

    # datsources_dict = {}
    # # print_color(client_name, color='b')
    # for each_refresh in refreshes:
    #
    #     print_color(each_refresh, color='y')
        #     datsources_dict.update({each_datasource.get('datasourceName'): each_datasource.get('id')})
        #
        # print_color(datsources_dict, color='r')
        # return datsources_dict

        # break



def run_pbi_integration(engine):
    '''
    Step 1: connect to gateway
    Step 2: connect to datasource
    step 3: connect to group
    step 4: connect to dataset
    step 5: refresh dataset
    step 6: get status of refresh
    :return:
    '''

    '''app consent'''


    'https://login.microsoftonline.com/62398a19-bc38-4724-8ef8-0e8c5e236e1a/adminconsent?client_id=2c3240f2-671e-4163-8506-d65e315405a7'

    group_id = '2c69af14-2e63-453b-9478-f68c3ebbb8dc'

    gateway_dict = power_bi_get_gateways()
    gateway_name = list(gateway_dict.keys())
    gatewayId = gateway_dict.get(gateway_name[0])
    datsources_dict = power_bi_get_data_sources(gatewayId)
    dataset_dict = power_bi_get_dataset(group_id)
    print(dataset_dict)
    dataset_id = dataset_dict.get('JosmoShoes PBI New')
    status_code = power_bi_refresh_datasets(engine, group_id, dataset_id, 'Main')
    if status_code == 202:
        time.sleep(15)
        power_bi_get_refresh_history(engine, group_id, dataset_id, 'Main')

    dataset_id = dataset_dict.get('JosmoShoes Inventory PBI')
    status_code = power_bi_refresh_datasets(engine, group_id, dataset_id, 'Inventory')
    if status_code == 202:
        time.sleep(15)
        power_bi_get_refresh_history(engine, group_id, dataset_id, 'Inventory')

    # print_color(gateway_dict, color='g')
    # print_color(datsources_dict, color='g')
    # print_color(dataset_dict, color='g')
    #

#
# run_pbi_integration()


# powerbi_get_group_id()

# print(header)
# authenticate()
