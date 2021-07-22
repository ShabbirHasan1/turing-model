import datetime
import traceback
from dataclasses import dataclass

from fundamental.turing_db.base.core import InstrumentBase
from fundamental.turing_db.data import Turing
from fundamental.turing_db.utils import to_snake
from turing_models.instruments.core import Instrument
from turing_models.utilities.calendar import TuringCalendarTypes, TuringBusDayAdjustTypes, \
    TuringDateGenRuleTypes
from turing_models.utilities.day_count import TuringDayCountTypes
from turing_models.utilities.frequency import TuringFrequency, TuringFrequencyTypes
from turing_models.utilities.global_types import TuringYTMCalcType
from turing_models.utilities.schedule import TuringSchedule
from turing_models.utilities.turing_date import TuringDate
from turing_models.utilities.helper_functions import label_to_string

dy = 0.0001


@dataclass(repr=False, eq=False, order=False, unsafe_hash=True)
class Bond(Instrument, InstrumentBase):
    asset_id: str = None
    bond_type: str = None
    interest_accrued: float = None
    issue_date: TuringDate = None
    due_date: TuringDate = None
    bond_term_year: float = None
    bond_term_day: float = None
    freq_type: str = None
    accrual_type: str = None
    par: float = None
    clean_price: float = None
    name: str = None
    settlement_date: TuringDate = TuringDate(*(datetime.date.today().timetuple()[:3]))

    def __post_init__(self):
        super().__init__()
        self.convention = TuringYTMCalcType.UK_DMO
        self.calendar_type = TuringCalendarTypes.WEEKEND
        self._redemption = 1.0  # This is amount paid at maturity
        self._flow_dates = []
        self._flow_amounts = []
        self._accrued_interest = None
        self._accrued_days = 0.0
        self.set_param()

    def set_param(self):
        self._settlement_date = self.settlement_date
        if self.freq_type:
            self._calculate_flow_dates()
        if self.freq_type:
            self.frequency = TuringFrequency(self.freq_type_)

    @property
    def freq_type_(self):
        if self.freq_type == '每年付息':
            return TuringFrequencyTypes.ANNUAL
        elif self.freq_type == '半年付息':
            return TuringFrequencyTypes.SEMI_ANNUAL
        elif self.freq_type == '4个月一次':
            return TuringFrequencyTypes.TRI_ANNUAL
        elif self.freq_type == '按季付息':
            return TuringFrequencyTypes.QUARTERLY
        elif self.freq_type == '按月付息':
            return TuringFrequencyTypes.MONTHLY
        else:
            raise Exception('Please check the input of freq_type')

    @property
    def accrual_type_(self):
        if self.accrual_type == 'ACT/365':
            return TuringDayCountTypes.ACT_365L
        elif self.accrual_type == 'ACT/ACT':
            return TuringDayCountTypes.ACT_ACT_ISDA
        elif self.accrual_type == 'ACT/360':
            return TuringDayCountTypes.ACT_360
        elif self.accrual_type == '30/360':
            return TuringDayCountTypes.THIRTY_E_360
        elif self.accrual_type == 'ACT/365F':
            return TuringDayCountTypes.ACT_365F
        else:
            raise Exception('Please check the input of accrual_type')

    @property
    def settlement_date_(self):
        return self.ctx.pricing_date or self._settlement_date

    def _calculate_flow_dates(self):
        """ Determine the bond cashflow payment dates."""

        calendar_type = TuringCalendarTypes.NONE
        bus_day_rule_type = TuringBusDayAdjustTypes.NONE
        date_gen_rule_type = TuringDateGenRuleTypes.BACKWARD
        self._flow_dates = TuringSchedule(self.issue_date,
                                          self.due_date,
                                          self.freq_type_,
                                          calendar_type,
                                          bus_day_rule_type,
                                          date_gen_rule_type)._generate()

    def dv01(self):
        print("You should not be here!")
        return 0.0

    def dollar_duration(self):
        return self.dv01() / dy

    def dollar_convexity(self):
        print("You should not be here!")
        return 0.0

    def fetch_yield_curve(self, curve_code_list):
        """根据asset_ids的集合为参数,取行情"""
        try:
            return Turing.get_yieldcurve(_ids=curve_code_list)
        except Exception:
            traceback.print_exc()
            return None

    def fetch_quotes(self, ids):
        """根据asset_ids的集合为参数,取行情"""
        try:
            res = Turing.get_bond_markets(_ids=ids)
            return res
        except Exception as e:
            traceback.print_exc()
            return None

    def put_zero_dates(self, curve_code_list):
        zero_dates = []
        curve = self.fetch_yield_curve(curve_code_list)
        if curve:
            for code in to_snake(curve):
                if code.get("curve_code") == curve_code_list[0]:
                    for cu in code.get('curve_data'):
                        zero_dates.append(cu.get('term'))
        self.zero_dates = zero_dates
        return zero_dates

    def put_zero_rates(self, curve_code_list):
        zero_rates = []
        curve = self.fetch_yield_curve(curve_code_list)
        if curve:
            for code in to_snake(curve):
                if code.get("curve_code") == curve_code_list[0]:
                    for cu in code.get('curve_data'):
                        zero_rates.append(cu.get('spot_rate'))
        self.zero_rates = zero_rates
        return zero_rates

    def put_ytm(self, quotes_dict, asset_id):
        if quotes_dict:
            for quote in quotes_dict:
                if quote.get("asset_id") == asset_id:
                    ytm_ = quote.get("ytm", None)
                    if ytm_:
                        return ytm_
        return None

    def __repr__(self):
        s = label_to_string("Object Type", type(self).__name__)
        s += label_to_string("Asset Id", self.asset_id)
        s += label_to_string("Interest Accrued", self.interest_accrued)
        s += label_to_string("Issue Date", self.issue_date)
        s += label_to_string("Due Date", self.due_date)
        s += label_to_string("Freq Type", self.freq_type)
        s += label_to_string("Accrual Type", self.accrual_type)
        s += label_to_string("Par", self.par)
        s += label_to_string("Clean Price", self.clean_price)
        s += label_to_string("Settlement Date", self.settlement_date_)
        return s
