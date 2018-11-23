import pandas as pd
import datetime

cdr = pd.read_excel('9644346975 idea.xlsx', header=10,sheet_name=1)
cdr=cdr[['Date','Time', 'Duration In Secs','First Cell ID/LOCATION AREA CODE','Last Cell ID / PDP Address']]
cdr = cdr.iloc[1:81]

cdr=cdr.rename(columns = {'Date':'START_DATE'})
cdr=cdr.rename(columns = {'Duration In Secs':'DUR_IN_SECS'})
cdr=cdr.rename(columns = {'First Cell ID/LOCATION AREA CODE':'FIRST_CELLID'})
cdr=cdr.rename(columns = {'Last Cell ID / PDP Address':'LAST_CELL_ID_ORIGIN'})
cdr=cdr.rename(columns = {'Last Cell ID / PDP Address':'LAST_CELL_ID_ORIGIN'})
cdr=cdr.rename(columns = {'Time':'START_TIM'})

ncdr=cdr[['START_DATE','DUR_IN_SECS','FIRST_CELLID','LAST_CELL_ID_ORIGIN']].copy()

ncdr['FIRST_CELLID'] = ncdr['FIRST_CELLID'].str.replace('-', '')
ncdr['LAST_CELL_ID_ORIGIN'] = ncdr['LAST_CELL_ID_ORIGIN'].str.replace('-', '')

ncdr['START_DATE']=pd.to_datetime(ncdr.START_DATE.astype(str)) + pd.to_timedelta(cdr.START_TIM.astype(str), unit='s')

ncdr['END_DATE'] = pd.to_datetime(ncdr['START_DATE'].astype(str)) + pd.to_timedelta(ncdr['DUR_IN_SECS'].astype(int), unit='s')

ncdr['START_DATE_wot'] = [d.date() for d in ncdr['START_DATE']]
ncdr['START_TIME'] = [d.time() for d in ncdr['START_DATE']]

ncdr['END_DATE_wot'] = [d.date() for d in ncdr['END_DATE']]
ncdr['END_TIME'] = [d.time() for d in ncdr['END_DATE']]


del ncdr['START_DATE']
del ncdr['END_DATE']

ncdr = ncdr[['START_DATE_wot','START_TIME','DUR_IN_SECS','FIRST_CELLID','END_DATE_wot','END_TIME','LAST_CELL_ID_ORIGIN' ]]

ctid=pd.read_csv('intersect_IDEA_MP.csv')
ctid=ctid[['up','down','CGI1','DIVISION','Descriptio','District','ZONE_','Zone','Railway_Br','ID',]]
ctid['CGI1'] = ctid['CGI1'].str.replace('-', '')


new1=pd.merge(ncdr, ctid, how='inner', left_on=['FIRST_CELLID'], right_on=['CGI1'])
new2=pd.merge(ncdr, ctid, how='inner', left_on=['LAST_CELL_ID_ORIGIN'], right_on=['CGI1'])

del new1['END_TIME']
del new2['START_TIME']
del new1['END_DATE_wot']
del new2['START_DATE_wot']



del new1['CGI1']
del new2['CGI1']
del new1['FIRST_CELLID']
del new2['FIRST_CELLID']
del new1['LAST_CELL_ID_ORIGIN']
del new2['LAST_CELL_ID_ORIGIN']
del new1['DUR_IN_SECS']
del new2['DUR_IN_SECS']




comb = pd.concat([new1, new2], ignore_index=True)
comb['Time']=comb['START_TIME'].fillna(comb['END_TIME'])
comb['Date']=comb['START_DATE_wot'].fillna(comb['END_DATE_wot'])
del comb['END_TIME']
del comb['START_TIME']
del comb['START_DATE_wot']
del comb['END_DATE_wot']



comb = comb.sort_values(by=['Date','Time'],ascending=True)
comb=comb[['Date','Time','ID','up','down','Zone','ZONE_','Railway_Br','District','Descriptio','DIVISION']]
comb.to_csv('result_idea.csv',index=False)