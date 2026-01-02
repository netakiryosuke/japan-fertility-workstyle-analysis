import type { FixedEffectsResult } from '../types/fixedEffectsResult'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

type AnalyzeParams = {
  csvFile: File
  dependentVar: string
  independentVars: string[]
}

type ProblemDetails = {
  type?: string
  title?: string
  status?: number
  detail?: string
  instance?: string
}

export default async function analyzeFertility({ csvFile, dependentVar, independentVars }: AnalyzeParams): Promise<FixedEffectsResult> {
  const formData = new FormData()
  formData.append('csv_file', csvFile)
  formData.append('dependent_var', dependentVar)
  independentVars.forEach((variable) => {
    formData.append('independent_vars', variable)
  })

  const response = await fetch(`${API_BASE_URL}/analysis`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const problemDetails = await response.json() as ProblemDetails
    throw new Error(problemDetails.detail || `Request failed with status ${response.status}`)
  }

  return response.json()
}
