###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import time

import sys
sys.path.append("..")

from financepy.finutils.turing_global_types import TuringOptionTypes
from financepy.products.fx.turing_fx_float_lookback_option import TuringFXFloatLookbackOption
from financepy.products.fx.turing_fx_fixed_lookback_option import TuringFXFixedLookbackOption
from financepy.market.curves.turing_discount_curve_flat import TuringDiscountCurveFlat
from financepy.finutils.turing_date import TuringDate

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)

###############################################################################

def test_FinEquityLookBackOption():
    valueDate = TuringDate(1, 1, 2015)
    expiryDate = TuringDate(1, 1, 2016)
    stockPrice = 100.0
    volatility = 0.3
    numPathsRange = [10000]
    stockPriceRange = range(90, 110, 5)
    numStepsPerYear = 252

    domesticRate = 0.05
    domesticCurve = TuringDiscountCurveFlat(valueDate, domesticRate)

    foreignRate = 0.02
    foreignCurve = TuringDiscountCurveFlat(valueDate, foreignRate)

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

    optionType = TuringOptionTypes.EUROPEAN_CALL
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = TuringFXFloatLookbackOption(expiryDate, optionType)
            stockMin = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
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

    optionType = TuringOptionTypes.EUROPEAN_CALL
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = TuringFXFloatLookbackOption(expiryDate, optionType)
            stockMin = stockPrice - 10
            value = option.value(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
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

    optionType = TuringOptionTypes.EUROPEAN_PUT
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = TuringFXFloatLookbackOption(expiryDate, optionType)
            stockMax = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
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

    optionType = TuringOptionTypes.EUROPEAN_PUT
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = TuringFXFloatLookbackOption(expiryDate, optionType)
            stockMax = stockPrice + 10
            value = option.value(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
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

    stockPriceRange = range(90, 110, 5)
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

    optionType = TuringOptionTypes.EUROPEAN_CALL
    k = 95.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = TuringFXFixedLookbackOption(expiryDate, optionType, k)
            stockMax = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
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

    optionType = TuringOptionTypes.EUROPEAN_CALL
    k = 100.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = TuringFXFixedLookbackOption(expiryDate, optionType, k)
            stockMax = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
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

    optionType = TuringOptionTypes.EUROPEAN_CALL
    k = 105.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = TuringFXFixedLookbackOption(expiryDate, optionType, k)
            stockMax = stockPrice + 10.0
            value = option.value(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
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

    optionType = TuringOptionTypes.EUROPEAN_PUT
    k = 95.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = TuringFXFixedLookbackOption(expiryDate, optionType, k)
            stockMin = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
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

    optionType = TuringOptionTypes.EUROPEAN_PUT
    k = 100.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = TuringFXFixedLookbackOption(expiryDate, optionType, k)
            stockMin = stockPrice
            value = option.value(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
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

    optionType = TuringOptionTypes.EUROPEAN_PUT
    k = 105.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = TuringFXFixedLookbackOption(expiryDate, optionType, k)
            stockMin = stockPrice - 10.0
            value = option.value(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valueDate,
                stockPrice,
                domesticCurve,
                foreignCurve,
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


test_FinEquityLookBackOption()
testCases.compareTestCases()
