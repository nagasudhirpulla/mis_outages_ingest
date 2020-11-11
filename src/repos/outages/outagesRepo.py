import cx_Oracle
from src.repos.outages.getOutages import getOutages
from src.repos.outages.getTransElOutages import getTransElOutages
from src.repos.outages.getMajorGenOutages import getMajorGenUnitOutages
from src.repos.outages.getLongTimeUnrevForcedOtgs import getLongTimeUnrevivedForcedOutages
from src.repos.outages.getPwcIdsForSync import getPwcIdsForSync
from src.typeDefs.outages import IOutages
from src.typeDefs.outage import IOutage
import datetime as dt
from typing import List


class OutagesRepo():
    """Repository class for outages data of application
    """
    localConStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConf (DbConfig): database connection string
        """
        self.localConStr = dbConStr

    def insertOutages(self, outages: IOutages) -> bool:
        """inserts outages into the app db

        Args:
            outages (IOutages): outages to be inserted

        Returns:
            bool: returns true if process is ok
        """
        # get connection with raw data table
        conLocal = cx_Oracle.connect(self.localConStr)

        isInsertSuccess = True
        try:
            # column names of the raw data table
            colNames = outages['columns']
            # get cursor for raw data table
            curLocal = conLocal.cursor()

            # text for sql place holders
            sqlPlceHldrsTxt = ','.join([':{0}'.format(x+1)
                                        for x in range(len(colNames))])

            # delete the rows which are already present
            pwcIdColInd = colNames.index('PWC_ID')
            pwcIds = [(x[pwcIdColInd],) for x in outages['rows']]
            curLocal.executemany(
                "delete from outage_events where PWC_ID=:1", pwcIds)

            # insert the raw data
            ouatageEvntsInsSql = 'insert into mis_warehouse.outage_events({0}) values ({1})'.format(
                ','.join(colNames), sqlPlceHldrsTxt)

            curLocal.executemany(ouatageEvntsInsSql, outages['rows'])

            # commit the changes
            conLocal.commit()
        except Exception as e:
            isInsertSuccess = False
            print('Error while bulk insertion of outage events into raw data db')
            print(e)
        finally:
            # closing database cursor and connection
            if curLocal is not None:
                curLocal.close()
            conLocal.close()
        return isInsertSuccess

    def getOutages(self, startDt: dt.datetime, endDt: dt.datetime) -> List[IOutage]:
        """get outages

        Args:
            startDt (dt.datetime): fetch window start time
            endDt (dt.datetime): fetch window end time

        Returns:
            List[IOutage]: List of outages
        """
        outages = getOutages(self.localConStr, startDt, endDt)
        return outages

    def getTransElOutages(self, startDt: dt.datetime, endDt: dt.datetime) -> List[IOutage]:
        """get transmission elements outages

        Args:
            startDt (dt.datetime): fetch window start time
            endDt (dt.datetime): fetch window end time

        Returns:
            List[IOutage]: List of transmission element outages
        """
        outages = getTransElOutages(self.localConStr, startDt, endDt)
        return outages

    def getMajorGenOutages(self, startDt: dt.datetime, endDt: dt.datetime) -> List[IOutage]:
        """get transmission elements outages

        Args:
            startDt (dt.datetime): fetch window start time
            endDt (dt.datetime): fetch window end time

        Returns:
            List[IOutage]: List of outages
        """
        outages = getMajorGenUnitOutages(self.localConStr, startDt, endDt)
        return outages

    def getLongTimeUnrevivedForcedOutages(self, startDt: dt.datetime, endDt: dt.datetime) -> List[IOutage]:
        """get Long Time Unrevived Forced Outages

        Args:
            startDt (dt.datetime): fetch window start time
            endDt (dt.datetime): fetch window end time

        Returns:
            List[IOutage]: List of outages
        """
        outages = getLongTimeUnrevivedForcedOutages(
            self.localConStr, startDt, endDt)
        return outages
    
    def getPwcIdsForSync(self, startDt: dt.datetime, endDt: dt.datetime) -> List[int]:
        """get pwcIds from app db for syncing with vendor DB

        Args:
            startDt (dt.datetime): fetch window start time
            endDt (dt.datetime): fetch window end time

        Returns:
            List[int]: List pwc Ids
        """
        pwcIds = getPwcIdsForSync(self.localConStr, startDt, endDt)
        return pwcIds
