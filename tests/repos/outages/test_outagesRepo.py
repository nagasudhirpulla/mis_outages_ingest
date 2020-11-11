import unittest
from src.repos.outages.outagesRepo import OutagesRepo
import datetime as dt
from src.appConfig import getConfig


class TestOutagesRepo(unittest.TestCase):
    def setUp(self):
        appConfig = getConfig()
        appDbConStr = appConfig['appDbConStr']
        self.outagesRepo = OutagesRepo(appDbConStr)

    def test_getOutages(self) -> None:
        """tests the outages fetching function
        """
        startDate = dt.datetime(2020, 8, 1)
        endDate = dt.datetime(2020, 8, 12)
        outages = self.outagesRepo.getOutages(startDate, endDate)
        self.assertFalse(len(outages) == 0)
    
    def test_getTransElOutages(self) -> None:
        """tests the transmission elements outages fetching function
        """
        startDate = dt.datetime(2020, 8, 1)
        endDate = dt.datetime(2020, 8, 12)
        outages = self.outagesRepo.getTransElOutages(startDate, endDate)
        self.assertFalse(len(outages) == 0)

    def test_getMajorGenOutages(self) -> None:
        """tests the Major Generator outages fetching function
        """
        startDate = dt.datetime(2020, 8, 1)
        endDate = dt.datetime(2020, 8, 12)
        outages = self.outagesRepo.getMajorGenOutages(startDate, endDate)
        self.assertFalse(len(outages) == 0)

    def test_getLongTimeUnrevivedForcedOutages(self) -> None:
        """tests the Long time unrevived forced outages fetching function
        """
        startDate = dt.datetime(2020, 8, 1)
        endDate = dt.datetime(2020, 8, 12)
        outages = self.outagesRepo.getLongTimeUnrevivedForcedOutages(
            startDate, endDate)
        self.assertFalse(len(outages) == 0)

    def test_getPwcIdsForSync(self) -> None:
        """tests the outages pwc ids for sync fetching function
        """
        startDate = dt.datetime(2020, 8, 1)
        endDate = dt.datetime(2020, 8, 12)
        pwcIds = self.outagesRepo.getPwcIdsForSync(startDate, endDate)
        self.assertFalse(len(pwcIds) == 0)
