#! /usr/bin/env pythons
import sys
from dbconfig import read_db_config
import mysql.connector
from mysql.connector import Error, MySQLConnection
import datetime

def convertStartDate(date):
    """
    Takes a date in YYYYMMDD format and changes it to YYYY-MM-DD hh:mm format
    Args:
        date: a date as a string in YYYYMMDD format
    returns:
        a date as a string in YYYY-MM-DD 00:00
    """
    if len(date) != 8:
        exit(1)
    try: 
        numDate = int(date)
    except:
        exit(1)
    date = date[:4] + '-' + date[5:6] + '-' + date[6:] + ' 00:00'
    return date

def convertEndDate(date):
    """
    Takes a date in YYYYMMDD format and changes it to YYYY-MM-DD hh:mm format
    Args:
        date: a date as a string in YYYYMMDD format
    returns:
        a date as a string in YYYY-MM-DD 23:59
    """
    if len(date) != 8:
        exit(1)
    try: 
        numDate = int(date)
    except:
        exit(1)
    date = date[:4] + '-' + date[5:6] + '-' + date[6:] + ' 23:59'
    return date

def createReport(startDate, endDate):
    """
    Creates a report of transactions based on given start and end dates
    Args:
        startDate: date as string in YYYY-MM-DD hh:mm format
        endDate: date as string in YYY-MM-DD hh:mm format
    returns:
        report as a string
    """

    db_config = read_db_config()
    try:
        print("Connecting to MySQL database...")
        conn = MySQLConnection(**db_config)
        
        if conn.is_connected():
            print("Connection is established")
        else:
            print("Connection failed")
            return ""

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trans t JOIN trans_line tl ON tl.trans_id = t.trans_id JOIN products p ON p.prod_num = tl.prod_num" )
        
        rows = cursor.fetchall()

        if cursor.rowcount == 0:
            print("No transactions in dates")
            exit(2)

        for row in rows:
            print(row[1])
    except Error as error:
        print(error)
    
    finally:
        cursor.close()
        conn.close()
        print("Connection closed")


def main():
    """
    Test Function
    """
    createReport(convertStartDate("20160101"), convertEndDate("20161231"))
    return

if __name__=="__main__":
    main()
    exit(0)
