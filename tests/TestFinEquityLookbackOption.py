###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import time

import sys
sys.path.append("..")

from financepy.products.equity.turing_equity_float_lookback_option import FinEquityFloatLookbackOption
from financepy.products.equity.turing_equity_fixed_lookback_option import FinEquityFixedLookbackOption
from financepy.finutils.turing_global_types import FinOptionTypes
from financepy.market.curves.turing_discount_curve_flat import FinDiscountCurveFlat
from financepy.finutils.turing_date import FinDate

from FinTestCases import FinTestCases, globalTestCaseMode
testCases = FinTestCases(__file__, globalTestCaseMode)

###############################################################################

def test_FinEquityLookBackOption():
    valueDate = FinDate(1, 1, 2015)
    expiryDate = FinDate(1, 1, 2016)
    stockPrice = 100.0
    volatility = 0.3
    interestRate = 0.05
    dividendYield = 0.01
    numPathsRange = [10000]
    stockPriceRange = range(90, 110, 10)
    numStepsPerYear = 252

    discountCurve = FinDiscountCurveFlat(valueDate, interestRate)
    dividendCurve = FinDiscountCurveFlat(valueDate, dividendYield)

###############################################################################

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "SMIN",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_CALL
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFloatLookbackOption(expiryDate, optionType)
            stockMin = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMin,
                numPaths,
                numStepsPerYear)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                stockMin,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "SMIN",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_CALL
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFloatLookbackOption(expiryDate, optionType)
            stockMin = stockPrice - 10
            value = option.value(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMin,
                numPaths,
                numStepsPerYear)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                stockMin,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "SMAX",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_PUT
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFloatLookbackOption(expiryDate, optionType)
            stockMax = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMax,
                numPaths,
                numStepsPerYear)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                stockMax,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "SMAX",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_PUT
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFloatLookbackOption(expiryDate, optionType)
            stockMax = stockPrice + 10
            value = option.value(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMax,
                numPaths,
                numStepsPerYear)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                stockMax,
                value,
                valueMC,
                diff,
                timeElapsed)

###############################################################################
###############################################################################

    stockPriceRange = range(90, 110, 10)
    numStepsPerYear = 252

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMAX",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_CALL
    k = 95.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiryDate, optionType, k)
            stockMax = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMax,
                numPaths,
                numStepsPerYear)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMax,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMAX",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_CALL
    k = 100.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiryDate, optionType, k)
            stockMax = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMax,
                numPaths,
                numStepsPerYear)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMax,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMAX",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_CALL
    k = 105.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiryDate, optionType, k)
            stockMax = stockPrice + 10.0
            value = option.value(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMax,
                numPaths,
                numStepsPerYear)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMax,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMIN",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_PUT
    k = 95.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiryDate, optionType, k)
            stockMin = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMin,
                numPaths,
                numStepsPerYear)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMin,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMIN",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_PUT
    k = 100.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiryDate, optionType, k)
            stockMin = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMin,
                numPaths,
                numStepsPerYear)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMin,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMIN",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_PUT
    k = 105.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiryDate, optionType, k)
            stockMin = stockPrice - 10.0
            value = option.value(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                discountCurve,
                dividendCurve,
                volatility,
                stockMin,
                numPaths,
                numStepsPerYear)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMin,
                value,
                valueMC,
                diff,
                timeElapsed)

###############################################################################

def test_example():

    expiryDate = FinDate(1, 1, 2021)
    strikePrice = 105.0
    optionTypeCall = FinOptionTypes.EUROPEAN_CALL
    optionTypePut = FinOptionTypes.EUROPEAN_PUT
    lookbackCall = FinEquityFixedLookbackOption(expiryDate, optionTypeCall, strikePrice)
    lookbackPut = FinEquityFixedLookbackOption(expiryDate, optionTypePut, strikePrice)

    valueDate = FinDate(1, 1, 2020)
    interestRate = 0.10
    stockPrice = 100.0
    dividendYield = 0.0
    stockMinMax = 100.0

    discountCurve = FinDiscountCurveFlat(valueDate, interestRate)
    dividendCurve = FinDiscountCurveFlat(valueDate, dividendYield)

    volatilities = [0.30]

    testCases.header("VALUE")
    for vol in volatilities:
        v = lookbackCall.value(valueDate, stockPrice, discountCurve, dividendCurve, vol, stockMinMax)
        testCases.print(v)

###############################################################################

test_example()
#test_FinEquityLookBackOption()
testCases.compareTestCases()
