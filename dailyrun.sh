#!/bin/sh
LOGFILE=`/usr/bin/mktemp -p ~/findmyvm2/`

SUBJECT="FindMyVM2 DailyRun :: "
SUBJECT+=`date +"%F %T"`

echo -n "findmyvm2 daily run: " > $LOGFILE
date >> $LOGFILE
echo >> $LOGFILE

/home/cecadmin/findmyvm2/test-vcs-conn.py >> $LOGFILE
echo -n "test-vcs-conn done: " >> $LOGFILE
date >> $LOGFILE
echo >> $LOGFILE

/home/cecadmin/findmyvm2/getvms-from-vcs.py >> $LOGFILE
echo -n "getvms-from-vcs done: " >> $LOGFILE
date >> $LOGFILE
echo >> $LOGFILE

/home/cecadmin/findmyvm2/create-index.py > /var/www/roweb/findmyvm/index.html
/home/cecadmin/findmyvm2/create-vcs-list.py > /var/www/roweb/findmyvm/vc.html
echo -n "create-index done: " >> $LOGFILE
date >> $LOGFILE
echo >> $LOGFILE
echo >> $LOGFILE

/home/cecadmin/findmyvm2/getnetworkjson.py -u siterecadmin -p DgT2WfMXiUyZ7NXg -s 10.228.254.152 --api 2.6.1 -o /var/www/roweb/findmyvm/networks.json

### /home/cecadmin/findmyvm2/networks.json

cat $LOGFILE | /usr/bin/mail -s "$SUBJECT" accadn@cec.lab.emc.com
#cat $LOGFILE | /usr/bin/mail -s "findmyvm2 dailyrun" accadn@cec.lab.emc.com
/usr/bin/rm $LOGFILE
