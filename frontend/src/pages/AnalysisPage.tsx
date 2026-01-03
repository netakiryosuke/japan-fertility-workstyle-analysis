import { useAnalysis } from "../hooks/useAnalysis";
import AnalysisForm from "../components/AnalysisForm";
import AnalysisResult from "../components/AnalysisResult";
import { useEffect, useRef } from "react";

export default function AnalysisPage() {
    const analysis = useAnalysis();
    const resultRef = useRef<HTMLDivElement | null>(null)

    useEffect(() => {
        if (analysis.result && resultRef.current) {
            resultRef.current.scrollIntoView({
                behavior: "smooth",
                block: "center",
            })
        }
    }, [analysis.result])

    return (
        <div className="min-h-screen bg-gray-50 flex justify-center">
            <div className="w-full max-w-4xl px-4 py-10 space-y-6">
                <AnalysisForm
                    csvFile={analysis.csvFile}
                    setCsvFile={analysis.setCsvFile}
                    dependentVar={analysis.dependentVar}
                    setDependentVar={analysis.setDependentVar}
                    independentVars={analysis.independentVars}
                    setIndependentVars={analysis.setIndependentVars}
                    onAnalyze={analysis.handleAnalyze}
                    loading={analysis.loading}
                    error={analysis.error}
                />

                {analysis.result && (
                    <div ref={resultRef}>
                        <AnalysisResult result={analysis.result} />
                    </div>
                )}
            </div>
        </div>
    );
}
