import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import AnalysisResult from '../../src/components/AnalysisResult'
import type FixedEffectsResult from '../../src/types/fixedEffectsResult'

describe('AnalysisResult', () => {
  const mockResult: FixedEffectsResult = {
    nobs: 100,
    params: {
      unmarried: 0.5,
      employment_rate: -0.3,
    },
    std_errors: {
      unmarried: 0.1,
      employment_rate: 0.05,
    },
    tstats: {
      unmarried: 5.0,
      employment_rate: -6.0,
    },
    pvalues: {
      unmarried: 0.001,
      employment_rate: 0.0001,
    },
    rsquared_within: 0.75,
    rsquared_between: 0.65,
    rsquared_overall: 0.70,
    dropped_vars: [],
  }

  it('renders nothing when result is null', () => {
    // Given & When
    const { container } = render(<AnalysisResult result={null} />)

    // Then
    expect(container.firstChild).toBeNull()
  })

  it('renders result section when result is provided', () => {
    // Given & When
    render(<AnalysisResult result={mockResult} />)

    // Then
    expect(screen.getByText('Result')).toBeInTheDocument()
  })

  it('displays model summary statistics', () => {
    // Given & When
    render(<AnalysisResult result={mockResult} />)

    // Then
    expect(screen.getByText(/R² \(within\) = 0\.75/)).toBeInTheDocument()
    expect(screen.getByText(/R² \(between\) = 0\.65/)).toBeInTheDocument()
    expect(screen.getByText(/R² \(overall\) = 0\.70/)).toBeInTheDocument()
    expect(screen.getByText(/Number of observations = 100/)).toBeInTheDocument()
  })

  it('displays coefficient table with variable names', () => {
    // Given & When
    render(<AnalysisResult result={mockResult} />)

    // Then
    expect(screen.getByText('unmarried')).toBeInTheDocument()
    expect(screen.getByText('employment_rate')).toBeInTheDocument()
  })

  it('displays coefficient table headers', () => {
    // Given & When
    render(<AnalysisResult result={mockResult} />)

    // Then
    expect(screen.getByText('Variable')).toBeInTheDocument()
    expect(screen.getByText('Coef.')).toBeInTheDocument()
    expect(screen.getByText('Std. Err.')).toBeInTheDocument()
    expect(screen.getByText('t')).toBeInTheDocument()
    expect(screen.getByText('P>|t|')).toBeInTheDocument()
  })

  it('displays dropped variables warning when present', () => {
    // Given
    const resultWithDropped: FixedEffectsResult = {
      ...mockResult,
      dropped_vars: ['w_time', 'd_tokyo'],
    }

    // When
    render(<AnalysisResult result={resultWithDropped} />)

    // Then
    expect(screen.getByText('推定から除外された説明変数')).toBeInTheDocument()
    expect(screen.getByText('w_time')).toBeInTheDocument()
    expect(screen.getByText('d_tokyo')).toBeInTheDocument()
    expect(screen.getByText('※ 固定効果や完全共線性により推定できませんでした')).toBeInTheDocument()
  })

  it('does not display dropped variables warning when none present', () => {
    // Given & When
    render(<AnalysisResult result={mockResult} />)

    // Then
    expect(screen.queryByText('推定から除外された説明変数')).not.toBeInTheDocument()
  })
})
