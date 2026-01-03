import { useState } from "react";
import analyzeFertility from "../api/analysis";
import type { FixedEffectsResult } from "../types/fixedEffectsResult";
import type IndependentVar from "../types/independentVar";

export function useAnalysis() {
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [dependentVar, setDependentVar] = useState<string>("TFR");
  const [independentVars, setIndependentVars] = useState<IndependentVar[]>([
    { name: "unmarried", selected: true },
    { name: "employment_rate", selected: true },
    { name: "w_time", selected: true },
    { name: "w_overtime", selected: true },
    { name: "wage_hour", selected: true },
    { name: "telework_com", selected: true },
    { name: "d_tokyo", selected: true },
    { name: "d_okinawa", selected: true },
    { name: "d_covid", selected: true },
  ]);
  const [result, setResult] = useState<FixedEffectsResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!csvFile) {
      setError("Please upload a CSV file.");
      return;
    }

    const selectedIndependentVars = independentVars
      .filter((independentVar) => independentVar.selected)
      .map((independentVar) => independentVar.name.trim());

    if (selectedIndependentVars.length === 0) {
      setError("Please select at least one independent variable.");
      return;
    }

    if (selectedIndependentVars.some((name) => name === "")) {
      setError("Selected independent variables must not be empty.");
      return;
    }

    try {
      setLoading(true);
      setResult(null);
      setError("");

      const response = await analyzeFertility({
        csvFile,
        dependentVar,
        independentVars: selectedIndependentVars,
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
