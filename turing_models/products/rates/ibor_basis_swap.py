from turing_models.utilities.error import TuringError
from turing_models.utilities.turing_date import TuringDate
from turing_models.utilities.day_count import TuringDayCountTypes
from turing_models.utilities.frequency import TuringFrequencyTypes
from turing_models.utilities.calendar import TuringCalendarTypes, TuringDateGenRuleTypes
from turing_models.utilities.calendar import TuringCalendar, TuringBusDayAdjustTypes
from turing_models.utilities.helper_functions import checkArgumentTypes, labelToString
from turing_models.utilities.mathematics import ONE_MILLION
from turing_models.utilities.global_types import TuringSwapTypes
from turing_models.market.curves.discount_curve import TuringDiscountCurve

from .float_leg import TuringFloatLeg

###############################################################################


class TuringIborBasisSwap(object):
    ''' Class for managing an Ibor-Ibor basis swap contract. This is a
    contract in which a floating leg with one LIBOR tenor is exchanged for a 
    floating leg payment in a different LIBOR tenor. There is no exchange of
    par. The contract is entered into at zero initial cost. The contract lasts
    from an effective date to a specified maturity date.
    
    The value of the contract is the NPV of the two coupon streams. Discounting
    is done on a supplied discount curve which can be different from the two 
    index curves from which the implied index rates are extracted. '''
    
    def __init__(self,
                 effectiveDate: TuringDate,  # Date interest starts to accrue
                 terminationDateOrTenor: (TuringDate, str),  # Date contract ends
                 leg1Type: TuringSwapTypes,
                 leg1FreqType: TuringFrequencyTypes = TuringFrequencyTypes.QUARTERLY,
                 leg1DayCountType: TuringDayCountTypes  = TuringDayCountTypes.THIRTY_E_360,
                 leg1Spread: float = 0.0,
                 leg2FreqType: TuringFrequencyTypes = TuringFrequencyTypes.QUARTERLY,
                 leg2DayCountType: TuringDayCountTypes = TuringDayCountTypes.THIRTY_E_360,
                 leg2Spread: float = 0.0,
                 notional: float = ONE_MILLION,
                 calendarType: TuringCalendarTypes = TuringCalendarTypes.WEEKEND,
                 busDayAdjustType: TuringBusDayAdjustTypes = TuringBusDayAdjustTypes.FOLLOWING,
                 dateGenRuleType: TuringDateGenRuleTypes = TuringDateGenRuleTypes.BACKWARD):
        ''' Create a Ibor basis swap contract giving the contract start
        date, its maturity, frequency and day counts on the two floating 
        legs and notional. The floating leg parameters have default
        values that can be overwritten if needed. The start date is contractual
        and is the same as the settlement date for a new swap. It is the date
        on which interest starts to accrue. The end of the contract is the
        termination date. This is not adjusted for business days. The adjusted
        termination date is called the maturity date. This is calculated. '''

        checkArgumentTypes(self.__init__, locals())

        if type(terminationDateOrTenor) == TuringDate:
            self._terminationDate = terminationDateOrTenor
        else:
            self._terminationDate = effectiveDate.addTenor(terminationDateOrTenor)

        calendar = TuringCalendar(calendarType)
        self._maturityDate = calendar.adjust(self._terminationDate,
                                             busDayAdjustType)

        if effectiveDate > self._maturityDate:
            raise TuringError("Start date after maturity date")

        leg2Type = TuringSwapTypes.PAY
        if leg1Type == TuringSwapTypes.PAY:
            leg2Type = TuringSwapTypes.RECEIVE
        
        paymentLag = 0
        principal = 0.0

        self._floatLeg1 = TuringFloatLeg(effectiveDate,
                                         self._terminationDate,
                                         leg1Type,
                                         leg1Spread,
                                         leg1FreqType,
                                         leg1DayCountType,
                                         notional,
                                         principal,
                                         paymentLag,
                                         calendarType,
                                         busDayAdjustType,
                                         dateGenRuleType)

        self._floatLeg2 = TuringFloatLeg(effectiveDate,
                                         self._terminationDate,
                                         leg2Type,
                                         leg2Spread,
                                         leg2FreqType,
                                         leg2DayCountType,
                                         notional,
                                         principal,
                                         paymentLag,
                                         calendarType,
                                         busDayAdjustType,
                                         dateGenRuleType)

###############################################################################

    def value(self,
              valuationDate: TuringDate,
              discountCurve: TuringDiscountCurve,
              indexCurveLeg1: TuringDiscountCurve = None,
              indexCurveLeg2: TuringDiscountCurve = None,
              firstFixingRateLeg1=None,
              firstFixingRateLeg2=None):
        ''' Value the interest rate swap on a value date given a single Ibor
        discount curve and an index curve for the Ibors on each swap leg. '''

        if indexCurveLeg1 is None:
            indexCurveLeg1 = discountCurve

        if indexCurveLeg2 is None:
            indexCurveLeg2 = discountCurve

        floatLeg1Value = self._floatLeg1.value(valuationDate,
                                               discountCurve, 
                                               indexCurveLeg1, 
                                               firstFixingRateLeg1)

        floatLeg2Value = self._floatLeg2.value(valuationDate,
                                               discountCurve,
                                               indexCurveLeg2,
                                               firstFixingRateLeg2)

        value = floatLeg1Value + floatLeg2Value
        return value

###############################################################################

    def printFloatLeg1PV(self):
        ''' Prints the fixed leg amounts without any valuation details. Shows
        the dates and sizes of the promised fixed leg flows. '''

        self._floatLeg1.printValuation()

###############################################################################

    def printFloatLeg2PV(self):
        ''' Prints the fixed leg amounts without any valuation details. Shows
        the dates and sizes of the promised fixed leg flows. '''

        self._floatLeg2.printValuation()

###############################################################################

    def printFlows(self):
        ''' Prints the fixed leg amounts without any valuation details. Shows
        the dates and sizes of the promised fixed leg flows. '''

        self._floatLeg1.printPayments()
        self._floatLeg2.printPayments()

##########################################################################

    def __repr__(self):
        s = labelToString("OBJECT TYPE", type(self).__name__)
        s += self._floatLeg1.__repr__()
        s += "\n"
        s += self._floatLeg2.__repr__()
        return s

###############################################################################

    def _print(self):
        ''' Print a list of the unadjusted coupon payment dates used in
        analytic calculations for the bond. '''
        print(self)

###############################################################################
