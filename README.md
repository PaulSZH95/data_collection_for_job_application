# data_collection_for_job_application
Creating a tool to get data for job application.

Project is straightforward. Pull data from popular job websites (mainly in singapore) and then apply analytics. Dynamic websites are harder to collect data and thus
I have seek to extract data from dynamic websites. More to come.

p.s. excel is used now due to habit, will move to mysql or whatever sql (the syntax are mostly the same) in the future

# Demo of gui usage:

https://youtu.be/oCQWBGQyD7Y

take note that it's normal for it to be loading on choices page

# create virtual environment in anaconda:

conda create -n envname python=3.7

conda activate envname

cd ../path_of_requirement.txt/

pip install - r requirements.txt

# usage:

in cli

cd ../app

for windows:

set FLASK_APP=run.py

set FLASK_ENV=development (so you can debug)

//

set FLASK_ENV=production (run as is)

flask run

on browser enter the ip 127.0.0.1:5000, to access the webapp

p.s.

for linux:
use export instead of set.

do also remember to downlowd a linux version of chromedriver, chromedriver attached is for windows only


# updates:

available website: mycareersfuture(sg)

upcoming updates: linkedin and indeed


