import os
import datetime as dt

import sys
sys.path.append("..")

from turing_models.utilities.global_types import TuringSwapTypes
from turing_models.products.bonds.bond import TuringYTMCalcType
from turing_models.products.bonds.bond import TuringBond
from turing_models.products.rates.ibor_single_curve import TuringIborSingleCurve
from turing_models.products.rates.ibor_deposit import TuringIborDeposit
from turing_models.products.rates.ibor_swap import TuringIborSwap
from turing_models.utilities.mathematics import ONE_MILLION
from turing_models.utilities.turing_date import TuringDate, fromDatetime
from turing_models.utilities.day_count import TuringDayCountTypes
from turing_models.utilities.frequency import TuringFrequencyTypes
from turing_models.utilities.calendar import TuringCalendarTypes
from fundamental.market.curves.discount_curve_flat import TuringDiscountCurveFlat

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)



##########################################################################

def buildIborCurve(valuationDate):

    depoDCCType = TuringDayCountTypes.THIRTY_E_360_ISDA
    depos = []
    depositRate = 0.050

    depo0 = TuringIborDeposit(
        valuationDate,
        "1D",
        depositRate,
        depoDCCType)

    spotDays = 2
    settlementDate = valuationDate.addWeekDays(spotDays)

    maturityDate = settlementDate.addMonths(1)
    depo1 = TuringIborDeposit(settlementDate,
                              maturityDate,
                              depositRate,
                              depoDCCType)

    maturityDate = settlementDate.addMonths(3)
    depo2 = TuringIborDeposit(
        settlementDate,
        maturityDate,
        depositRate,
        depoDCCType)

    maturityDate = settlementDate.addMonths(6)
    depo3 = TuringIborDeposit(
        settlementDate,
        maturityDate,
        depositRate,
        depoDCCType)

    maturityDate = settlementDate.addMonths(9)
    depo4 = TuringIborDeposit(
        settlementDate,
        maturityDate,
        depositRate,
        depoDCCType)

    maturityDate = settlementDate.addMonths(12)
    depo5 = TuringIborDeposit(
        settlementDate,
        maturityDate,
        depositRate,
        depoDCCType)

    depos.append(depo0)
    depos.append(depo1)
    depos.append(depo2)
    depos.append(depo3)
    depos.append(depo4)
    depos.append(depo5)

    fras = []
    fixedDCCType = TuringDayCountTypes.ACT_365F
    fixedFreqType = TuringFrequencyTypes.SEMI_ANNUAL

    swaps = []

    swapRate = 0.05
    maturityDate = settlementDate.addMonths(24)
    swap1 = TuringIborSwap(
        settlementDate,
        maturityDate,
        TuringSwapTypes.PAY,
        swapRate,
        fixedFreqType,
        fixedDCCType)

#    print(swap1._fixedLeg._paymentDates)

    swaps.append(swap1)

    maturityDate = settlementDate.addMonths(36)
    swap2 = TuringIborSwap(
        settlementDate,
        maturityDate,
        TuringSwapTypes.PAY,
        swapRate,
        fixedFreqType,
        fixedDCCType)
    swaps.append(swap2)

#    print(swap2._fixedLeg._paymentDates)


    maturityDate = settlementDate.addMonths(48)
    swap3 = TuringIborSwap(
        settlementDate,
        maturityDate,
        TuringSwapTypes.PAY,
        swapRate,
        fixedFreqType,
        fixedDCCType)
    swaps.append(swap3)

#    print(swap3._fixedLeg._paymentDates)

    maturityDate = settlementDate.addMonths(60)
    swap4 = TuringIborSwap(
        settlementDate,
        maturityDate,
        TuringSwapTypes.PAY,
        swapRate,
        fixedFreqType,
        fixedDCCType)
    swaps.append(swap4)

#    print(swap4._fixedLeg._paymentDates)

    maturityDate = settlementDate.addMonths(72)
    swap5 = TuringIborSwap(
        settlementDate,
        maturityDate,
        TuringSwapTypes.PAY,
        swapRate,
        fixedFreqType,
        fixedDCCType)
    swaps.append(swap5)

#    print(swap5._fixedLeg._paymentDates)

    maturityDate = settlementDate.addMonths(84)
    swap6 = TuringIborSwap(
        settlementDate,
        maturityDate,
        TuringSwapTypes.PAY,
        swapRate,
        fixedFreqType,
        fixedDCCType)
    swaps.append(swap6)

#    print(swap6._fixedLeg._paymentDates)

    maturityDate = settlementDate.addMonths(96)
    swap7 = TuringIborSwap(
        settlementDate,
        maturityDate,
        TuringSwapTypes.PAY,
        swapRate,
        fixedFreqType,
        fixedDCCType)
    swaps.append(swap7)

