import type { FixedEffectsResult } from "../types/fixedEffectsResult";
import CoefficientTable from "./CoefficientTable";
import ModelSummary from "./ModelSummary";

interface Props {
    result: FixedEffectsResult | null;
}

export default function AnalysisResult({ result }: Props) {
    if (!result) return null;

    return (
        <div className="mt-6 space-y-4">
            <h2 className="text-lg font-semibold">
                Fixed Effects Regression Result
            </h2>

            <CoefficientTable result={result} />
            <ModelSummary result={result} />
        </div>
    );
}
