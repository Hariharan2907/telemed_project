# telemed_project

Once repository is cloned into directory on vidal (var/www/cea), enter this command to give permission for files:

chmod o+rx /var/www/cea/telemed_project
find /var/www/cea/telemed_project/static -type d -exec chmod o=rx {} \; -print
find /var/www/cea/telemed_project/static -type f -exec chmod o=r {} \; -print


Check if a flask app is already running by entering: ps aux | grep flask

To kill Flask process: 
kill -9 ppid
#ppid is the second field number from "ps aux | grep flask" command 

In order to start flask on the vidal server: <br/>

cd /var/www/cea <br/>
source cea/bin/activate <br/>
cd telemed_project <br/>
flask run & <br/>
#To log off safely <br/>
exit <br/>

To test flask app on vidal server: 

Use just "flask run" to see all log messages in console. Once done testing, rerun flask via "flask run &" so flask process will run in background and can log off safely by entering "exit". 

