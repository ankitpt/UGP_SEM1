import pandas as pd

import numpy as np
import math

df=pd.read_csv("BSNL.csv")
ndf=df[['Site Name','Cell ID','LAC','Latitude','Longitude','Alpha']].copy()

ndf=ndf.rename(columns = {'Latitude':'Lat'})
ndf=ndf.rename(columns = {'Longitude':'Long'})
#ndf=ndf.rename(columns = {'Unique_ID':'SiteID'})
ndf=ndf.rename(columns = {'Alpha':'Azimuth'})
ndf=ndf.rename(columns = {'Site Name':'SiteName'})
#ndf=ndf.rename(columns = {'Cell_Name':'Description'})
#ndf=ndf.rename(columns = {'Site_Addre':'Address'})
#ndf=ndf.rename(columns = {'City_Town':'City'})



#ndf['Beam_Width'] = 120.0
#ndf['Down_Tilt'] = 
#ndf['HgAbvSeaLv'] = 15.0
#ndf['Province']=' '
#ndf['Structure_Height']=' '
#ndf['Structure_Notes']=' '
#ndf['State']='Madhya Pradesh'
#ndf['Postal_Code']=' '
#ndf['Structure_Type']='Lattice'
#ndf['Address']='Bhopal_MP'
#ndf['Sector_Latitude']=' '
#ndf['Sector_Longitude']=' '
#ndf.dropna(subset=['Lat','Long','Azimuth'])
#ndf.dropna(axis=0, how='any', subset=['Lat','Long','Azimuth'])

ndf['Sector_Radius']=10.0
ndf['Lat'] = pd.to_numeric(ndf['Lat'], errors='coerce')
ndf['Long'] = pd.to_numeric(ndf['Long'], errors='coerce')




lat = np.radians(ndf['Lat']) #Current lat point converted to radians
lon = np.radians(ndf['Long']) #Current long point converted to radians
d=ndf['Sector_Radius']
R = 6378.1 #Radius of the Earth
#brng = 1.57 #Bearing is 90 degrees converted to radians.
#d = 15 #Distance in km

#def lati()

ndf['Azimuth'] = ndf['Azimuth'].apply(pd.to_numeric, errors='coerce')
ndf=ndf.dropna(axis=0, subset=['Lat','Long','Azimuth'])
#ndf['Azimuth'] = ndf[ndf['Azimuth'].apply(lambda x: isinstance(x, (float, np.float64)))]


