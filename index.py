'''
This script creates the data mart for outages data in weekly report

## Steps
* read data from reporting software outages database
* transform it to fit the local raw data table and push into it

## links
auto increment in oracle - https://chartio.com/resources/tutorials/how-to-define-an-auto-increment-primary-key-in-oracle/
install Python Docstring Generator for auto documentation of function
'''
import argparse
import datetime as dt
from src.appConfig import getConfig
from src.rawDataCreators.outagesRawDataCreator import createOutageEventsRawData

# get start and end dates from command line
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=6)
# get an instance of argument parser from argparse module
parser = argparse.ArgumentParser()
# setup firstname, lastname arguements
parser.add_argument('--start_date', help="Enter Start date in yyyy-mm-dd format",default=dt.datetime.strftime(startDate, '%Y-%m-%d'))
parser.add_argument('--end_date', help="Enter last date in yyyy-mm-dd format",default=dt.datetime.strftime(endDate, '%Y-%m-%d'))
# get the dictionary of command line inputs entered by the user
args = parser.parse_args()
# access each command line input from the dictionary
startDate = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
endDate = dt.datetime.strptime(args.end_date, '%Y-%m-%d')

startDate = startDate.replace(hour=0, minute=0, second=0, microsecond=0)
endDate = endDate.replace(hour=23, minute=59, second=59, microsecond=0)
# get application config
appConfig = getConfig()

# create outages raw data between start and end dates
isRawDataCreationSuccess = createOutageEventsRawData(appConfig, startDate, endDate)

if isRawDataCreationSuccess:
    print('raw outages data creation done...')
else:
    print('raw outages data creation failure...')
