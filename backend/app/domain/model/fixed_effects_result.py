from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class FixedEffectsResult:
    nobs: int
    params: Dict[str, float]
    std_errors: Dict[str, float]
    tstats: Dict[str, float]
    pvalues: Dict[str, float]
    rsquared_within: float
    rsquared_between: float
    rsquared_overall: float
