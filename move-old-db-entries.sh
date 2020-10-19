#!/bin/bash

bdate=`date --date "4 weeks ago" +"%F"`
ddate=`date --date "4 weeks ago" +"%Y%m%d"`
tweek=`date +%V`
fweek=$((tweek%4))

if [[ $fweek == 0 ]]
then
  query="BEGIN; "
  query+="DROP TABLE IF EXISTS vms_backup_$ddate; "
  query+="CREATE TABLE vms_backup_$ddate AS SELECT * FROM vms WHERE scandate < '$bdate'; "
  query+="DELETE FROM vms WHERE scandate < '$bdate'; "
  query+="SELECT COUNT(*) FROM vms; "
  query+="SELECT COUNT(*) FROM vms_backup_$ddate; "
  query+="COMMIT; "
  echo "$query" | psql findmyvmdb
else
  echo "BACKUP: Not week 4, skipping, modulo = $fweek"
fi

