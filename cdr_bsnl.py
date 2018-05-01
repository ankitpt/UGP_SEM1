import pandas as pd
import datetime

cdr = pd.read_excel('9406930664_542754bpl BSNL.xlsx', header=10,sheet_name=1)
cdr = cdr.iloc[1:]

ncdr=cdr[['START_DATE','DUR_IN_SECS','FIRST_CELLID','LAST_CELL_ID_ORIGIN']].copy()

ncdr['START_DATE']=pd.to_datetime(ncdr.START_DATE.astype(str)) + pd.to_timedelta(cdr.START_TIM.astype(str), unit='s')

ncdr['END_DATE'] = pd.to_datetime(ncdr['START_DATE'].astype(str)) + pd.to_timedelta(ncdr['DUR_IN_SECS'].astype(int), unit='s')

ncdr['START_DATE_wot'] = [d.date() for d in ncdr['START_DATE']]
ncdr['START_TIME'] = [d.time() for d in ncdr['START_DATE']]

ncdr['END_DATE_wot'] = [d.date() for d in ncdr['END_DATE']]
ncdr['END_TIME'] = [d.time() for d in ncdr['END_DATE']]


del ncdr['START_DATE']
del ncdr['END_DATE']

ncdr = ncdr[['START_DATE_wot','START_TIME','DUR_IN_SECS','FIRST_CELLID','END_DATE_wot','END_TIME','LAST_CELL_ID_ORIGIN' ]]

ctid=pd.read_csv('intersect_BSNL_MP.csv')

new=pd.merge(ncdr, ctid, how='inner', left_on=['FIRST_CELLID'], right_on=['Final_CID'])


