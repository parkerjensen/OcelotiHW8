#!/bin/bash - 
#===============================================================================
#
#          FILE: ftp_file.sh
# 
#         USAGE: ./ftp_file.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Steven R. Nye (), stevennye@mail.weber.edu
#  ORGANIZATION: Weber State University
#       CREATED: 12/04/2016 02:18
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

#Username and Password fron getopts are passed in as $1 and $2
#in the wrapper script
USERN=$1
PASSWD=$2
FILENAME=$3
HOST='137.190.19.103'

echo "Using $USERN FTP account"                                                     
ftp -inv $HOST << EOF
user $USERN $PASSWD
cd .
put $FILENAME
bye
EOF

exit 0
