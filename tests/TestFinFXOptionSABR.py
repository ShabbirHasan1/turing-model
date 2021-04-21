import numpy as np

import sys
sys.path.append("..")

from turing_models.utilities.turing_date import TuringDate
from turing_models.utilities.global_types import TuringOptionTypes
from turing_models.products.fx.fx_vanilla_option import TuringFXVanillaOption
from turing_models.models.model_black_scholes import TuringModelBlackScholes
from turing_models.market.curves.discount_curve_flat import TuringDiscountCurveFlat

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)

##########################################################################


def test_FinFXOptionSABR():

    # UNFINISHED
    # There is no FXAmericanOption class. It is embedded in the FXVanillaOption
    # class. This test just compares it to the European

    valueDate = TuringDate(13, 2, 2018)
    expiryDate = TuringDate(13, 2, 2019)

    # In BS the FX rate is the price in domestic of one unit of foreign
    # In case of EURUSD = 1.3 the domestic currency is USD and foreign is EUR
    # DOM = USD , FOR = EUR
    ccy1CCRate = 0.030  # EUR
    ccy2CCRate = 0.025  # USD

    spotFXRate = 1.20
    strikeFXRate = 1.250
    volatility = 0.10

    notional = 1000000.0

    domDiscountCurve = TuringDiscountCurveFlat(valueDate, ccy2CCRate)
    forDiscountCurve = TuringDiscountCurveFlat(valueDate, ccy1CCRate)

    model = TuringModelBlackScholes(volatility)

    # Two examples to show that changing the notional currency and notional
    # keeps the value unchanged
    notional = 1000000.0

    spotFXRates = np.arange(50, 200, 10)/100.0

    testCases.header("OPTION", "FX_RATE", "VALUE_BS", "VOL_IN", "DIFF")

    for spotFXRate in spotFXRates:

        callOption = TuringFXVanillaOption(expiryDate,
                                           strikeFXRate,
                                        "EURUSD",
                                           TuringOptionTypes.EUROPEAN_CALL,
                                           notional,
                                        "USD")

        valueEuropean = callOption.value(valueDate,
                                         spotFXRate,
                                         domDiscountCurve,
                                         forDiscountCurve,
                                         model)['v']

        callOption = TuringFXVanillaOption(expiryDate,
                                           strikeFXRate,
                                        "EURUSD",
                                           TuringOptionTypes.AMERICAN_CALL,
                                           1000000,
                                        "USD")

        valueAmerican = callOption.value(valueDate,
                                         spotFXRate,
                                         domDiscountCurve,
                                         forDiscountCurve,
                                         model)['v']

        diff = (valueAmerican - valueEuropean)

        testCases.print("CALL:",
                        "%9.6f" % spotFXRate,
                        "%9.7f" % valueEuropean,
                        "%9.7f" % valueAmerican,
                        "%9.7f" % diff)

    testCases.header("OPTION", "FX_RATE", "VALUE_BS", "VOL_IN", "DIFF")

    for spotFXRate in spotFXRates:

        callOption = TuringFXVanillaOption(expiryDate,
                                           strikeFXRate,
                                        "EURUSD",
                                           TuringOptionTypes.EUROPEAN_PUT,
                                           1000000,
                                        "USD")

        valueEuropean = callOption.value(valueDate,
                                         spotFXRate,
                                         domDiscountCurve,
                                         forDiscountCurve,
                                         model)['v']

        callOption = TuringFXVanillaOption(expiryDate,
                                           strikeFXRate,
                                        "EURUSD",
                                           TuringOptionTypes.AMERICAN_PUT,
                                           1000000,
                                        "USD")

        valueAmerican = callOption.value(valueDate,
                                         spotFXRate,
                                         domDiscountCurve,
                                         forDiscountCurve,
                                         model)['v']

        diff = (valueAmerican - valueEuropean)
        testCases.print("PUT:",
                        "%9.6f" % spotFXRate,
                        "%9.7f" % valueEuropean,
                        "%9.7f" % valueAmerican,
                        "%9.7f" % diff)

###############################################################################


test_FinFXOptionSABR()
testCases.compareTestCases()
