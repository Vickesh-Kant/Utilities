import teradatasql
import teradata
import pathlib
import pandas as pd
import pyodbc


# driverless simple query function to output .csv result file
def td_simple_query(input_script, output_file, variable_file):
    # looking for credentials
    with open(variable_file, 'r') as f:
        username = f.readline().rstrip('\n')
        my_password = f.readline().rstrip('\n')
        host = f.readline().rstrip('\n')

    # assigning sql code to a variable
    sql_script1 = input_script
    sql_script_read1 = pathlib.Path(sql_script1).read_text()
    
    # creating a connection using teradatasql
    with teradatasql.connect(host=host, user=username, password=my_password, logmech = 'LDAP') as connect:
        df1 = pd.read_sql(sql_script_read1, connect)
        df1.to_csv(output_file, index = False, encoding='utf-8-sig')

# driverless ddl query function to output .csv result file    
def td_ddl_query(input_script, output_file, variable_file):
    # creating an empty list to hold SQL code split by delimiter
    sql_chunks = []

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

    # creating a connection using teradatasql
    with teradatasql.connect(host=host, user=username, password=my_password, logmech = 'LDAP') as connect:
        with connect.cursor() as cur:
            for i in range(len(sql_chunks)):
                if sql_chunks[i] != sql_chunks[-1]:
                    cur.execute(sql_chunks[i])
                    print ('executed ' + str(i+1) + ' times')
                else:
                    print(sql_chunks[i])
                    df1 = pd.read_sql(sql_chunks[i], connect)
                    df1.to_csv(output_file, index = False)

# function to connect to kcdr server and output result to csv
def kcdr_query(input_script, output_file, variables_file):
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
    df1.to_csv(output_file, index = False, encoding='utf-8-sig')

# definition to pull data from teradata based on sql script provided
def teradata_driver_query(input_script, output_file, variable_file):
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
        df1.to_csv(output_file, index = False, encoding='utf-8-sig')

# definition to pull data from teradata based on sql script provided which contains multiple ddl statements       
def teradata_driver_ddl_query(input_script, output_file, variable_file):
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
                df1.to_csv(output_file, index = False, encoding='utf-8-sig')