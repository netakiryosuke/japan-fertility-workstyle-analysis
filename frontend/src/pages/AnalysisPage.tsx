import { useState } from "react";
import type { FixedEffectsResult } from "../types/fixedEffectsResult";
import analyzeFertility from "../api/analysis";

type IndependentVar = {
    name: string
    selected: boolean
};

export default function AnalysisPage() {
    const [csvFile, setCsvFile] = useState<File | null>(null);
    const [dependentVar, setDependentVar] = useState<string>("");
    const [independentVars, setIndependentVars] = useState<IndependentVar[]>([
        { name: "", selected: false },
    ])
    const [result, setResult] = useState<FixedEffectsResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);


    const handleAnalyze = async () => {
        if (!csvFile) return;

        try {
            setLoading(true);

            const response = await analyzeFertility({
                csvFile,
                dependentVar: dependentVar,
                independentVars: independentVars
                    .filter(v => v.selected)
                    .map(v => v.name),
            });

            setResult(response);
        } catch (e) {
            // TODO: improve error handling
            setError((e as Error).message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="p-6 space-y-4">
            <input
                type="file"
                accept=".csv"
                onChange={e => setCsvFile(e.target.files?.[0] ?? null)}
            />
            <input
                type="text"
                value={dependentVar}
                onChange={e => setDependentVar(e.target.value)}
                className="border px-2 py-1"
            />
            {independentVars.map((value, index) => (
                <div key={index} className="flex items-center gap-2">
                    <input
                        type="checkbox"
                        checked={value.selected}
                        onChange={() =>
                            setIndependentVars(prev =>
                                prev.map((independentVar, i) =>
                                    i === index
                                        ? { ...independentVar, selected: !independentVar.selected }
                                        : independentVar
                                )
                            )
                        }
                    />
                    <input
                        type="text"
                        value={value.name}
                        onChange={e =>
                            setIndependentVars(prev =>
                                prev.map((independentVar, i) =>
                                    i === index
                                        ? { ...independentVar, name: e.target.value }
                                        : independentVar
                                )
                            )
                        }
                        className="border px-2 py-1"
                    />
                </div>
            ))}
            <button
                onClick={() =>
                    setIndependentVars(prev => [
                        ...prev,
                        { name: "", selected: false },
                    ])
                }
                className="px-2 py-1 border rounded"
            >
                ＋
            </button>
            <button
                onClick={handleAnalyze}
                className="px-4 py-2 bg-blue-600 text-white rounded"
            >
                Analyze
            </button>
            {result && (
                <pre className="bg-gray-100 p-4 text-xs">
                    {JSON.stringify(result, null, 2)}
                </pre>
            )}
        </div>
    )
}