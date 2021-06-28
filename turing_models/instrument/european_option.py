from dataclasses import dataclass

from turing_models.utilities.global_types import TuringOptionTypes
from turing_models.models.model_black_scholes_analytical import bsValue, bsDelta, \
     bsVega, bsGamma, bsRho, bsPsi, bsTheta
from turing_models.instrument.equity_option import EqOption


@dataclass
class EuropeanOption(EqOption):

    def __post_init__(self):
        super().__post_init__()

    @property
    def option_type_(self) -> TuringOptionTypes:
        return TuringOptionTypes.EUROPEAN_CALL if self.option_type == 'CALL' \
            else TuringOptionTypes.EUROPEAN_PUT

    def params(self) -> list:
        return [
            self.stock_price_,
            self.texp,
            self.strike_price,
            self.r,
            self.q,
            self.v,
            self.option_type_.value
        ]

    def price(self) -> float:
        return bsValue(*self.params()) * self.multiplier * self.number_of_options

    def eq_delta(self) -> float:
        return bsDelta(*self.params()) * self.multiplier * self.number_of_options

    def eq_gamma(self) -> float:
        return bsGamma(*self.params()) * self.multiplier * self.number_of_options

    def eq_vega(self) -> float:
        return bsVega(*self.params()) * self.multiplier * self.number_of_options

    def eq_theta(self) -> float:
        return bsTheta(*self.params()) * self.multiplier * self.number_of_options

    def eq_rho(self) -> float:
        return bsRho(*self.params()) * self.multiplier * self.number_of_options

    def eq_rho_q(self) -> float:
        return bsPsi(*self.params()) * self.multiplier * self.number_of_options