#    print(swap7._fixedLeg._paymentDates)

    maturityDate = settlementDate.addMonths(108)
    swap8 = TuringIborSwap(
        settlementDate,
        maturityDate,
        TuringSwapTypes.PAY,
        swapRate,
        fixedFreqType,
        fixedDCCType)
    swaps.append(swap8)

#    print(swap8._fixedLeg._paymentDates)

    maturityDate = settlementDate.addMonths(120)
    swap9 = TuringIborSwap(
        settlementDate,
        maturityDate,
        TuringSwapTypes.PAY,
        swapRate,
        fixedFreqType,
        fixedDCCType)
    swaps.append(swap9)

#    print(swap9._fixedLeg._paymentDates)

    liborCurve = TuringIborSingleCurve(valuationDate,
                                       depos,
                                       fras,
                                       swaps)

    if 1 == 0:
        import numpy as np
        numSteps = 40
        dt = 10 / numSteps
        times = np.linspace(0.0, 10.0, numSteps + 1)

        df0 = 1.0
        for t in times[1:]:
            df1 = liborCurve.df(t)
            fwd = (df0 / df1 - 1.0) / dt
            print(t, df1, fwd)
            df0 = df1

    return liborCurve

##########################################################################


def test_FinBond():

    import pandas as pd
    path = os.path.join(os.path.dirname(__file__), './data/giltBondPrices.txt')
    bondDataFrame = pd.read_csv(path, sep='\t')
    bondDataFrame['mid'] = 0.5*(bondDataFrame['bid'] + bondDataFrame['ask'])

    freqType = TuringFrequencyTypes.SEMI_ANNUAL
    settlementDate = TuringDate(2012, 9, 19)
    face = ONE_MILLION

    for accrualType in TuringDayCountTypes:

        testCases.header("MATURITY", "COUPON", "CLEAN_PRICE", "ACCD_DAYS",
                         "ACCRUED", "YTM")

        for _, bond in bondDataFrame.iterrows():

            dateString = bond['maturity']
            matDatetime = dt.datetime.strptime(dateString, '%d-%b-%y')
            maturityDt = fromDatetime(matDatetime)
            issueDt = TuringDate(2000, maturityDt._m, maturityDt._d)

            coupon = bond['coupon']/100.0
            cleanPrice = bond['mid']
            bond = TuringBond(issueDt, maturityDt,
                              coupon, freqType, accrualType, 100)

            ytm = bond.yieldToMaturity(settlementDate, cleanPrice)
            accd = bond._accruedInterest
            accd_days = bond._accruedDays

            testCases.print("%18s" % maturityDt, "%8.4f" % coupon,
                            "%10.4f" % cleanPrice, "%6.0f" % accd_days,
                            "%10.4f" % accd, "%8.4f" % ytm)

    ###########################################################################
    #  EXAMPLE FROM http://bondtutor.com/btchp4/topic6/topic6.htm

    accrualConvention = TuringDayCountTypes.ACT_ACT_ICMA
    y = 0.062267
    settlementDate = TuringDate(1994, 4, 19)
    issueDate = TuringDate(1990, 7, 15)
    maturityDate = TuringDate(1997, 7, 15)
    coupon = 0.085
    face = ONE_MILLION
    freqType = TuringFrequencyTypes.SEMI_ANNUAL
    bond = TuringBond(issueDate, maturityDate,
                      coupon, freqType, accrualConvention, face)

    testCases.header("FIELD", "VALUE")
    fullPrice = bond.fullPriceFromYTM(settlementDate, y)
    testCases.print("Full Price = ", fullPrice)
    cleanPrice = bond.cleanPriceFromYTM(settlementDate, y)
    testCases.print("Clean Price = ", cleanPrice)
    accd = bond._accruedInterest
    testCases.print("Accrued = ", accd)
    ytm = bond.yieldToMaturity(settlementDate, cleanPrice)
    testCases.print("Yield to Maturity = ", ytm)

    bump = 1e-4
    priceBumpedUp = bond.fullPriceFromYTM(settlementDate, y + bump)
    testCases.print("Price Bumped Up:", priceBumpedUp)

    priceBumpedDn = bond.fullPriceFromYTM(settlementDate, y - bump)
    testCases.print("Price Bumped Dn:", priceBumpedDn)

    durationByBump = -(priceBumpedUp - fullPrice) / bump
    testCases.print("Duration by Bump = ", durationByBump)

    duration = bond.dollarDuration(settlementDate, y)
    testCases.print("Dollar Duration = ", duration)
    testCases.print("Duration Difference:", duration - durationByBump)

    modifiedDuration = bond.modifiedDuration(settlementDate, y)
    testCases.print("Modified Duration = ", modifiedDuration)

    macauleyDuration = bond.macauleyDuration(settlementDate, y)
    testCases.print("Macauley Duration = ", macauleyDuration)

    conv = bond.convexityFromYTM(settlementDate, y)
    testCases.print("Convexity = ", conv)

    # ASSET SWAP SPREAD

    # When the libor curve is the flat bond curve then the ASW is zero by
    # definition
    flatCurve = TuringDiscountCurveFlat(settlementDate,
                                        ytm,
                                        TuringFrequencyTypes.SEMI_ANNUAL)

    testCases.header("FIELD", "VALUE")

    cleanPrice = bond.cleanPriceFromYTM(settlementDate, ytm)
    asw = bond.assetSwapSpread(settlementDate, cleanPrice, flatCurve)
    testCases.print("Discounted on Bond Curve ASW:", asw * 10000)

    # When the libor curve is the Libor curve then the ASW is positive
    liborCurve = buildIborCurve(settlementDate)
    asw = bond.assetSwapSpread(settlementDate, cleanPrice, liborCurve)
    oas = bond.optionAdjustedSpread(settlementDate, cleanPrice, liborCurve)
    testCases.print("Discounted on LIBOR Curve ASW:", asw * 10000)
    testCases.print("Discounted on LIBOR Curve OAS:", oas * 10000)

    p = 90.0
    asw = bond.assetSwapSpread(settlementDate, p, liborCurve)
    oas = bond.optionAdjustedSpread(settlementDate, p, liborCurve)
    testCases.print("Deep discount bond at 90 ASW:", asw * 10000)
    testCases.print("Deep discount bond at 90 OAS:", oas * 10000)

    p = 100.0
    asw = bond.assetSwapSpread(settlementDate, p, liborCurve)
    oas = bond.optionAdjustedSpread(settlementDate, p, liborCurve)
    testCases.print("Par bond at 100 ASW:", asw * 10000)
    testCases.print("Par bond at 100 OAS:", oas * 10000)

    p = 120.0
    asw = bond.assetSwapSpread(settlementDate, p, liborCurve)
    oas = bond.optionAdjustedSpread(settlementDate, p, liborCurve)
    testCases.print("Above par bond at 120 ASW:", asw * 10000)
    testCases.print("Above par bond at 120 OAS:", oas * 10000)

