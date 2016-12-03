#!/bin/bash - 
#===============================================================================
#
#          FILE: run_report.sh
# 
#         USAGE: ./run_report.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Steven R. Nye (), stevennye@mail.weber.edu
#  ORGANIZATION: Weber State University
#       CREATED: 12/03/2016 15:02
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

#Declaration of usage function
usageState()
{
	echo "Usage: ./run_report.sh -u <FTPuser> -p <FTPpw> -e <email> -f <begDate> -t <endDate>"
	echo "All arguments are REQUIRED"
}

#Declaration of help function
helpFun()
{
	if [[ "$1" == "--help" ]]
	then
		echo "Usage: ./run_report.sh -u <FTPuser> -p <FTPpw> -e <email> -f <begDate> -t <endDate>"
		echo "--help Print this help message"
		echo "-u specifies the FTP user"
		echo "-p specifies the FTP user's password"
		echo "-e specifies the user's email"
		echo "-f specifies the beginning date"
		echo "-t specifies the end date"
		echo "With no arguments it provides a usage statement"
		exit
	fi
}

#Call help function with first parameter
helpFun "$1"

#Start getopts
while getopts ":u:p:e:f:t:" opt
do
	case $opt in
		u)
			USER=$OPTARG
			;;
		p)
			PASSWD=$OPTARG
			;;
		e)
			EMAIL=$OPTARG
			;;
		f)
			BEGDATE=$OPTARG
			;;
		t)
			ENDDATE=$OPTARG
			;;
		\?)
			echo "Invalid argument, exiting..."
			exit 1
			;;
	esac
done
