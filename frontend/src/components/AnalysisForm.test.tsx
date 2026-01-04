import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import AnalysisForm from './AnalysisForm'
import type IndependentVar from '../types/independentVar'

describe('AnalysisForm', () => {
  const mockProps = {
    csvFile: null,
    setCsvFile: vi.fn(),
    dependentVar: 'TFR',
    setDependentVar: vi.fn(),
    independentVars: [
      { name: 'unmarried', selected: true },
      { name: 'employment_rate', selected: false },
    ] as IndependentVar[],
    setIndependentVars: vi.fn(),
    onAnalyze: vi.fn(),
    loading: false,
    error: null,
  }

  it('renders the form with all input fields', () => {
    render(<AnalysisForm {...mockProps} />)

    // Check for main heading
    expect(screen.getByText('Fixed Effects Analysis')).toBeInTheDocument()

    // Check for CSV file upload section
    expect(screen.getByText('CSVファイル')).toBeInTheDocument()
    expect(screen.getByText('ファイルを選択')).toBeInTheDocument()

    // Check for dependent variable input
    expect(screen.getByText('被説明変数（Dependent Variable）')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('例：TFR')).toBeInTheDocument()

    // Check for independent variables section
    expect(screen.getByText('説明変数（Independent Variables）')).toBeInTheDocument()

    // Check for analyze button
    expect(screen.getByRole('button', { name: /analyze/i })).toBeInTheDocument()
  })

  it('displays selected CSV file name', () => {
    const file = new File(['content'], 'test.csv', { type: 'text/csv' })
    render(<AnalysisForm {...mockProps} csvFile={file} />)

    expect(screen.getByText('選択中: test.csv')).toBeInTheDocument()
  })

  it('displays error message when error prop is provided', () => {
    const errorMessage = 'Please upload a CSV file.'
    render(<AnalysisForm {...mockProps} error={errorMessage} />)

    expect(screen.getByText(errorMessage)).toBeInTheDocument()
  })

  it('calls onAnalyze when analyze button is clicked', async () => {
    const user = userEvent.setup()
    render(<AnalysisForm {...mockProps} />)

    const analyzeButton = screen.getByRole('button', { name: /analyze/i })
    await user.click(analyzeButton)

    expect(mockProps.onAnalyze).toHaveBeenCalledTimes(1)
  })

  it('disables analyze button when loading', () => {
    render(<AnalysisForm {...mockProps} loading={true} />)

    const analyzeButton = screen.getByRole('button', { name: /analyzing/i })
    expect(analyzeButton).toBeDisabled()
  })

  it('calls setDependentVar when dependent variable input changes', async () => {
    const user = userEvent.setup()
    render(<AnalysisForm {...mockProps} />)

    const input = screen.getByPlaceholderText('例：TFR')
    await user.clear(input)
    await user.type(input, 'newVar')

    expect(mockProps.setDependentVar).toHaveBeenCalled()
  })

  it('renders independent variables with checkboxes', () => {
    render(<AnalysisForm {...mockProps} />)

    const checkboxes = screen.getAllByRole('checkbox')
    expect(checkboxes).toHaveLength(2)

    // Check that variable names are displayed
    expect(screen.getByDisplayValue('unmarried')).toBeInTheDocument()
    expect(screen.getByDisplayValue('employment_rate')).toBeInTheDocument()
  })

  it('shows add independent variable button', () => {
    render(<AnalysisForm {...mockProps} />)

    expect(screen.getByText('＋ 説明変数を追加')).toBeInTheDocument()
  })
})
