import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import AnalysisForm from '../../src/components/AnalysisForm'
import type IndependentVar from '../../src/types/independentVar'

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
    // Given & When
    render(<AnalysisForm {...mockProps} />)

    // Then
    expect(screen.getByText('Fixed Effects Analysis')).toBeInTheDocument()
    expect(screen.getByText('CSVファイル')).toBeInTheDocument()
    expect(screen.getByText('ファイルを選択')).toBeInTheDocument()
    expect(screen.getByText('被説明変数（Dependent Variable）')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('例：TFR')).toBeInTheDocument()
    expect(screen.getByText('説明変数（Independent Variables）')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /analyze/i })).toBeInTheDocument()
  })

  it('displays selected CSV file name', () => {
    // Given
    const file = new File(['content'], 'test.csv', { type: 'text/csv' })

    // When
    render(<AnalysisForm {...mockProps} csvFile={file} />)

    // Then
    expect(screen.getByText('選択中: test.csv')).toBeInTheDocument()
  })

  it('displays error message when error prop is provided', () => {
    // Given
    const errorMessage = 'Please upload a CSV file.'

    // When
    render(<AnalysisForm {...mockProps} error={errorMessage} />)

    // Then
    expect(screen.getByText(errorMessage)).toBeInTheDocument()
  })

  it('calls onAnalyze when analyze button is clicked', async () => {
    // Given
    const user = userEvent.setup()
    render(<AnalysisForm {...mockProps} />)

    // When
    const analyzeButton = screen.getByRole('button', { name: /analyze/i })
    await user.click(analyzeButton)

    // Then
    expect(mockProps.onAnalyze).toHaveBeenCalledTimes(1)
  })

  it('disables analyze button when loading', () => {
    // Given & When
    render(<AnalysisForm {...mockProps} loading={true} />)

    // Then
    const analyzeButton = screen.getByRole('button', { name: /analyzing/i })
    expect(analyzeButton).toBeDisabled()
  })

  it('calls setDependentVar when dependent variable input changes', async () => {
    // Given
    const user = userEvent.setup()
    render(<AnalysisForm {...mockProps} />)

    // When
    const input = screen.getByPlaceholderText('例：TFR')
    await user.clear(input)
    await user.type(input, 'newVar')

    // Then
    expect(mockProps.setDependentVar).toHaveBeenCalled()
  })

  it('renders independent variables with checkboxes', () => {
    // Given & When
    render(<AnalysisForm {...mockProps} />)

    // Then
    const checkboxes = screen.getAllByRole('checkbox')
    expect(checkboxes).toHaveLength(2)
    expect(screen.getByDisplayValue('unmarried')).toBeInTheDocument()
    expect(screen.getByDisplayValue('employment_rate')).toBeInTheDocument()
  })

  it('shows add independent variable button', () => {
    // Given & When
    render(<AnalysisForm {...mockProps} />)

    // Then
    expect(screen.getByText('＋ 説明変数を追加')).toBeInTheDocument()
  })
})
