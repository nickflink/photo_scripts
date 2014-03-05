#!/bin/bash
USAGE="organize-dir.sh searchdir organizeddir";
if [ "$#" != "2" ]; then
	echo "$USAGE";
	exit 0;
fi
echo searching: $1
echo storing $2

if [ "`which md5sum`" != "" ]; then
	MD5_COMMAND="md5sum"
fi
if [ "$MD5_COMMAND" == "" -a "`which md5`" != "" ]; then
	MD5_COMMAND="md5 -r"
fi

EXIF_SIG="EXIF standard";
TIME_MD5_SEP="_";
for i in `find "$1" -maxdepth 20 -path '*/organized' -prune -o -type f -print;`; do
	echo -n ".";
	FILE_SIG="`file $i|egrep -o "$EXIF_SIG"`";
	if [ "$FILE_SIG" == "$EXIF_SIG" ]; then
		echo "";
#echo "get ext";
		EXT=`echo "$i"|awk -F . '{print $NF}'`;
#echo "get time";
		PHOTO_TIME=`exiftool -a -u -g1 "$i" |grep Date\/Time\ Original|awk '{gsub(":", "-");print $4 "_" $5}'`;
#echo "get md5";
		PHOTO_MD5=`$MD5_COMMAND "$i" |awk '{print $1}'`;
#echo "get name";
		PHOTO_NAME="$PHOTO_TIME$TIME_MD5_SEP$PHOTO_MD5";
#echo "get loc";
		PHOTO_LOC="$2$PHOTO_NAME.$EXT";
		echo "cp \"$i\" $PHOTO_LOC"|bash -x;
	fi
done
echo $?;
