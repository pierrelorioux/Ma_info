import MySQLdb
import sys
import json
import time
import subprocess

#open the output file where the data will be written
with open("data/data.json", "w") as outfile:

        #connect to the ushahidi database
        connection = MySQLdb.connect (host = "", user = "", passwd = "", db = "")
        # prepare a cursor object
        cursor = connection.cursor ()
        # execute the SQL query that will join the locations table to the incident table and give use the coordinates and the date of add. Only for Active incident
        cursor.execute("SELECT t1.incident_dateadd, t2.latitude , t2.longitude FROM incident AS t1 INNER JOIN location AS t2 ON t1.location_id = t2.id WHERE t1.incident_active = 1")
        #get the total number of rows
        numrows = cursor.rowcount
        #string that starts the geojson output and add the date of update of the file
        outfile.write('{ "type": "FeatureCollection","last_update":\"'+str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())) +'\", "features":')
        lsp = []
        for x in xrange(0,numrows):
                row = cursor.fetchone()
                out = '{"type": "Feature", "properties":{"incident_dateadd":\"'+str(row[0])+'"}, "geometry": { "type": "Point", "coordinates": ['+str(round(row[2],2))+','+str(round(row[1],2))+']}}'
                lsp.append(out)
        #a bit of cleaning, we replace the ' by nothing
        chaine_complete = str(lsp).replace("'","")
        #and write all the data
        outfile.write(chaine_complete)
        #close the geoson string
        outfile.write('}')
#close the outfile
outfile.close()
# close the cursor object
cursor.close ()
# close the connection
connection.close ()

#Copy the file to www/var/public/map
subprocess.call(['cp', '-r', '/home/cartong/mapps/data/data.json', '/var/www/publicmap/map/'])
sys.exit()
