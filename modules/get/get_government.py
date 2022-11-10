import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas as pd
import json
import configparser


DB_SQLITE = './db/db_collect.db'
GOVERNMENT_TABLE = 'GOVERNMENT'
CONFIG_FILE = './datatype.properties'


# connect DB
def connect_DB():
    # DB sqlite
    connectionDB = f'sqlite:///{DB_SQLITE}'
    engineDB = create_engine(connectionDB)
    return engineDB

# get data DB
def get_data_year(engineDB):
    dict_data = [{'Year': 2016},
                 {'Year': 2017},
                 {'Year': 2018},
                 {'Year': 2019},
                 {'Year': 2020},
                 {'Year': 2021}]
    
    return dict_data

# get years for governments
def get_years():
    # connect
    engineDB = connect_DB()
    
    # select data
    result_data = get_data_year(engineDB)
    # build metadata
    result_metadata = get_government_metadata(result_data, 'YEAR')
    
    # set final result
    result = {}
    result['data'] = result_data
    result['metadata'] = result_metadata

    return result

# get type and description of columns
def get_government_metadata(data, name):
    # def type info
    info = name
    # get properties file
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    # convert to df
    df = pd.DataFrame(data)
    # get cols of df
    cols = df.columns
    list_datatype = []
    # every col
    for c in cols:
        dict_datatype = {}
        # id
        dict_datatype['id'] = c
        if config.has_option(info, c):
            # get type
            dict_datatype['type'] = json.loads(config.get(info, c))['type']
            # get text
            dict_datatype['description'] = json.loads(config.get(info, c))['text']
            list_datatype.append(dict_datatype)
    
    dict_datatype = pd.DataFrame(list_datatype).to_dict(orient='records')
    
    return dict_datatype

# get data DB
def get_government_region_data(engineDB, year=None, id_region=None, normalized='no'):
    # query 
    if year != None:
        query = f'''
        WITH max_date AS 
        (
        SELECT g.Id_region , MAX(g.Ini_date) Ini_date, MAX(IFNULL(g.End_date, DATE('9999-12-31'))) End_date
        FROM {GOVERNMENT_TABLE} g 
        WHERE g.Id_region IS NOT NULL
            AND g.Ini_date <= DATE('{year}-12-31')
        GROUP BY g.Id_region
        )
        '''
    else:
        query = f'''
        '''

    if normalized == 'no':
        query = query + f'''
        SELECT g.Id_region , r.Region , 
            g.Ini_date,
            g.End_date,
            g.Government,
            g.Name_president
        '''
    else:
        query = query + f'''
        SELECT g.Id_region ,
            g.Ini_date,
            g.End_date,
            g.Government,
            g.Name_president
        '''
        
    # from
    
    # specific year
    if year != None:
        query = query + f'''
        FROM "{GOVERNMENT_TABLE}" g
            INNER JOIN max_date m ON g.Id_region = m.Id_region 
            INNER JOIN REGION r ON r.Id_region = g.Id_region
        WHERE g.Id_region IS NOT NULL
            AND g.Ini_date <= DATE('{year}-12-31')
            AND g.Ini_date = m.Ini_date
            AND IFNULL(g.End_date, DATE('9999-12-31')) = m.End_date
        '''
    else:
        query = query + f'''
        FROM "{GOVERNMENT_TABLE}" g
            INNER JOIN REGION r ON r.Id_region = g.Id_region
        WHERE g.Id_region IS NOT NULL
        '''        

    # specific region
    if id_region != None:
        query = query + f'''
         AND r.Id_region = '{id_region}'
        '''

    query = query + f'''
    ORDER BY g.Id_region , g.Ini_date 
    '''

    #print(query)

    try:
        dict_data = pd.read_sql_query(query, engineDB).to_dict(orient='records')
    except:
        dict_data = {}
    
    return dict_data

# get governments by region
def get_government_region(year=None, id_region=None, normalized='no'):
    # connect
    engineDB = connect_DB()
    
    # select data
    result_data = get_government_region_data(engineDB, year, id_region, normalized)
    # build metadata
    result_metadata = get_government_metadata(result_data, 'government_region')
    
    # set final result
    result = {}
    result['data'] = result_data
    result['metadata'] = result_metadata

    return result

# get data DB
def get_government_city_data(engineDB, year=None, id_city=None, id_province=None, id_region=None, normalized='no'):
    # query 
    if year != None:
        query = f'''
        WITH max_date AS 
        (
        SELECT g.Id_city , MAX(g.Ini_date) Ini_date, MAX(IFNULL(g.End_date, DATE('9999-12-31'))) End_date
        FROM {GOVERNMENT_TABLE} g 
        WHERE g.Id_city IS NOT NULL
            AND g.Ini_date <= DATE('{year}-12-31')
        GROUP BY g.Id_city
        )
        '''
    else:
        query = f'''
        '''

    if normalized == 'no':
        query = query + f'''
        SELECT g.Id_city , c.City ,
            c.Id_province , p.Province ,
            p.Id_region , r.Region , 
            g.Ini_date,
            g.End_date,
            g.Government,
            g.Name_president
        '''
    else:
        query = query + f'''
        SELECT g.Id_city ,
            c.Id_province , 
            p.Id_region , 
            g.Ini_date,
            g.End_date,
            g.Government,
            g.Name_president
        '''
        
    # from
    
    # specific year
    if year != None:
        query = query + f'''
        FROM "{GOVERNMENT_TABLE}" g
            INNER JOIN max_date m ON g.Id_city = m.Id_city 
            INNER JOIN CITY c ON c.Id_city = g.Id_city  
            INNER JOIN PROVINCE p ON p.Id_province = c.Id_province 
            INNER JOIN REGION r ON r.Id_region = p.Id_region
        WHERE g.Id_city IS NOT NULL
            AND g.Ini_date <= DATE('{year}-12-31')
            AND g.Ini_date = m.Ini_date
            AND IFNULL(g.End_date, DATE('9999-12-31')) = m.End_date
        '''
    else:
        query = query + f'''
        FROM "{GOVERNMENT_TABLE}" g
            INNER JOIN CITY c ON c.Id_city = g.Id_city  
            INNER JOIN PROVINCE p ON p.Id_province = c.Id_province 
            INNER JOIN REGION r ON r.Id_region = p.Id_region
        WHERE g.Id_city IS NOT NULL
        '''        

    # specific city
    if id_city != None:
        query = query + f'''
         AND c.Id_city = '{id_city}'
        '''
    
    # specific province
    if id_province != None:
        query = query + f'''
         AND p.Id_province = '{id_province}'
        '''
    
    # specific region
    if id_region != None:
        query = query + f'''
         AND r.Id_region = '{id_region}'
        '''

    query = query + f'''
    ORDER BY g.Id_region , g.Ini_date 
    '''

    #print(query)

    try:
        dict_data = pd.read_sql_query(query, engineDB).to_dict(orient='records')
    except:
        dict_data = {}
    
    return dict_data

# get governments by region
def get_government_city(year=None, id_city=None, id_province=None, id_region=None, normalized='no'):
    # connect
    engineDB = connect_DB()
    
    # select data
    result_data = get_government_city_data(engineDB, year, id_city, id_province, id_region, normalized)
    # build metadata
    result_metadata = get_government_metadata(result_data, 'government_city')
    
    # set final result
    result = {}
    result['data'] = result_data
    result['metadata'] = result_metadata

    return result
