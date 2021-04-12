##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

import numpy as np
from numba import jit, njit, float64, int64
from ..finutils.turing_math import cholesky

###############################################################################

class FinModel():
    
    def __init__(implementationType,
                 parameterDict: dict):
 
        self._implementationType = implementationType
        self._parameterDist = parameterDict

###############################################################################
