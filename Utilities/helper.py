import pandas as pd
import teradata
import pathlib
import win32com.client as win32
import os
import pyodbc
import pyautogui

# Version Control
__version__ = '0.0.9'

# definition to check for NaN and return columns containing them
def check_nan(df_sub):
    nan_values = df_sub.isna()
    nan_columns = nan_values.any()
    columns_with_nan = df_sub.columns[nan_columns].tolist()
    return print(columns_with_nan)

# definition to create a store key column from dataframe
def store_key(df_sub):
    df_sub['STORE_KEY'] = df_sub['ENTERPRISE_CD'] + df_sub['STORE_CD'].astype('string')

# defintion to create new calculation column    
def calc_margin(df_sub):
    df_sub['MARGIN'] = df_sub['SUM_TX_TOT_AMT'] - df_sub['PRC_ACQ_COST_AMT']

# definition to pull data from teradata based on sql script provided
def teradata_data_pull(input_script, output_file, variable_file):
    # looking for credentials
    with open(variable_file, 'r') as f:
        username = f.readline().rstrip('\n')
        my_password = f.readline().rstrip('\n')
        host = f.readline().rstrip('\n')

    # assigning sql code to a variable
    sql_script1 = input_script
    sql_script_read1 = pathlib.Path(sql_script1).read_text()

    # make a connection
    udaExec = teradata.UdaExec (appName='test', version='1.0', logConsole = False)

    with udaExec.connect(method='odbc', system=host, username=username,
                        password=my_password, driver='Teradata Database ODBC Driver 17.10',
                        authentication='LDAP') as session:

        # reading sql script, creating a session, saving table output from teradata to dataframe
        df1 = pd.read_sql(sql_script_read1, session)
        # saving dataframe to .csv file
        df1.to_csv(output_file, index = False)
        
def excel_refresh(excel_doc):
    
    excelFile = excel_doc

    # assigning excel application to variable, setting alerts and app to background
    excel = win32.DispatchEx('Excel.Application')
    excel.DisplayAlerts = True
    excel.Visible = False
    book = excel.Workbooks.Open(excelFile)

    # Refresh all sheets in workbook
    book.RefreshAll()
    excel.CalculateUntilAsyncQueriesDone() # this will actually wait for the excel workbook to finish updating
    book.Save()
    book.Close()
    excel.Quit()
    del book  # deleting object book for memory purposes
    del excel # deleting object excel for memory purposes
    
def kcdr_data_pull(input_script, output_file, variables_file):
    # opening file to access parameters
    with open(variables_file, 'r') as f:
        username = f.readline().rstrip('\n')
        password = f.readline().rstrip('\n')
        server = f.readline().rstrip('\n')
        database = f.readline().rstrip('\n')
    
    # creating a session
    session = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    # assigning sql code to a variable
    sql_script1 = input_script
    sql_script_read1 = pathlib.Path(sql_script1).read_text()

    # using pandas to read sql code and output to a csv file
    df1 = pd.read_sql(sql_script_read1, session)
    df1.to_csv(output_file, index = False)
    

def teradata_ddl_pull (input_script, output_file, variable_file):
    # creating an empty list to hold SQL code split by delimiter
    sql_chunks = []

    # creating a connection 
    udaExec = teradata.UdaExec (appName = 'test', version = '1.0', logConsole = False)

    # opening the SQL script
    # using a for loop to split the script wherever semicolons are present until end of script
    with open (input_script) as sq:
        sql_script = sq.read()
        for i in sql_script.split(';'):
            sql_chunks.append(i)

    # using a for loop through the length of the list to add the semi colon's back to the chunks of SQL code
    for i in range(len(sql_chunks)):
        sql_chunks[i]=sql_chunks[i] + ";"

    # deleting empty element in the last slot of the list
    print(sql_chunks[-1])    
    del sql_chunks[-1]

    # looking for variables
    with open (variable_file, 'r') as f:
        username = f.readline().rstrip('\n')
        my_password = f.readline().rstrip('\n')
        host = f.readline().rstrip('\n')

    with udaExec.connect(method='odbc', system=host, username=username,
                        password=my_password, driver='Teradata Database ODBC Driver 17.10',
                        authentication = 'LDAP') as session:


        for i in range(len(sql_chunks)):
            if sql_chunks[i] != sql_chunks[-1]:
                session.execute(sql_chunks[i])
                print ('executed ' + str(i+1) + ' times')
            else:
                print(sql_chunks[i])
                df1 = pd.read_sql(sql_chunks[i], session)
                df1.to_csv(output_file, index = False)

def auto_connect():
    pyautogui.FAILSAFE = True
    x = 1572
    y = 1060

    pyautogui.doubleClick(x, y)

def auto_disconnect():
    pyautogui.FAILSAFE = True
    x = 1572
    y = 1060
    x3 = 1638
    y3 = 933
    x4 = 964
    y4 = 542

    pyautogui.rightclick(x, y)
    pyautogui.click(x3, y3)
    pyautogui.click(x4, y4)