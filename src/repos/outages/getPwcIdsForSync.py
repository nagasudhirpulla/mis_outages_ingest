import datetime as dt
import cx_Oracle
from typing import List


def getPwcIdsForSync(conStr: str, startDt: dt.datetime, endDt: dt.datetime) -> List[int]:
    """fetch Pwc Ids for outages for a start and end dates 
    for the sake of sync check with pwc db ouutages
    Args:
        conStr (str): connection string to app database
        startDt (dt.datetime): start date of report time scope
        endDt (dt.datetime): end date of report time scope
    Returns:
        List[int]: list of pwc ids of outages in app db
    """
    # connect to app database
    con = cx_Oracle.connect(conStr)

    # sql query to fetch the outages
    outagesFetchSql = '''select oe.PWC_ID
    from mis_warehouse.outage_events oe 
    where (TRUNC(oe.OUTAGE_DATETIME) between :1 and :2) or (TRUNC(oe.REVIVED_DATETIME) between :1 and :2) 
    or (TRUNC(oe.MODIFIED_DATETIME) between :1 and :2) or (TRUNC(oe.CREATED_DATETIME) between :1 and :2)
    '''

    # get cursor and execute fetch sql
    cur = con.cursor()
    cur.execute(outagesFetchSql, (startDt, endDt))
    colNames = [row[0] for row in cur.description]
    targetColumns = ['PWC_ID']
    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return []
    # print(colNames)

    # fetch all rows
    dbRows = cur.fetchall()

    # initialise pwc Ids to be returned
    pwcIds: List[int] = []

    pwcIdInd = colNames.index('PWC_ID')

    # iterate through each row to populate result outage rows
    for row in dbRows:
        pwcId: int = int(row[pwcIdInd])
        pwcIds.append(pwcId)
    return pwcIds
