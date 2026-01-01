export type FixedEffectsResult = {
  nobs: number
  params: Record<string, number>
  std_errors: Record<string, number>
  tstats: Record<string, number>
  pvalues: Record<string, number>
  rsquared_within: number
  rsquared_between: number
  rsquared_overall: number
}
