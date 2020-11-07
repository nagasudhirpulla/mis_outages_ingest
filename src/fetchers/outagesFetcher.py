import datetime as dt
import cx_Oracle
import pandas as pd
from typing import Dict
from src.typeDefs.outages import IOutages
from src.utils.timeUtils import getTimeDeltaFromDbStr
from src.utils.stringUtils import extractVoltFromName
from src.fetchers.acTransLineCktOwnersFetcher import getOwnersForAcTransLineCktIds
from src.fetchers.bayOwnersFetcher import getOwnersForBayIds
from src.fetchers.busOwnersFetcher import getOwnersForBusIds
from src.fetchers.busReactorOwnersFetcher import getOwnersForBusReactorIds
from src.fetchers.compensatorOwnersFetcher import getOwnersForCompensatorIds
from src.fetchers.fscOwnersFetcher import getOwnersForFscIds
from src.fetchers.genUnitOwnersFetcher import getOwnersForGenUnitIds
from src.fetchers.hvdcLineCktOwnersFetcher import getOwnersForHvdcLineCktIds
from src.fetchers.hvdcPoleOwnersFetcher import getOwnersForHvdcPoleIds
from src.fetchers.lineReactorOwnersFetcher import getOwnersForLineReactorIds
from src.fetchers.transformerOwnersFetcher import getOwnersForTransformerIds


