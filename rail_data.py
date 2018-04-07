import urllib
import json


serviceurl = 'https://api.railwayapi.com/v2/between/source/CNB/dest/NDLS/date/5-1-2019/apikey/g5hfzos9dg/'

#while True:
 #address1 = 'misrod-MSO'
 #address2='bhopaljn-BPL' 

# if len(address1) < 1 : break

url = serviceurl
print 'Retrieving', url
uh = urllib.urlopen(url)
data = uh.read()
print 'Retrieved',len(data),'characters'
 
js = json.loads(str(data))
total_trains = js["total"]

train_no=list()
train_arr_dest=list()
train_dept_src=list()


for i in range(total_trains):
    train_no.append(js["trains"][i]["number"])
    train_arr_dest.append(js["trains"][i]["dest_arrival_time"])
    train_dept_src.append(js["trains"][i]["src_departure_time"])
    


 #except: js = None
 #if 'status' not in js or js['status'] != 'OK':
  #print '==== Failure To Retrieve ===='
  #print data
  #continue

