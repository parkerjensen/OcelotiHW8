# OcelotiHW8

config.ini - 
  This file contains the configuration to connect to the database (host uersname password database)
  
dbconfig.py - 
  This file reads the config.ini file and connects to the datbase
 
create_report.py
  Contains 3 definitions:
    1. convertStartDate - 
      Takes a date in YYYYMMDD format as an arguments and returns it in YYYY-MM-DD 00:00 format
    2. convertEndDate -
      Takes a date in YYYYMMDD format as an arguments and returns it in YYYY-MM-DD 23:59 format
    3. createReport - 
      Takes startDate and endDate in YYYYMMDD formats as arguments and calls convertStartDate and
      convertEndDate to get properly formatted dates. Calls the dbconfig.py file to open a connection
      to the desired database. Gets all transactions between the start and end dates entered. Creates
      a file that contains all the transaction records.
      
  create_report.py should be called like the example given:
    python3 create_report.py <startDate> <endDate>
    EX: python3 create_report.py 20160123 20160435
