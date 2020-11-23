import logging
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter
from logging import Logger
import pandas as pd
from src.appConfig import getConfig

def getAppLogger() -> Logger:
    """get the logger object for logging

    Returns:
        Logger: logger object
    """
    # formatting for log stash
    logstashFormatter = LogstashFormatter(
        message_type='python-logstash',
        extra=dict(application='mis_outages_service'))

    # set app logger name and minimum logging level
    appLogger = logging.getLogger('python-logstash-logger')
    appLogger.setLevel(logging.INFO)

    # configure console logging
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logstashFormatter)
    appLogger.addHandler(streamHandler)

    # get app config
    appConfig = getConfig()

    # configure logstash logging
    host = appConfig["logstash_host"]
    port = appConfig["logstash_port"]
    if not(pd.isna(host)) and not(pd.isna(port)):
        logstashHandler = AsynchronousLogstashHandler(
            host, port, database_path='logstash.db')
        logstashHandler.setFormatter(logstashFormatter)
        appLogger.addHandler(logstashHandler)
    return appLogger
