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
    csvFile,
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

                    <label className="inline-flex items-center gap-3 px-2 py-1 border rounded cursor-pointer hover:bg-gray-100 transition">
                        <span className="text-sm text-gray-700">
                            ファイルを選択
                        </span>
                        <input
                            type="file"
                            accept=".csv"
                            onChange={e => setCsvFile(e.target.files?.[0] ?? null)}
                            className="hidden"
                        />
                    </label>

                    <div className="text-xs text-gray-500">
                        {csvFile ? `選択中: ${csvFile.name}` : "ファイルは選択されていません"}
                    </div>
                </div>

                <div className="space-y-1">
                    <label className="block text-sm font-medium">
                        被説明変数（Dependent Variable）
                    </label>
                    <input
                        type="text"
                        value={dependentVar}
                        onChange={e => setDependentVar(e.target.value)}
                        placeholder="例：TFR"
                        className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <div className="space-y-2">
                    <label className="block text-sm font-medium">
                        説明変数（Independent Variables）
                    </label>

                    <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
                        {independentVars.map((value, index) => (
                            <div
                                key={index}
                                className="flex items-center gap-2 rounded px-2 py-1 hover:bg-gray-50"
                            >
                                <input
                                    type="checkbox"
                                    checked={value.selected}
                                    className="cursor-pointer"
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
                                    placeholder="例：unmarried"
                                    className="flex-1 border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                            </div>
                        ))}
                    </div>

                    <button
                        onClick={() =>
                            setIndependentVars(prev => [
                                ...prev,
                                { name: "", selected: true },
                            ])
                        }
                        className="text-sm text-blue-600 hover:text-blue-800 transition cursor-pointer"
                    >
                        ＋ 説明変数を追加
                    </button>
                </div>

                <button
                    onClick={onAnalyze}
                    disabled={loading}
                    className="w-full py-2 bg-blue-600 text-white rounded font-medium
                    hover:bg-blue-700 transition cursor-pointer
                    disabled:opacity-60 disabled:cursor-not-allowed"
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

