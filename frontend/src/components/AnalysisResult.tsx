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
                {result.dropped_vars.length > 0 && (
                    <div className="mt-4 rounded border border-yellow-300 bg-yellow-50 p-3 text-sm">
                        <p className="font-medium text-yellow-800">
                            推定から除外された説明変数
                        </p>
                        <ul className="mt-1 list-disc list-inside text-yellow-700">
                            {result.dropped_vars.map(v => (
                                <li key={v}>{v}</li>
                            ))}
                        </ul>
                        <p className="mt-1 text-xs text-yellow-700">
                            ※ 固定効果や完全共線性により推定できませんでした
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
