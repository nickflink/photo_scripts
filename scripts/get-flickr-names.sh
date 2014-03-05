#!/bin/bash
FLICKR_NAMES_FILE="./flickr_names.txt"
PG_CONTENT=`curl -s -L http://www.flickr.com/photos/nickflink/page1/`;
PG_COUNT=`echo "$PG_CONTENT"|grep -E -o "data-page-count=\"[0-9]*"|awk '{sub("data-page-count=\"","");print}'`
echo "found $PG_COUNT page(s)"
PG_COUNT=4
echo "using $PG_COUNT page(s)"
touch $FLICKR_NAMES_FILE
for PG in `jot - 1 $PG_COUNT`; do 
  CURL_PG="http://www.flickr.com/photos/nickflink/page$PG/"
  echo "curling [curl -s -L http://www.flickr.com/photos/nickflink/page$PG/]..."
  curl -s -L $CURL_PG/|grep --color "</p></div></div></div></div><a name="|grep -E -o "alt=\"[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_[0-9][0-9]-[0-9][0-9]-[0-9][0-9]_[a-z0-9]*"|awk '{sub("alt=\"","");print}' >> $FLICKR_NAMES_FILE
done

#for i in `echo "1 2 3"`; do curl -s -L http://www.flickr.com/photos/nickflink/page$i/|grep --color "</p></div></div></div></div><a name="|grep -E -o "alt=\"[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_[0-9][0-9]-[0-9][0-9]-[0-9][0-9]_[a-z0-9]*"|awk '{sub("alt=\"","");print}';done
