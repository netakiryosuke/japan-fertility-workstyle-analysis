import { useAnalysis } from "../hooks/useAnalysis";
import AnalysisForm from "../components/AnalysisForm";
import AnalysisResult from "../components/AnalysisResult";

export default function AnalysisPage() {
    const analysis = useAnalysis();

    return (
        <>
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
            <AnalysisResult result={analysis.result} />
        </>
    );
}
