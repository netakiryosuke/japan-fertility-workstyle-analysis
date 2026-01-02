import { useState } from "react";
import analyzeFertility from "../api/analysis";
import type { FixedEffectsResult } from "../types/fixedEffectsResult";

interface IndependentVar {
  name: string;
  selected: boolean;
}

export function useAnalysis() {
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [dependentVar, setDependentVar] = useState<string>("");
  const [independentVars, setIndependentVars] = useState<IndependentVar[]>([
    { name: "", selected: false },
  ]);
  const [result, setResult] = useState<FixedEffectsResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!csvFile) return;

    try {
      setLoading(true);

      const response = await analyzeFertility({
        csvFile,
        dependentVar,
        independentVars: independentVars
          .filter((v) => v.selected)
          .map((v) => v.name),
      });

      setResult(response);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return {
    csvFile,
    setCsvFile,
    dependentVar,
    setDependentVar,
    independentVars,
    setIndependentVars,
    result,
    loading,
    error,
    handleAnalyze,
  };
}
