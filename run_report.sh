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
	echo "Usage: ./run_report.sh -u <FTPuser> -p <FTPpw> -e <email> -f <begDate YYYYMMDD> -t <endDate YYYYMMDD>"
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
		echo "-f specifies the beginning date (FORMAT: YYYYMMDD)"
		echo "-t specifies the end date (FORMAT: YYYYMMDD)"
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

#Check for required arguments
if [[ ! "$USER" || ! "$PASSWD" || ! "$EMAIL" || ! "$BEGDATE" || ! "$ENDDATE" ]]
then
	usageState
	exit 1
fi

#Call create_report.py
python3 create_report.py "$BEGDATE" "$ENDDATE"

#Check exit code
if [[ $? -eq 0 ]]
then
	echo "Successfully created report"
	#zip file
	zip -r "company_trans.zip" "company_trans_""$BEGDATE""_""$ENDDATE"".dat"
	#Connect to FTP
	HOST='137.190.19.103'
	echo "Using "$USER"'s FTP account"
	ftp -inv $HOST << EOF
	user $USER $PASSWD
	cd . 
	put company_trans.zip
	bye
EOF
elif [[ $? -eq -1 ]]
	mail -s "The create_report program exited with code -1" $EMAIL <<< "Bad Input parameters $BEGDATE $ENDDATE"
	echo "Email sent to $EMAIL"
	exit 1
else
	mail -s "The create_report program exited with code -2" $EMAIL <<< "No transactions available from $BEGDATE to $ENDDATE"
	echo "Email sent to $EMAIL"
	exit 1
fi

