import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import AnalysisPage from '../../src/pages/AnalysisPage'
import type FixedEffectsResult from '../../src/types/fixedEffectsResult'

// Mock fetch
global.fetch = vi.fn()

describe('AnalysisPage - Integration Test', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders form and displays validation error when no CSV file is selected', async () => {
    // Given
    const user = userEvent.setup()
    render(<AnalysisPage />)

    // When
    const analyzeButton = screen.getByRole('button', { name: /analyze/i })
    await user.click(analyzeButton)

    // Then
    expect(screen.getByText('Fixed Effects Analysis')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /analyze/i })).toBeInTheDocument()
    await waitFor(() => {
      expect(screen.getByText('Please upload a CSV file.')).toBeInTheDocument()
    })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('displays validation error when no independent variables are selected', async () => {
    // Given
    const user = userEvent.setup()
    render(<AnalysisPage />)

    const file = new File(['content'], 'test.csv', { type: 'text/csv' })
    const fileInput = document.querySelector('input[type="file"][accept=".csv"]') as HTMLInputElement
    if (fileInput) {
      await user.upload(fileInput, file)
    }

    await waitFor(() => {
      expect(screen.getByText(/選択中: test.csv/)).toBeInTheDocument()
    })

    const checkboxes = screen.getAllByRole('checkbox')
    for (const checkbox of checkboxes) {
      if ((checkbox as HTMLInputElement).checked) {
        await user.click(checkbox)
      }
    }

    // When
    const analyzeButton = screen.getByRole('button', { name: /analyze/i })
    await user.click(analyzeButton)

    // Then
    await waitFor(() => {
      expect(screen.getByText('Please select at least one independent variable.')).toBeInTheDocument()
    })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('calls API and displays results when valid data is submitted', async () => {
    // Given
    const user = userEvent.setup()

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

    const mockFetch = vi.mocked(fetch)
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResult,
    } as Response)

    render(<AnalysisPage />)

    const file = new File(['content'], 'test.csv', { type: 'text/csv' })
    const fileInput = document.querySelector('input[type="file"][accept=".csv"]') as HTMLInputElement
    if (fileInput) {
      await user.upload(fileInput, file)
    }

    await waitFor(() => {
      expect(screen.getByText(/選択中: test.csv/)).toBeInTheDocument()
    })

    // When
    const analyzeButton = screen.getByRole('button', { name: /analyze/i })
    await user.click(analyzeButton)

    // Then
    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledTimes(1)
    })
    
    const callArgs = mockFetch.mock.calls[0]
    expect(callArgs[0]).toContain('/analysis')
    expect(callArgs[1]?.method).toBe('POST')

    await waitFor(() => {
      expect(screen.getByText('Result')).toBeInTheDocument()
    })

    expect(screen.getByText(/R² \(within\) = 0\.75/)).toBeInTheDocument()
    expect(screen.getByText(/Number of observations = 100/)).toBeInTheDocument()
    expect(screen.getByText('unmarried')).toBeInTheDocument()
    expect(screen.getByText('employment_rate')).toBeInTheDocument()
  })

  it('displays error message when API call fails', async () => {
    // Given
    const user = userEvent.setup()

    const mockFetch = vi.mocked(fetch)
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => ({
        detail: 'Invalid CSV file format',
      }),
    } as Response)

    render(<AnalysisPage />)

    const file = new File(['content'], 'test.csv', { type: 'text/csv' })
    const fileInput = document.querySelector('input[type="file"][accept=".csv"]') as HTMLInputElement
    if (fileInput) {
      await user.upload(fileInput, file)
    }

    await waitFor(() => {
      expect(screen.getByText(/選択中: test.csv/)).toBeInTheDocument()
    })

    // When
    const analyzeButton = screen.getByRole('button', { name: /analyze/i })
    await user.click(analyzeButton)

    // Then
    await waitFor(() => {
      expect(screen.getByText('Invalid CSV file format')).toBeInTheDocument()
    }, { timeout: 3000 })

    expect(screen.queryByText('Result')).not.toBeInTheDocument()
  })
})
