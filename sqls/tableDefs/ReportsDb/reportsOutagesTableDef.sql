CREATE TABLE REPORTING_WEB_UI_UAT.REAL_TIME_OUTAGE (
  ID NUMBER(*, 0) NOT NULL,
  ENTITY_ID NUMBER(*, 0) NOT NULL,
  ELEMENT_ID NUMBER(*, 0) NOT NULL,
  OUTAGE_DATE DATE NOT NULL,
  OUTAGE_TIME VARCHAR2(20 BYTE) NOT NULL,
  EXPECTED_DATE DATE,
  EXPECTED_TIME VARCHAR2(20 BYTE),
  REVIVED_DATE DATE,
  REVIVED_TIME VARCHAR2(20 BYTE),
  OPENING_CODE VARCHAR2(500 BYTE),
  CLOSING_CODE VARCHAR2(500 BYTE),
  RELAY_INDICATION_SENDING_ID NUMBER(*, 0),
  RELAY_INDICATION_RECIEVING_ID NUMBER(*, 0),
  LOAD_OR_GENERATORTEXT NUMBER(*, 0),
  CREATED_DATE TIMESTAMP(6),
  MODIFIED_DATE TIMESTAMP(6),
  OUTAGE_REMARKS VARCHAR2(500 BYTE),
  SHUT_DOWN_TYPE NUMBER(*, 0) NOT NULL,
  REASON_ID NUMBER(*, 0) NOT NULL,
  IS_DELETED CHAR(1 BYTE) DEFAULT 'N',
  CREATED_BY NUMBER(*, 0),
  MODIFIED_BY NUMBER(*, 0),
  REVIVAL_REMARKS VARCHAR2(500 BYTE),
  REGION_ID NUMBER NOT NULL,
  ELEMENTNAME VARCHAR2(200 BYTE),
  SHUTDOWNREQUEST_ID NUMBER,
  LOAD_AFFECTED NUMBER,
  LOAD_AFFECTED_AREA VARCHAR2(100 BYTE),
  GENERATION_AFFECTED NUMBER,
  IS_LOAD_OR_GEN_AFFECTED NUMBER(*, 0),
  GENERATION_AFFECTED_PLANT VARCHAR2(200 BYTE),
  SHUTDOWN_TAG_ID NUMBER(38, 0)
) LOGGING TABLESPACE USERS PCTFREE 10 INITRANS 1 STORAGE (
  INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS UNLIMITED BUFFER_POOL DEFAULT
) NOCOMPRESS NOPARALLEL