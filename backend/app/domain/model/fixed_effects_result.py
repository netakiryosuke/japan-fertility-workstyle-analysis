from dataclasses import dataclass

@dataclass(frozen=True)
class FixedEffectsResult:
    nobs: int
    params: dict[str, float]
    std_errors: dict[str, float]
    tstats: dict[str, float]
    pvalues: dict[str, float]
    rsquared_within: float
    rsquared_between: float
    rsquared_overall: float
    dropped_vars: list[str]
