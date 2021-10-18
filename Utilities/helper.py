import pandas as pd
import numpy as np
import teradata
import pathlib
import win32com.client as win32
import pyautogui
import os

def generate_modified_sql_script(sql_code, sql_script_path):
	if os.path.isfile(sql_script_path) == True:
     	 os.remove(sql_script_path)

	with open(sql_script_path, "w+") as f:
			f.writelines(sql_code)
        
def excel_refresh(excel_doc):
    # variable to hold excel file
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


