# mine info



#### A Python script that will connect to the ushahidi DB, round the coordinates to only 2 digits and create a geojson

Use SSH to connect to the server
In the cartong folder and that where we're going to build our repo

```
mkdir mapps
cd mapps
```
Important step first !
Install the python mysql librairy :

```
sudo apt-get install libmysqlclient-dev
sudo apt-get install python-mysqldb
```

Create the data folder that will store: the data...

```
mkdir data
```

Create the python file

```
touch usha_get_loc.py

```
Open the file and copy paste the script usha_get_loc.py that should be in this github repo

```
nano usha_get_loc.py
```

Paste, replace the missing connexion strings by yours.
CTRL X / yes and Enter to save




#### Create the folder where the heatmap will be and where we will push the geojson

Create the publicmap repo

```
cd /var/www/
sudo mkdir publicmap
sudo chown cartong publicmap
```

In it, create a folder map

```
cd publicmap
sudo mkdir map
sudo chown cartong map
```

Go back to the mapps folder

```
cd /home/cartong/mapps/
```

And run the script

```
python usha_get_loc.py
```

And it should have created a data.json file in the data folder and in the /var/www/publicmap/map/ folder

Yeah :)




#### Run the script every hour

```
crontab -e
```
At the end paste the line:
```
 0 * * * * python /home/cartong/mapps/usha_get_loc.py > ~/robo-heat.log 2>&1
```
It will run the script every first minute of every hour and it will create a log file

Yeah :)



#### The heatmap


Install GIT
```
sudo apt-get update
sudo apt-get install git
```
Configure git
```
git config --global user.email "mainfo.cartong@gmail.com"
git config --global user.name "mainfo"
```
Go to the apache repo
```
cd /var/www/publicmap
```
clone the mainfo github repo
```
git clone https://github.com/mainfo/mainfo.github.io.git
```
remove the folder map
```
rm -r map/
```
rename the folder mainfo.github.io to map
```
mv mainfo.github.io map
```
Go in the folder
```
cd map
```
Remove index.html and index_vietnam.html
```
rm index.html
rm index_vietnam.html
```
Rename index_ukraine.html as index.html
```
mv index_ukraine.html index.html
```
You may have to change the source of the data to just data.json after $getJSON
Run the python script to get the data
```
cd /home/cartong/mapps
python usha_get_loc.py