def fetchOutages(appConfig: dict, startDate: dt.datetime, endDate: dt.datetime) -> IOutages:
    """fetches outages from reports database

    Args:
        appConfig (dict): application configuration
        startDate (dt.datetime): start date
        endDate (dt): end date

    Returns:
        IOutages: Each tuple will have the following attributes
        column names should be
        'PWC_ID', 'ELEMENT_ID', 'ELEMENT_NAME', 'ENTITY_ID', 'ENTITY_NAME', 
        'CAPACITY', 'OUTAGE_DATETIME', 'REVIVED_DATETIME', 
        'CREATED_DATETIME', 'MODIFIED_DATETIME', 'SHUTDOWN_TAG', 
        'SHUTDOWN_TAG_ID', 'SHUTDOWN_TYPENAME', 'SHUT_DOWN_TYPE_ID', 
        'OUTAGE_REMARKS', 'REASON', 'REASON_ID', 'REVIVAL_REMARKS', 
        'REGION_ID', 'SHUTDOWNREQUEST_ID', 'OWNERS'
    """
    # get the reports connection string
    reportsConnStr = appConfig['reportsConStr']

    # connect to reports database
    con = cx_Oracle.connect(reportsConnStr)

    # sql query to fetch the outages
    outagesFetchSql = '''select rto.ID as pwc_id, rto.ELEMENT_ID,rto.ELEMENTNAME as ELEMENT_NAME,
    rto.ENTITY_ID, ent_master.ENTITY_NAME, gen_unit.installed_capacity as CAPACITY, rto.OUTAGE_DATE as OUTAGE_DATETIME, 
    rto.REVIVED_DATE as REVIVED_DATETIME, rto.CREATED_DATE as CREATED_DATETIME, 
    rto.MODIFIED_DATE as MODIFIED_DATETIME, sd_tag.name as shutdown_tag,rto.SHUTDOWN_TAG_ID, 
    sd_type.name as shutdown_typename,rto.SHUT_DOWN_TYPE as SHUT_DOWN_TYPE_ID, rto.OUTAGE_REMARKS, 
    reas.reason,rto.REASON_ID, rto.REVIVAL_REMARKS, rto.REGION_ID, 
    rto.SHUTDOWNREQUEST_ID,rto.OUTAGE_TIME, rto.REVIVED_TIME
    from REPORTING_WEB_UI_UAT.real_time_outage rto 
    left join REPORTING_WEB_UI_UAT.outage_reason reas on reas.id = rto.reason_id
    left join REPORTING_WEB_UI_UAT.shutdown_outage_tag sd_tag on sd_tag.id = rto.shutdown_tag_id
    left join REPORTING_WEB_UI_UAT.shutdown_outage_type sd_type on sd_type.id = rto.shut_down_type
    left join REPORTING_WEB_UI_UAT.entity_master ent_master on ent_master.id = rto.ENTITY_ID
    left join REPORTING_WEB_UI_UAT.generating_unit gen_unit on gen_unit.id = rto.element_id 
    where (rto.OUTAGE_DATE between :1 and :2) or (rto.revived_date between :1 and :2) 
    or (rto.MODIFIED_DATE between :1 and :2) or (rto.CREATED_DATE between :1 and :2)'''
    cur = con.cursor()
    cur.execute(outagesFetchSql, (startDate, endDate))
    colNames = [row[0] for row in cur.description]
    # print(colNames)
    colNames = colNames[0:-2]
    colNames.append('OWNERS')
    dbRows = cur.fetchall()
    # print(dbRows)
    instCapIndexInRow: int = 5
    outDateIndexInRow: int = 6
    revDateIndexInRow: int = 7
    elemIdIndexInRow: int = 1
    elemIdNameIndexInRow: int = 2
    elemTypeIndexInRow: int = 4

    # initialize owners dictionary
    acTransLineCktOwners: Dict[int, str] = {}
    bayOwners: Dict[int, str] = {}
    busOwners: Dict[int, str] = {}
    busReactorOwners: Dict[int, str] = {}
    compensatorOwners: Dict[int, str] = {}
    fscOwners: Dict[int, str] = {}
    genUnitOwners: Dict[int, str] = {}
    hvdcLineCktOwners: Dict[int, str] = {}
    hvdcPoleOwners: Dict[int, str] = {}
    lineReactorOwners: Dict[int, str] = {}
    transfomerOwners: Dict[int, str] = {}

    # iterate through db rows
    for rIter in range(len(dbRows)):
        # convert tuple to list to facilitate manipulation
        dbRows[rIter] = list(dbRows[rIter])

        # get the element Id and element type of outage entry
        elemName = dbRows[rIter][elemIdNameIndexInRow]
        elemId = dbRows[rIter][elemIdIndexInRow]
        elemType = dbRows[rIter][elemTypeIndexInRow]
        if elemType == 'AC_TRANSMISSION_LINE_CIRCUIT':
            acTransLineCktOwners[elemId] = ''
        elif elemType == 'GENERATING_UNIT':
            genUnitOwners[elemId] = ''
        elif elemType == 'FSC':
            fscOwners[elemId] = ''
        elif elemType == 'HVDC_LINE_CIRCUIT':
            hvdcLineCktOwners[elemId] = ''
        elif elemType == 'BUS REACTOR':
            busReactorOwners[elemId] = ''
        elif elemType == 'LINE_REACTOR':
            lineReactorOwners[elemId] = ''
        elif elemType == 'TRANSFORMER':
            transfomerOwners[elemId] = ''
        elif elemType == 'HVDC POLE':
            hvdcPoleOwners[elemId] = ''
        elif elemType == 'BUS':
            busOwners[elemId] = ''
        elif elemType == 'Bay':
            bayOwners[elemId] = ''
        elif elemType in ['TCSC', 'MSR', 'MSC', 'STATCOM']:
            compensatorOwners[elemId] = ''

        # convert installed capacity to string
        instCap = dbRows[rIter][instCapIndexInRow]
        if elemType == 'GENERATING_UNIT' and not(pd.isnull(instCap)):
            instCap = str(instCap)
        else:
            instCap = extractVoltFromName(elemType, elemName)
        dbRows[rIter][instCapIndexInRow] = instCap

        outageDateTime = dbRows[rIter][outDateIndexInRow]
        if not pd.isnull(outageDateTime):
            # convert string to time delta
            outTimeStr = dbRows[rIter][-2]
            outTimeDelta = getTimeDeltaFromDbStr(outTimeStr)
            # strip off hours and minute components
            outageDateTime = outageDateTime.replace(
                hour=0, minute=0, second=0, microsecond=0)
            # add out time to out date to get outage timestamp
            outageDateTime += outTimeDelta
            dbRows[rIter][outDateIndexInRow] = outageDateTime

        revivalDateTime = dbRows[rIter][revDateIndexInRow]
        if not pd.isnull(revivalDateTime):
            # convert string to time delta
            revTimeStr = dbRows[rIter][-1]
            revTimeDelta = getTimeDeltaFromDbStr(revTimeStr)
            # strip off hours and minute components
            revivalDateTime = revivalDateTime.replace(
                hour=0, minute=0, second=0, microsecond=0)
            # add revival time to out date to get revival timestamp
            revivalDateTime += revTimeDelta
            dbRows[rIter][revDateIndexInRow] = revivalDateTime

        # remove last 2 column of the row
        dbRows[rIter] = dbRows[rIter][0:-2]

    # fetch owners for each type separately
    acTransLineCktOwners = getOwnersForAcTransLineCktIds(
        reportsConnStr, list(acTransLineCktOwners.keys()))

    bayOwners = getOwnersForBayIds(reportsConnStr, list(bayOwners.keys()))

    busOwners = getOwnersForBusIds(reportsConnStr, list(busOwners.keys()))

    busReactorOwners = getOwnersForBusReactorIds(
        reportsConnStr, list(busReactorOwners.keys()))

    compensatorOwners = getOwnersForCompensatorIds(
        reportsConnStr, list(compensatorOwners.keys()))

    fscOwners = getOwnersForFscIds(reportsConnStr, list(fscOwners.keys()))

    genUnitOwners = getOwnersForGenUnitIds(
        reportsConnStr, list(genUnitOwners.keys()))

    hvdcLineCktOwners = getOwnersForHvdcLineCktIds(
        reportsConnStr, list(hvdcLineCktOwners.keys()))

    hvdcPoleOwners = getOwnersForHvdcPoleIds(
        reportsConnStr, list(hvdcPoleOwners.keys()))

    lineReactorOwners = getOwnersForLineReactorIds(
        reportsConnStr, list(lineReactorOwners.keys()))

    transfomerOwners = getOwnersForTransformerIds(
        reportsConnStr, list(transfomerOwners.keys()))

    # iterate through db rows and assign owner string to each row
    for rIter in range(len(dbRows)):
        elemId = dbRows[rIter][elemIdIndexInRow]
        elemType = dbRows[rIter][elemTypeIndexInRow]
        if elemType == 'AC_TRANSMISSION_LINE_CIRCUIT':
            if elemId in acTransLineCktOwners:
                dbRows[rIter].append(acTransLineCktOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        elif elemType == 'GENERATING_UNIT':
            if elemId in genUnitOwners:
                dbRows[rIter].append(genUnitOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        elif elemType == 'FSC':
            if elemId in fscOwners:
                dbRows[rIter].append(fscOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        elif elemType == 'HVDC_LINE_CIRCUIT':
            if elemId in hvdcLineCktOwners:
                dbRows[rIter].append(hvdcLineCktOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        elif elemType == 'BUS REACTOR':
            if elemId in busReactorOwners:
                dbRows[rIter].append(busReactorOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        elif elemType == 'LINE_REACTOR':
            if elemId in lineReactorOwners:
                dbRows[rIter].append(lineReactorOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        elif elemType == 'TRANSFORMER':
            if elemId in transfomerOwners:
                dbRows[rIter].append(transfomerOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        elif elemType == 'HVDC POLE':
            if elemId in hvdcPoleOwners:
                dbRows[rIter].append(hvdcPoleOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        elif elemType == 'BUS':
            if elemId in busOwners:
                dbRows[rIter].append(busOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        elif elemType == 'Bay':
            if elemId in bayOwners:
                dbRows[rIter].append(bayOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        elif elemType in ['TCSC', 'MSR', 'MSC', 'STATCOM']:
            if elemId in compensatorOwners:
                dbRows[rIter].append(compensatorOwners[elemId])
            else:
                dbRows[rIter].append('NA')
        # convert row to tuple
        dbRows[rIter] = tuple(dbRows[rIter])

    return {'columns': colNames, 'rows': dbRows}
