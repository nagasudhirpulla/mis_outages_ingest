import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.outage import IOutage
from src.utils.stringUtils import removeRedundantRemarks


def getOutages(conStr: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IOutage]:
    """fetch transmission element outages for a start and end dates, where
    outage time between start and end time
    revived time between start and end time
    Args:
        conStr (str): connection string to app database
        startDt (dt.datetime): start date of report time scope
        endDt (dt.datetime): end date of report time scope
    Returns:
        List[IOutage]: list of outage objects that contain the following data
        element_name, owners, capacity, outage date, outage time, revival date, revival time, reason
    """
    # connect to app database
    con = cx_Oracle.connect(conStr)

    # sql query to fetch the outages
    outagesFetchSql = '''select oe.ELEMENT_NAME, ENTITY_NAME,
    oe.OWNERS, oe.CAPACITY,
    oe.OUTAGE_DATETIME, oe.REVIVED_DATETIME,
    oe.OUTAGE_REMARKS, oe.REASON, oe.shutdown_tag, oe.SHUTDOWN_TYPENAME
    from mis_warehouse.outage_events oe 
    where 
    (oe.OUTAGE_DATETIME between :1 and :2) 
    or (oe.REVIVED_DATETIME between :1 and :2)
    or (oe.OUTAGE_DATETIME <= :1 and oe.REVIVED_DATETIME >= :2)
    or (oe.OUTAGE_DATETIME <= :1 and oe.REVIVED_DATETIME IS NULL)
    order by oe.OUTAGE_DATETIME desc
    '''

    # get cursor and execute fetch sql
    cur = con.cursor()
    cur.execute(outagesFetchSql, (startDt, endDt))
    colNames = [row[0] for row in cur.description]
    targetColumns = ['ELEMENT_NAME', 'ENTITY_NAME', 'OWNERS', 'CAPACITY',
                     'OUTAGE_DATETIME', 'REVIVED_DATETIME', 'OUTAGE_REMARKS', 'REASON', 'SHUTDOWN_TAG', 'SHUTDOWN_TYPENAME']
    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return []
    # print(colNames)

    # fetch all rows
    dbRows = cur.fetchall()

    # initialise outages to be returned
    outages: List[IOutage] = []

    elNameInd = colNames.index('ELEMENT_NAME')
    elTypeInd = colNames.index('ENTITY_NAME')
    ownersInd = colNames.index('OWNERS')
    capInd = colNames.index('CAPACITY')
    outDtInd = colNames.index('OUTAGE_DATETIME')
    reviveDtInd = colNames.index('REVIVED_DATETIME')
    remarksInd = colNames.index('OUTAGE_REMARKS')
    reasonInd = colNames.index('REASON')
    outageTagInd = colNames.index('SHUTDOWN_TAG')
    outageTypeInd = colNames.index('SHUTDOWN_TYPENAME')

    # iterate through each row to populate result outage rows
    for row in dbRows:
        elName: str = row[elNameInd]
        elType: str = row[elTypeInd]
        owners: str = row[ownersInd]
        voltLvl: str = str(row[capInd])
        outDateStr: str = dt.datetime.strftime(row[outDtInd], "%Y-%m-%d")
        outTimeStr: str = dt.datetime.strftime(row[outDtInd], "%H:%M")
        revivalDateStr: str = 'Still out'
        revivalTimeStr: str = 'Still out'
        revivalDt = row[reviveDtInd]
        if not(revivalDt == None):
            revivalDateStr = dt.datetime.strftime(revivalDt, "%Y-%m-%d")
            revivalTimeStr = dt.datetime.strftime(revivalDt, "%H:%M")
        reason = row[reasonInd]
        remarks = row[remarksInd]
        outageType = row[outageTypeInd]
        outageTag = row[outageTagInd]
        outageTag, reason, remarks = removeRedundantRemarks(
            outageTag, reason, remarks)
        reasonStr = ' / '.join([r for r in [outageTag, reason,
                                            remarks] if not(r == None)])
        # create outage record
        outageObj: IOutage = {
            'elName': elName,
            'elType': elType,
            'owners': owners,
            'capacity': voltLvl,
            'outageDate': outDateStr,
            'outageTime': outTimeStr,
            'revivalDate': revivalDateStr,
            'revivalTime': revivalTimeStr,
            'reason': reasonStr,
            'outageType': outageType
        }
        outages.append(outageObj)
    return outages
