interface IndependentVar {
    name: string;
    selected: boolean;
}

interface Props {
    csvFile: File | null;
    setCsvFile: (file: File | null) => void;
    dependentVar: string;
    setDependentVar: (value: string) => void;
    independentVars: IndependentVar[];
    setIndependentVars: React.Dispatch<React.SetStateAction<IndependentVar[]>>;
    onAnalyze: () => void;
    loading: boolean;
    error: string | null;
}

export default function AnalysisForm({
    setCsvFile,
    dependentVar,
    setDependentVar,
    independentVars,
    setIndependentVars,
    onAnalyze,
    loading,
    error,
}: Props) {
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
                onClick={onAnalyze}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded"
            >
                {loading ? "Analyzing..." : "Analyze"}
            </button>

            {error && <div className="text-red-600">{error}</div>}
        </div>
    );
}
