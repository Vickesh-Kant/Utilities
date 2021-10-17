import teradatasql
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
        df1.to_csv(output_file, index = False)

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
