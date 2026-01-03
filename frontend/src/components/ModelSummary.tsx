import type FixedEffectsResult from "../types/fixedEffectsResult"
import formatNumber from "../utils/formatNumber"

interface Props {
    result: FixedEffectsResult
}

export default function ModelSummary({ result }: Props) {
    return (
        <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
            <div>
                <div>R² (within) = {formatNumber(result.rsquared_within)}</div>
                <div>R² (between) = {formatNumber(result.rsquared_between)}</div>
                <div>R² (overall) = {formatNumber(result.rsquared_overall)}</div>
            </div>
            <div>
                <div>Number of observations = {result.nobs}</div>
            </div>
        </div>
    )
}
