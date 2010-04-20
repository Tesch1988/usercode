if [ $# -eq 2 ]
then
  offset=0
elif [ $# -eq 3 ]
then
  offset=$3
else
  exit
fi

s=`echo $2`
    #  echo $s
if [ $s == '.' ]
then
#  echo "ls /pnfs/physik.rwth-aachen.de/cms/store/user/magass/$1"
    srmls -offset=$offset srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/$1/$2 | grep -v WARNING | grep pnfs | awk '{print $2}' | sed s/"\.\/"/""/g | cut -c51- | grep "/" 
  else
    srmls -offset=$offset srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/$1/$2 | grep -v WARNING | grep pnfs | awk '{print $2}' | sed s/"\.\/"/""/g | cut -c51- | grep "/" | sed s:$s:: | cut -c2-
  fi
  count=`srmls -offset=$offset srm://grid-srm.physik.rwth-aachen.de:8443/pnfs/physik.rwth-aachen.de/cms/store/user/$1/$2 | grep -v WARNING | grep pnfs | grep -v SURL | sed s:/pnfs/physik.rwth-aachen.de/cms/store/user/$1/::g  | grep root | wc -l`
#  echo "  #Files : " $count
  if [ $count -eq 999 ]
  then
    let offset=offset+999
    mysrmls.sh $1 $offset
fi 

