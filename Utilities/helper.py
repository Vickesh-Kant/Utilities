import pandas as pd
import numpy as np
import teradata
import pathlib
import win32com.client as win32
import pyautogui

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

    pyautogui.rightClick(x, y)
    pyautogui.click(x3, y3)
    pyautogui.click(x4, y4)