##########################################################################
# https://data.bloomberglp.com/bat/sites/3/2017/07/SF-2017_Paul-Fjeldsted.pdf
# Page 10 TREASURY NOTE SCREENSHOT
##########################################################################

    testCases.banner("BLOOMBERG US TREASURY EXAMPLE")
    settlementDate = TuringDate(2017, 7, 21)
    issueDate = TuringDate(2010, 5, 15)
    maturityDate = TuringDate(2027, 5, 15)
    coupon = 0.02375
    freqType = TuringFrequencyTypes.SEMI_ANNUAL
    accrualType = TuringDayCountTypes.ACT_ACT_ICMA
    face = 100.0

    bond = TuringBond(issueDate,
                      maturityDate,
                      coupon,
                      freqType,
                      accrualType,
                      face,
                      convention=TuringYTMCalcType.UK_DMO)

    testCases.header("FIELD", "VALUE")
    cleanPrice = 99.7808417

    yld = bond.currentYield(cleanPrice)
    testCases.print("Current Yield = ", yld)

    ytm = bond.yieldToMaturity(settlementDate, cleanPrice)
    testCases.print("UK DMO Yield To Maturity = ", ytm)

    bond = TuringBond(issueDate,
                      maturityDate,
                      coupon,
                      freqType,
                      accrualType,
                      face,
                      convention=TuringYTMCalcType.US_STREET)

    ytm = bond.yieldToMaturity(settlementDate, cleanPrice)
    testCases.print("US STREET Yield To Maturity = ", ytm)

    bond = TuringBond(issueDate,
                      maturityDate,
                      coupon,
                      freqType,
                      accrualType,
                      face,
                      convention=TuringYTMCalcType.US_TREASURY)

    ytm = bond.yieldToMaturity(settlementDate, cleanPrice)
    testCases.print("US TREASURY Yield To Maturity = ", ytm)

    fullPrice = bond.fullPriceFromYTM(settlementDate, ytm)
    testCases.print("Full Price = ", fullPrice)

    cleanPrice = bond.cleanPriceFromYTM(settlementDate, ytm)
    testCases.print("Clean Price = ", cleanPrice)

    accd = bond._accruedInterest
    testCases.print("Accrued = ", accd)

    accddays = bond._accruedDays
    testCases.print("Accrued Days = ", accddays)

    duration = bond.dollarDuration(settlementDate, ytm)
    testCases.print("Dollar Duration = ", duration)

    modifiedDuration = bond.modifiedDuration(settlementDate, ytm)
    testCases.print("Modified Duration = ", modifiedDuration)

    macauleyDuration = bond.macauleyDuration(settlementDate, ytm)
    testCases.print("Macauley Duration = ", macauleyDuration)

    conv = bond.convexityFromYTM(settlementDate, ytm)
    testCases.print("Convexity = ", conv)

