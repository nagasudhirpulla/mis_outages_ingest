import unittest
from src.utils.stringUtils import extractVoltFromName, removeRedundantRemarks
import datetime as dt
from src.appConfig import getConfig


class TestStringUtils(unittest.TestCase):
    appConfig = None

    def test_fsc(self) -> None:
        """tests extract voltage level from fsc name
        """
        elemType = 'FSC'
        elemName = '400KV-APL-MUNDRA-SAMI-1 FSC@ SAMI'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '400KV')

    def test_acTransLineCkt(self) -> None:
        """tests extract voltage level from acTransLineCkt name
        """
        elemType = 'AC_TRANSMISSION_LINE_CIRCUIT'
        elemName = '132KV-BINA-MP-MORWA-1'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '132KV')

    def test_hvdcLineCkt(self) -> None:
        """tests extract voltage level from hvdcLineCkt name
        """
        elemType = 'HVDC_LINE_CIRCUIT'
        elemName = 'HVDC400KV-Vindyachal(PS)-RIHAND-1'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '400KV')

    def test_busReactor(self) -> None:
        """tests extract voltage level from busReactor name
        """
        elemType = 'BUS REACTOR'
        elemName = 'AKOLA (2) - 765KV B/R 1'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '765KV')

    def test_lineReactor(self) -> None:
        """tests extract voltage level from lineReactor name
        """
        elemType = 'LINE_REACTOR'
        elemName = '400KV-AKOLA-AURANGABAD-2 L/R@ AKOLA - 400KV'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '400KV')

    def test_transformer(self) -> None:
        """tests extract voltage level from transformer name
        """
        elemType = 'TRANSFORMER'
        elemName = '1200KV/400KV BINA-ICT-1'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '1200KV/400KV')

    def test_hvdcPole(self) -> None:
        """tests extract voltage level from hvdc pole
        """
        elemType = 'HVDC POLE'
        elemName = 'HVDC 500KV APL  POLE 1'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '500KV')

    def test_bus(self) -> None:
        """tests extract voltage level from bus
        """
        elemType = 'BUS'
        elemName = 'ACBIL - 400KV - BUS 2'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '400KV')

    def test_bay(self) -> None:
        """tests extract voltage level from bay
        """
        elemType = 'Bay'
        elemName = 'MAIN BAY - 765KV/400KV BHOPAL-ICT-1 AND BHOPAL - 765KV - BUS 2 at BHOPAL - 765KV'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '765KV')

    def test_tcsc(self) -> None:
        """tests extract voltage level from bay
        """
        elemType = 'TCSC'
        elemName = 'AURANGABAD - 400KV - BUS 2 MSR@AURANGABAD'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '400KV')

    def test_removeRedundantRemarks(self) -> None:
        """tests the function that removes redundant remarks
        """
        tag, reas, rem = removeRedundantRemarks("Outage", "RSD", "RSD")
        self.assertTrue((tag == None) and (reas == "RSD") and (rem == "RSD"))

        tag, reas, rem = removeRedundantRemarks("RSD", "RSD ", " rsd")
        self.assertTrue((tag == "RSD") and (reas == None) and (rem == None))

        tag, reas, rem = removeRedundantRemarks("RSD", "something", " rsd")
        self.assertTrue((tag == "RSD") and (
            reas == "something") and (rem == None))

        tag, reas, rem = removeRedundantRemarks("RSD", " rsd", "somthing")
        self.assertTrue((tag == "RSD") and (
            reas == None) and (rem == "somthing"))
