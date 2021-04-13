###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import numpy as np

import sys
sys.path.append("..")

from financepy.finutils.turing_day_count import TuringDayCountTypes
from financepy.finutils.turing_date import TuringDate
from financepy.market.volatility.turing_ibor_cap_vol_curve import TuringIborCapVolCurve

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)

##########################################################################


def test_FinCapVolCurve():

    # Reproduces example in Table 32.1 of Hull Book
    valuationDate = TuringDate(1, 1, 2020)

    capVolDates = []
    capletVolTenor = "1Y"
    numPeriods = 10
    capletDt = valuationDate

    capVolDates.append(valuationDate)

    for i in range(0, numPeriods):
        capletDt = capletDt.addTenor(capletVolTenor)
        capVolDates.append(capletDt)

    capVolatilities = [0.0, 15.50, 18.25, 17.91, 17.74, 17.27,
                       16.79, 16.30, 16.01, 15.76, 15.54]
    capVolatilities = np.array(capVolatilities)/100.0

    dayCountType = TuringDayCountTypes.ACT_ACT_ISDA
    volCurve = TuringIborCapVolCurve(valuationDate,
                                     capVolDates,
                                     capVolatilities,
                                     dayCountType)

    testCases.header("DATE", "CAPVOL", "CAPLETVOL")
    for dt in capVolDates:
        capFloorVol = volCurve.capVol(dt)
        capFloorLetVol = volCurve.capletVol(dt)
        testCases.print("%s" % dt,
                        "%7.3f" % (capFloorVol*100.0),
                        "%7.2f" % (capFloorLetVol*100.0))

##########################################################################


test_FinCapVolCurve()
testCases.compareTestCases()