##########################################################################
# Page 11 APPLE NOTE SCREENSHOT
##########################################################################

    testCases.banner("BLOOMBERG APPLE CORP BOND EXAMPLE")
    settlementDate = TuringDate(2017, 7, 21)
    issueDate = TuringDate(2012, 5, 13)
    maturityDate = TuringDate(2022, 5, 13)
    coupon = 0.027
    freqType = TuringFrequencyTypes.SEMI_ANNUAL
    accrualType = TuringDayCountTypes.THIRTY_E_360_ISDA
    face = 100.0

    bond = TuringBond(issueDate, maturityDate,
                      coupon, freqType, accrualType, face,
                      TuringYTMCalcType.UK_DMO)

    testCases.header("FIELD", "VALUE")
    cleanPrice = 101.581564

    yld = bond.currentYield(cleanPrice)
    testCases.print("Current Yield", yld)

    ytm = bond.yieldToMaturity(settlementDate, cleanPrice)
    testCases.print("UK DMO Yield To Maturity", ytm)

    bond = TuringBond(issueDate, maturityDate,
                      coupon, freqType, accrualType, face,
                      TuringYTMCalcType.US_STREET)

    ytm = bond.yieldToMaturity(settlementDate, cleanPrice)
    testCases.print("US STREET Yield To Maturity", ytm)

    bond = TuringBond(issueDate, maturityDate,
                      coupon, freqType, accrualType, face,
                      TuringYTMCalcType.US_TREASURY)

    ytm = bond.yieldToMaturity(settlementDate, cleanPrice)
    testCases.print("US TREASURY Yield To Maturity", ytm)

    fullPrice = bond.fullPriceFromYTM(settlementDate, ytm)
    testCases.print("Full Price", fullPrice)

    cleanPrice = bond.cleanPriceFromYTM(settlementDate, ytm)
    testCases.print("Clean Price", cleanPrice)

    accddays = bond._accruedDays
    testCases.print("Accrued Days", accddays)

    accd = bond._accruedInterest
    testCases.print("Accrued", accd)

    duration = bond.dollarDuration(settlementDate, ytm)
    testCases.print("Dollar Duration", duration)

    modifiedDuration = bond.modifiedDuration(settlementDate, ytm)
    testCases.print("Modified Duration", modifiedDuration)

    macauleyDuration = bond.macauleyDuration(settlementDate, ytm)
    testCases.print("Macauley Duration", macauleyDuration)

    conv = bond.convexityFromYTM(settlementDate, ytm)
    testCases.print("Convexity", conv)

###############################################################################


def test_FinBondExDividend():

    issueDate = TuringDate(2000, 9, 7)
    maturityDate = TuringDate(2020, 9, 7)
    coupon = 0.05
    freqType = TuringFrequencyTypes.SEMI_ANNUAL
    accrualType = TuringDayCountTypes.ACT_ACT_ICMA
    face = 100.0
    exDivDays = 7
    testCases.header("LABEL", "VALUE")

    calendarType = TuringCalendarTypes.UNITED_KINGDOM
    bond = TuringBond(issueDate, maturityDate, coupon,
                      freqType, accrualType, face)
    settlementDate = TuringDate(2003, 9, 7)
    accrued = bond.calcAccruedInterest(settlementDate, exDivDays, calendarType)
    testCases.print("SettlementDate:", settlementDate)
    testCases.print("Accrued:", accrued)

    ###########################################################################
    testCases.banner("=======================================================")
    testCases.header("SETTLEMENT", "ACCRUED")

    issueDate = TuringDate(2000, 9, 7)
    maturityDate = TuringDate(2020, 9, 7)
    coupon = 0.05
    freqType = TuringFrequencyTypes.SEMI_ANNUAL
    accrualType = TuringDayCountTypes.ACT_ACT_ICMA
    face = 100.0
    exDivDays = 7

    calendarType = TuringCalendarTypes.UNITED_KINGDOM
    bond = TuringBond(issueDate, maturityDate, coupon,
                      freqType, accrualType, face)

    settlementDate = TuringDate(2010, 8, 25)

    for _ in range(0, 13):
        settlementDate = settlementDate.addDays(1)
        accrued = bond.calcAccruedInterest(
            settlementDate, exDivDays, calendarType)
        testCases.print(settlementDate, accrued)

###############################################################################


test_FinBond()
test_FinBondExDividend()
testCases.compareTestCases()
