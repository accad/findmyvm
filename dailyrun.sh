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

/home/cecadmin/findmyvm2/getcluster-from-vcs.py >> $LOGFILE
echo -n "getcluster-from-vcs.py done: " >> $LOGFILE
date >> $LOGFILE
echo >> $LOGFILE 

/home/cecadmin/findmyvm2/create-index.py > /var/www/roweb/findmyvm/index.html
/home/cecadmin/findmyvm2/create-vcs-list.py > /var/www/roweb/findmyvm/vc.html
/home/cecadmin/findmyvm2/create-cluster-list.py > /var/www/roweb/findmyvm/clusters.html

echo -n "create-index done: " >> $LOGFILE
date >> $LOGFILE
echo >> $LOGFILE
echo >> $LOGFILE

cat $LOGFILE | /usr/bin/mail -s "$SUBJECT" nicholas.accad@delllabs.net
#cat $LOGFILE | /usr/bin/mail -s "findmyvm2 dailyrun" accadn@cec.lab.emc.com
/usr/bin/rm $LOGFILE
