# Pandas helper functions

# definition to make a trade name grouping based on first name
def trade_name_grouping(sub_df):
    sub_df['TRADE_NM_GROUPING'] = sub_df['TRADE_NM'].str.split(' ').str[0]
    
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