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
        <div className="min-h-screen flex justify-center items-start pt-16 bg-gray-50">
            <div className="w-full max-w-xl bg-white rounded-xl shadow p-6 space-y-6">
                <h1 className="text-xl font-semibold text-center">
                    Fixed Effects Analysis
                </h1>

                <div className="space-y-1">
                    <label className="block text-sm font-medium">
                        CSVファイル
                    </label>
                    <input
                        type="file"
                        accept=".csv"
                        onChange={e => setCsvFile(e.target.files?.[0] ?? null)}
                        className="block w-full text-sm"
                    />
                </div>

                <div className="space-y-1">
                    <label className="block text-sm font-medium">
                        被説明変数（Dependent Variable）
                    </label>
                    <input
                        type="text"
                        value={dependentVar}
                        onChange={e => setDependentVar(e.target.value)}
                        placeholder="例：fertility_rate"
                        className="w-full border rounded px-3 py-2 text-sm"
                    />
                </div>

                <div className="space-y-2">
                    <label className="block text-sm font-medium">
                        説明変数（Independent Variables）
                    </label>

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
                                placeholder="例：female_employment_rate"
                                className="flex-1 border rounded px-3 py-2 text-sm"
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
                        className="text-sm text-blue-600 hover:underline"
                    >
                        ＋ 説明変数を追加
                    </button>
                </div>

                <button
                    onClick={onAnalyze}
                    disabled={loading}
                    className="w-full py-2 bg-blue-600 text-white rounded font-medium disabled:opacity-60"
                >
                    {loading ? "Analyzing..." : "Analyze"}
                </button>

                {error && (
                    <div className="text-sm text-red-600 text-center">
                        {error}
                    </div>
                )}
            </div>
        </div>
    );
}

