import type { FixedEffectsResult } from "../types/fixedEffectsResult"

interface Props {
    result: FixedEffectsResult
}

export default function ModelSummary({ result }: Props) {
    return (
        <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
            <div>
                <div>N = {result.nobs}</div>
                <div>R² (within) = {result.rsquared_within}</div>
            </div>
            <div>
                <div>R² (between) = {result.rsquared_between}</div>
                <div>R² (overall) = {result.rsquared_overall}</div>
            </div>
        </div>
    )
}
