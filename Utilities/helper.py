import pandas as pd
import teradata
import pathlib
import win32com.client as win32
import os

# Version Control
__version__ = '0.0.1'

# definition to check for NaN and return columns containing them
def check_nan(df_sub):
    nan_values = df_sub.isna()
    nan_columns = nan_values.any()
    columns_with_nan = df_sub.columns[nan_columns].tolist()
    return print(columns_with_nan)

# definition to create a store key column from dataframe
def store_key(df_sub):
    df_sub['STORE_KEY'] = df_sub['ENTERPRISE_CD'] + df_sub['STORE_CD'].astype('string')

# definition to pull data from teradata based on sql script provided
def data_pull(input_script, output_file):
    # looking for credentials
    with open('Teradata/Teradata Variables.txt', 'r') as f:
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
    # finding directory path to project folder
    current_directory = os.getcwd()
    # variable to hold excel document with system path
    excelFile = current_directory + excel_doc

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