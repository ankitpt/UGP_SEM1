import pandas as pd
import math
import numpy as np

df=pd.read_csv("mnet.csv")
ndf=df[['Cell_ID','Unique_ID', 'Site_id', 'Latitude','Longitude','Alpha','Cell_Name','City_Town']].copy()

ndf=ndf.rename(columns = {'Latitude':'Lat'})
ndf=ndf.rename(columns = {'Longitude':'Long'})
ndf=ndf.rename(columns = {'Unique_ID':'SiteID'})
ndf=ndf.rename(columns = {'Alpha':'Azimuth'})
ndf=ndf.rename(columns = {'Site_id':'SiteName'})
ndf=ndf.rename(columns = {'Cell_Name':'Description'})
#ndf=ndf.rename(columns = {'Site_Addre':'Address'})
ndf=ndf.rename(columns = {'City_Town':'City'})



ndf['Beam_Width'] = 60
ndf['Down_Tilt'] = 0
ndf['HgAbvSeaLv'] = 15
ndf['Province']=' '
ndf['Structure_Height']=' '
ndf['Structure_Notes']=' '
ndf['State']='Madhya Pradesh'
ndf['Postal_Code']=' '
ndf['Structure_Type']='Lattice'
ndf['Address']='Bhopal_MP'
ndf['Sector_Latitude']=' '
ndf['Sector_Longitude']=' '
ndf['Sector_Radius']=10



ndf['SectorNum']=ndf.groupby(['SiteID']).cumcount()+1


lat = np.radians(ndf['Lat']) #Current lat point converted to radians
lon = np.radians(ndf['Long']) #Current long point converted to radians
d=ndf['Sector_Radius']
R = 6378.1 #Radius of the Earth
#brng = 1.57 #Bearing is 90 degrees converted to radians.
#d = 15 #Distance in km

#def lati()
ndf=ndf.dropna(axis=0, subset=[['Azimuth']])



ndf['wkt']=' ';

 
def segments1(k):
 global ndf
 
 lat1=np.arcsin(np.sin(lat)*np.cos(d/R) +np.cos(lat)*np.sin(d/R)*np.cos(np.radians(ndf['Azimuth']+(ndf['Beam_Width']/k))))

 lon1=lon + np.arctan2(np.radians(ndf['Azimuth']+ndf['Beam_Width']/k)*np.sin(d/R)*np.cos(lat),np.cos(d/R)-np.sin(lat)*np.sin(lat1))


 ndf['lat1']=np.degrees(lat1)
 ndf['lon1']=np.degrees(lon1)
 
 
#ndf['wkt']='POLYGON(('+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+','+ndf['lon1'].map(str)+' '+ndf['lat1'].map(str)+','+ndf['lon2'].map(str)+' '+ndf['lat2'].map(str)+','+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+'))'
 ndf['wkt']=ndf['wkt'].map(str)+ndf['lon1'].map(str)+' '+ndf['lat1'].map(str)+','
#new = ndf[['Cell_ID','wkt']].copy()
 
 
 return ndf

def segments2(k):
 global ndf
 
 
 lat2=np.arcsin( np.sin(lat)*np.cos(d/R) +np.cos(lat)*np.sin(d/R)*np.cos(np.radians(ndf['Azimuth']-ndf['Beam_Width']/k)))

 lon2=lon + np.arctan2(np.radians(ndf['Azimuth']-ndf['Beam_Width']/k)*np.sin(d/R)*np.cos(lat),np.cos(d/R)-np.sin(lat)*np.sin(lat2))


 ndf['lat2']=np.degrees(lat2)
 ndf['lon2']=np.degrees(lon2)

 
#ndf['wkt']='POLYGON(('+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+','+ndf['lon1'].map(str)+' '+ndf['lat1'].map(str)+','+ndf['lon2'].map(str)+' '+ndf['lat2'].map(str)+','+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+'))'
 ndf['wkt']=ndf['wkt'].map(str)+ndf['lon2'].map(str)+' '+ndf['lat2'].map(str)+','
#new = ndf[['Cell_ID','wkt']].copy()
 
 
 return ndf

dirc=[2,4];

for k in dirc:
    
    segments1(k)
for k in dirc:
    segments2(k)

#ndf['nwkt']='POLYGON((' + ndf['Long'].map(str)+ndf['Lat'].map(str)+ndf['wkt'].map(str)+ndf['Long'].map(str)+ndf['Lat'].map(str)+'))'

ndf['nwkt']='POLYGON(('+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+','+ndf['wkt'].map(str)+ndf['Long'].map(str)+' '+ndf['Lat'].map(str)+'))'

ndf.to_csv('mobnet_processed.csv',index=False)