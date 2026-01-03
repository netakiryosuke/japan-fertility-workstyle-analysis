import type FixedEffectsResult from "../types/fixedEffectsResult";
import CoefficientTable from "./CoefficientTable";
import ModelSummary from "./ModelSummary";

interface Props {
    result: FixedEffectsResult | null;
}

export default function AnalysisResult({ result }: Props) {
    if (!result) return null;

    return (
        <div className="flex justify-center">
            <div className="
                w-full max-w-3xl
                bg-white
                border rounded-lg shadow
                p-6
                space-y-4
            ">
                <h2 className="text-lg font-semibold text-center">
                    Result
                </h2>

                <ModelSummary result={result} />
                <CoefficientTable result={result} />
            </div>
        </div>
    );
}
