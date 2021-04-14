###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import time

import sys
sys.path.append("..")

from turingmodel.products.equity.turing_equity_american_option import TuringEquityAmericanOption
from turingmodel.turingutils.turing_global_types import TuringOptionTypes
from turingmodel.market.curves.turing_discount_curve_flat import TuringDiscountCurveFlat
from turingmodel.models.turing_model_black_scholes import TuringModelBlackScholes, TuringModelBlackScholesTypes
from turingmodel.turingutils.turing_date import TuringDate

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)

###############################################################################

def testFinEquityAmericanOption():

    valueDate = TuringDate(1, 1, 2016)
    expiryDate = TuringDate(1, 1, 2017)
    stockPrice = 50.0
    interestRate = 0.06
    dividendYield = 0.04
    volatility = 0.40
    strikePrice = 50.0

    discountCurve = TuringDiscountCurveFlat(valueDate, interestRate)
    dividendCurve = TuringDiscountCurveFlat(valueDate, dividendYield)

    testCases.banner("================== EUROPEAN PUT =======================")

    putOption = TuringEquityAmericanOption(expiryDate, strikePrice, TuringOptionTypes.EUROPEAN_PUT)

    model = TuringModelBlackScholes(volatility,
                                    TuringModelBlackScholesTypes.CRR_TREE,
                                    100)

    value = putOption.value(valueDate, stockPrice, discountCurve, dividendCurve, model)
    delta = putOption.delta(valueDate, stockPrice, discountCurve, dividendCurve, model)
    gamma = putOption.gamma(valueDate, stockPrice, discountCurve, dividendCurve, model)
    theta = putOption.theta(valueDate, stockPrice, discountCurve, dividendCurve, model)

    testCases.header("OPTION_TYPE", "VALUE", "DELTA", "GAMMA", "THETA")
    testCases.print("EUROPEAN_PUT_BS", value, delta, gamma, theta)

    option = TuringEquityAmericanOption(expiryDate, strikePrice, TuringOptionTypes.EUROPEAN_PUT)

    testCases.header("OPTION_TYPE", "NUMSTEPS", "VALUE DELTA GAMMA THETA", "TIME")

    numStepsList = [100, 200, 500, 1000, 2000]

    for numSteps in numStepsList:

        model = TuringModelBlackScholes(volatility,
                                        TuringModelBlackScholesTypes.CRR_TREE,
                                        numSteps)

        start = time.time()
        results = option.value(valueDate, stockPrice, discountCurve, dividendCurve, model)
        end = time.time()
        duration = end - start
        testCases.print("EUROPEAN_PUT_TREE", numSteps, results, duration)

    testCases.banner("================== AMERICAN PUT =======================")

    option = TuringEquityAmericanOption(
        expiryDate,
        strikePrice,
        TuringOptionTypes.AMERICAN_PUT)

    testCases.header(
        "OPTION_TYPE",
        "NUMSTEPS",
        "VALUE DELTA GAMMA THETA",
        "TIME")

    for numSteps in numStepsList:

        model = TuringModelBlackScholes(volatility,
                                        TuringModelBlackScholesTypes.CRR_TREE,
                                        numSteps)

        start = time.time()
        results = option.value(valueDate, stockPrice, discountCurve, dividendCurve, model)
        end = time.time()
        duration = end - start
        testCases.print("AMERICAN_PUT", numSteps, results, duration)

    testCases.banner(
        "================== EUROPEAN CALL =======================")

    callOption = TuringEquityAmericanOption(
        expiryDate,
        strikePrice,
        TuringOptionTypes.EUROPEAN_CALL)
    value = callOption.value(valueDate, stockPrice, discountCurve, dividendCurve, model)
    delta = callOption.delta(valueDate, stockPrice, discountCurve, dividendCurve, model)
    gamma = callOption.gamma(valueDate, stockPrice, discountCurve, dividendCurve, model)
    theta = callOption.theta(valueDate, stockPrice, discountCurve, dividendCurve, model)

    testCases.header("OPTION_TYPE", "VALUE", "DELTA", "GAMMA", "THETA")
    testCases.print("EUROPEAN_CALL_BS", value, delta, gamma, theta)

    option = TuringEquityAmericanOption(
        expiryDate,
        strikePrice,
        TuringOptionTypes.EUROPEAN_CALL)

    testCases.header(
        "OPTION_TYPE",
        "NUMSTEPS",
        "VALUE DELTA GAMMA THETA",
        "TIME")

    for numSteps in numStepsList:

        model = TuringModelBlackScholes(volatility,
                                        TuringModelBlackScholesTypes.CRR_TREE,
                                        numSteps)
        start = time.time()
        results = option.value(valueDate, stockPrice, discountCurve, 
                               dividendCurve, model)
        end = time.time()
        duration = end - start
        testCases.print("EUROPEAN_CALL_TREE", numSteps, results, duration)

    testCases.banner(
        "================== AMERICAN CALL =======================")
    testCases.header(
        "OPTION_TYPE",
        "NUMSTEPS",
        "VALUE DELTA GAMMA THETA",
        "TIME")

    option = TuringEquityAmericanOption(expiryDate, strikePrice,
                                        TuringOptionTypes.AMERICAN_CALL)

    for numSteps in numStepsList:

        model = TuringModelBlackScholes(volatility,
                                        TuringModelBlackScholesTypes.CRR_TREE,
                                        numSteps)

        start = time.time()

        results = option.value(valueDate, stockPrice, discountCurve, 
                               dividendCurve, model)

        end = time.time()
        duration = end - start
        testCases.print("AMERICAN_CALL", numSteps, results, duration)

#    FinTest.TestReport(filename)

###############################################################################


testFinEquityAmericanOption()
testCases.compareTestCases()