ndf['wkt']=' ';
#ndf=ndf.sort_values('CellID')
#ndf['SectorNum']=ndf.groupby(['SiteName']).cumcount()+1
ndf['Azimuth']= ndf['Azimuth']-(ndf['Azimuth']//360)*360
ndf = ndf.sort_values(['Lat','Long','Azimuth'])
ndf['SectorNum']=ndf.groupby(['Lat','Long'])['Azimuth'].rank(method='dense')
#ndf['SectorNum']= ndf.groupby('SiteName')['SectorNum'].rank
ndf['Angle']=0

ndf = ndf.drop_duplicates(subset=['Lat','Long','Azimuth'])


#This loop calculates extent of coverage for each cell ID
for index, row in enumerate(ndf.iterrows()):
    
 try:
     
     if(index==len(ndf)-1 or ndf['SectorNum'].values[index+1]==1 ):
         temp=abs(row[1][5]-ndf['Azimuth'].values[int(index-row[1][8]+1)])
         if temp<180 :
             ndf['Angle'].values[index]=ndf['Azimuth'].values[index]+temp/2.0
         else:
             temp=360-temp
             ndf['Angle'].values[index]=ndf['Azimuth'].values[index]+temp/2.0
         #break
         #ndf['Angle'][index]=abs(row['Azimuth']-ndf['Azimuth'][index+1])
     else:
#       ndf['Angle'][index]=abs(row['Azimuth']-ndf['Azimuth'][index-row['SectorNum']+1])
       temp2=abs(row[1][5]-ndf['Azimuth'].values[index+1])
       if temp2<180:
           ndf['Angle'].values[index]=ndf['Azimuth'].values[index]+temp2/2.0
       else :
           temp2=360-temp2
           ndf['Angle'].values[index]=ndf['Azimuth'].values[index]+temp2/2.0
    
       
       
 except:
  #   print index 
     continue


#def segments1(k):
 #global ndf
 
lat1=np.arcsin(np.sin(lat)*np.cos(d/R) +np.cos(lat)*np.sin(d/R)*np.cos(np.radians(ndf['Angle'])))

lon1=lon + np.arctan2(np.sin(np.radians(ndf['Angle']))*np.sin(d/R)*np.cos(lat),np.cos(d/R)-np.sin(lat)*np.sin(lat1))


ndf['lat1']=np.degrees(lat1)
ndf['lon1']=np.degrees(lon1)
 
 
#ndf['wkt']='POLYGON(('+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+','+ndf['lon1'].map(str)+' '+ndf['lat1'].map(str)+','+ndf['lon2'].map(str)+' '+ndf['lat2'].map(str)+','+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+'))'
ndf['wkt']=ndf['wkt'].map(str)+ndf['lon1'].map(str)+' '+ndf['lat1'].map(str)+','
#new = ndf[['Cell_ID','wkt']].copy()
 
 
 #return ndf

#def segments2(k):
 #global ndf
 
 
 
 #lat2=np.arcsin( np.sin(lat)*np.cos(d/R) +np.cos(lat)*np.sin(d/R)*np.cos(np.radians(ndf['Azimuth']-ndf['Beam_Width']/k)))

 #lon2=lon + np.arctan2(np.sin(np.radians(ndf['Azimuth']-ndf['Beam_Width']/k))*np.sin(d/R)*np.cos(lat),np.cos(d/R)-np.sin(lat)*np.sin(lat2))
 
#For assigning each cell ID EXCEPT the FIRST ONE, other pair of coordinates derieved from previous cell ID extent coordinates 
ndf['lat2']=0
ndf['lat2'] = ndf['lat1'].shift().where(ndf['SectorNum'] != 1)

ndf['lon2']=0
ndf['lon2'] = ndf['lon1'].shift().where(ndf['SectorNum'] != 1)


#for assigning 1st cell ID at each site the other pair of cordinates 

for index, row in enumerate(ndf.iterrows()):
   try: 
    if math.isnan(row[1][13]):
        k=1
        #if index+k<=len(ndf)-1:
        while ndf['SectorNum'].values[index+k]!=1:
                k=k+1
                if index+k>len(ndf)-1:
                    break;
        
        ndf['lat2'].values[index]=ndf['lat1'].values[index+k-1]
        ndf['lon2'].values[index]=ndf['lon1'].values[index+k-1]
# ndf['lat2']=np.degrees(lat2)
 #ndf['lon2']=np.degrees(lon2)
   except:
       continue

 
#ndf['wkt']='POLYGON(('+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+','+ndf['lon1'].map(str)+' '+ndf['lat1'].map(str)+','+ndf['lon2'].map(str)+' '+ndf['lat2'].map(str)+','+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+'))'
ndf['wkt']=ndf['wkt'].map(str)+ndf['lon2'].map(str)+' '+ndf['lat2'].map(str)+','
#new = ndf[['Cell_ID','wkt']].copy()
 
 
 #return ndf

#dirc=[2,8/3.0,4,8];
#dirc2=[8,4,8/3.0,2];
#for k in dirc:
    
 #   segments1(k)
#for k in dirc2:
 #   segments2(k)

#ndf['nwkt']='POLYGON((' + ndf['Long'].map(str)+ndf['Lat'].map(str)+ndf['wkt'].map(str)+ndf['Long'].map(str)+ndf['Lat'].map(str)+'))'

ndf['nwkt']='POLYGON(('+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+','+ndf['wkt'].map(str)+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+'))'

ndf['Final_CID'] = ndf['LAC'].astype(str).str.zfill(2) + ndf['Cell ID'].astype(str).str.zfill(3)


ndf.to_csv('mobnet_processed_bsnl.csv',index=False)