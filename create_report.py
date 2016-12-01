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
        print(date + " Not 8 in length")
        exit(1)
    try: 
        numDate = int(date)
    except:
        print(date + " Not able to become an int")
        exit(1)
    date = date[:4] + '-' + date[4:6] + '-' + date[6:] + ' 00:00'
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
        print(date + " Not 8 in length")
        exit(1)
    try: 
        numDate = int(date)
    except:
        print(date + " Not able to become an int")
        exit(1)
    date = date[:4] + '-' + date[4:6] + '-' + date[6:] + ' 23:59'
    return date

def createReport(startDate, endDate):
    """
    Creates a report of transactions based on given start and end dates
    Args:
        startDate: date as string in YYYYMMDD format
        endDate: date as string in YYYYMMDD format
    returns:
        report as a string
    """

    newStartDate = convertStartDate(startDate)
    newEndDate = convertEndDate(endDate)

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
        cursor.execute("SELECT t.trans_id, trans_date, card_num, qty, amt, p.prod_desc, line_id FROM trans t JOIN trans_line tl ON tl.trans_id = t.trans_id JOIN products p ON p.prod_num = tl.prod_num WHERE trans_date BETWEEN '" + newStartDate + "' AND '"+ newEndDate + "'" )
        stmt = "Getting transactions between " + newStartDate + " and " + newEndDate
        print(stmt)
        
        rows = cursor.fetchall()

        if cursor.rowcount == 0:
            print("No transactions in dates")
            exit(2)

        transaction = []
        transID = -1
        prod2qty = '0'
        prod2amt = '0'
        prod2desc = ''
        prod3qty = '0'
        prod3amt = '0'
        prod3desc = ''
        for row in rows:
            if transID != str(row[0]):
                if transID != -1:
                    transaction.append('{:5s}{:12s}{:6s}{:2s}{:6s}{:10s}{:2s}{:6s}{:10s}{:2s}{:6s}{:10s}'.format(transID.zfill(5), date, card[-6:], prod1qty.zfill(2), prod1amt.zfill(6), prod1desc, prod2qty.zfill(2), prod2amt.zfill(6), prod2desc, prod3qty.zfill(2), prod3amt.zfill(6), prod3desc))
                prod2qty = '0'
                prod2amt = '0'
                prod2desc = ''
                prod3qty = '0'
                prod3amt = '0'
                prod3desc = ''
                transID = str(row[0])
                date = row[1]
                card = row[2]
                prod1qty = str(int(row[3]))
                prod1amt = str("{0:.2f}".format(row[4]))
                prod1amt = prod1amt.replace(".","")
                prod1desc = row[5]
                date = date.strftime('%Y%m%d%H%M')
            else:
                if row[6] == 1:
                    prod2qty = str(int(row[3]))
                    prod2amt = str("{0:.2f}".format(row[4]))
                    prod2amt = prod2amt.replace(".","")
                    prod2desc = row[5]
                if row[6] == 2:
                    prod3qty = str(int(row[3]))
                    prod3amt = str("{0:.2f}".format(row[4]))
                    prod3amt = prod3amt.replace(".","")
                    prod3desc = row[5]
        transaction.append('{:5s}{:12s}{:6s}{:2s}{:6s}{:10s}{:2s}{:6s}{:10s}{:2s}{:6s}{:10s}'.format(transID.zfill(5), date, card[-6:], prod1qty.zfill(2), prod1amt.zfill(6), prod1desc, prod2qty.zfill(2), prod2amt.zfill(6), prod2desc, prod3qty.zfill(2), prod3amt.zfill(6), prod3desc))

        fileName = 'company_trans_' + startDate + '_' + endDate + '.dat'
        newFile = open(fileName, 'w')
        for trans in transaction:
            print(trans)
            newFile.write(trans)
            newFile.write("\n")
            

    except Error as error:
        print(error)
    
    finally:
        cursor.close()
        conn.close()
        print("Connection closed")


def main():
    import sys
    """
    Test Function
    """
    createReport(str(sys.argv[1]), str(sys.argv[2]))
    return

if __name__=="__main__":
    main()
    exit(0)
