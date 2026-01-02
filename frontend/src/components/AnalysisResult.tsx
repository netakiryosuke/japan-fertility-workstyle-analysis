import type { FixedEffectsResult } from "../types/fixedEffectsResult";

interface Props {
    result: FixedEffectsResult | null;
}

export default function AnalysisResult({ result }: Props) {
    if (!result) return null;

    return (
        <pre className="bg-gray-100 p-4 text-xs">
            {JSON.stringify(result, null, 2)}
        </pre>
    );
}
