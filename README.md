# UGP_SEM1
A project on developing modular programmes for tracking movement of individuals along railway track 

Steps 
a) Read CDR data - cdr_read and obtain Cell IDs for querying
b) Query above Cell IDs into ct_id database obtained from cell_track.py (QGIS) to get Track ID and associated pair of stations
   cell_track.py - Used to convert QGIS excel data (obtained from mobnet.py and spatial analysis) into .db file as ct_id
   mobnet_read.py - Used to generate coverage polygons for mobile towers
c) Query above obtained Track IDs (Requisition)  along with date and time into railway operation data. 
