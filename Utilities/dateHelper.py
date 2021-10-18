from datetime import date
import numpy as np
import pandas as pd
import pkgutil

# static file path
calendar = pkgutil.get_data(__name__, "Workbook/FY_Cal.xlsx")

def date_helper(date, return_value):
    cal_workbook = (calendar)
    df1 = pd.read_excel(cal_workbook)
    df1['Date'] = pd.to_datetime(df1['Date'])
    date  = np.datetime64(date)
    matching_row = df1.loc[df1['Date'] == date]
    if return_value == 'fiscal_yr':
        return (matching_row['Fiscal Year'].values)
    elif return_value == 'fiscal_qtr':
        return (matching_row['Quarter'].values)
    elif return_value == 'month_num':
        return (matching_row['Month No.'].values)
    elif return_value == 'month_nm':
        return (matching_row['Month Nm.'].values)
    elif return_value == 'period_num':
        return (matching_row['Period No.'].values)
    elif return_value == 'period_id':
        return (matching_row['Period ID'].values)
    elif return_value == 'fiscal_wk':
        return (matching_row['Fiscal Week'].values)
    elif return_value == 'day':
        return (matching_row['Day of Year'].values)
    else:
        return print('Invalid choice of return value')

def ytd_period_list(date):
    
    date  = np.datetime64(date)
    
    # list variables to hold period ID's
    list_current_yr = []

    # calling date helper to find out what the fiscal period number and fiscal year is based on today's date
    current_period = date_helper(date, 'period_num')
    current_year = date_helper(date, 'fiscal_yr')
    current_year = int(current_year)

    # finding the prior period based on today's date
    prior_period = int(current_period) - 1
    
    # condition to make sure prior period is 13 if current period is period 1
    if prior_period == 0:
        prior_period = 13
        current_year = current_year - 1

    
    # for loop to create list of periods up to current date - excluding current period
    for i in range(prior_period):
        period_id = str(current_year) + str(i+1).zfill(2)
        list_current_yr.append(period_id)
    
    # returning list of YTD periods minus the current period currently in
    return tuple(list_current_yr)

def prior_year_plus_ytd_period_list(date): 
    
    date  = np.datetime64(date)
    
    # list variables to hold period ID's
    list_current_yr = []
    list_prior_yr = []

    # calling date helper to find out what the fiscal period number and fiscal year is based on today's date
    current_period = date_helper(date, 'period_num')
    current_year = date_helper(date, 'fiscal_yr')
    current_year = int(current_year)
    prior_year = current_year - 1

    # finding the prior period based on today's date
    prior_period = int(current_period) - 1
    
    # condition to make sure prior period is 13 if current period is period 1
    if prior_period == 0:
        prior_period = 13
        current_year = current_year - 1
        prior_year = prior_year - 1

    # for loop to create list of periods up to current date - excluding current period
    for i in range(prior_period):
        period_id = str(current_year) + str(i+1).zfill(2)
        list_current_yr.append(period_id)
        
    for i in range(13):
        period_id = str(prior_year) + str(i+1).zfill(2)
        list_prior_yr.append(period_id)
    
    # returning list of YTD periods minus the current period currently in plus all periods prior year
    return tuple(list_prior_yr + list_current_yr)

def rolling_13_period_list(date):
    date  = np.datetime64(date)
    
    # list variables to hold period ID's
    list_current_yr = []
    list_prior_yr = []

    # calling date helper to find out what the fiscal period number and fiscal year is based on today's date
    current_period = date_helper(date, 'period_num')
    current_year = date_helper(date, 'fiscal_yr')
    current_year = int(current_year)
    prior_year = current_year - 1

    # finding the prior period based on today's date
    prior_period = int(current_period) - 1
    
    # condition to make sure prior period is 13 if current period is period 1
    if prior_period == 0:
        prior_period = 13
        current_year = current_year - 1
        prior_year = prior_year - 1

    # find out number of periods from prior year
    periods_from_prior_yr = 13 - prior_period

    # for loop to create list of periods up to current date - excluding current period
    for i in range(prior_period):
        period_id = str(current_year) + str(i+1).zfill(2)
        list_current_yr.append(period_id)
        
    for i in range(13, (13 - periods_from_prior_yr), -1):
        period_id = str(prior_year) + str(i).zfill(2)
        list_prior_yr.append(period_id)
    
    # returning list of YTD periods minus the current period currently in plus all periods prior year
    return tuple(list_prior_yr + list_current_yr)