import { describe, it, expect, vi, beforeEach } from 'vitest'
import analyzeFertility from './analysis'
import type FixedEffectsResult from '../types/fixedEffectsResult'

// Mock fetch
global.fetch = vi.fn()

describe('analyzeFertility', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('calls backend API with correct parameters', async () => {
    const mockResult: FixedEffectsResult = {
      nobs: 100,
      params: { unmarried: 0.5 },
      std_errors: { unmarried: 0.1 },
      tstats: { unmarried: 5.0 },
      pvalues: { unmarried: 0.001 },
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

    const csvFile = new File(['content'], 'test.csv', { type: 'text/csv' })
    const dependentVar = 'TFR'
    const independentVars = ['unmarried', 'employment_rate']

    const result = await analyzeFertility({
      csvFile,
      dependentVar,
      independentVars,
    })

    // Verify fetch was called
    expect(mockFetch).toHaveBeenCalledTimes(1)

    // Verify fetch was called with correct URL
    const callArgs = mockFetch.mock.calls[0]
    expect(callArgs[0]).toContain('/analysis')

    // Verify request method and FormData
    const requestOptions = callArgs[1]
    expect(requestOptions?.method).toBe('POST')
    expect(requestOptions?.body).toBeInstanceOf(FormData)

    // Verify result
    expect(result).toEqual(mockResult)
  })

  it('throws error when backend returns error response', async () => {
    const mockFetch = vi.mocked(fetch)
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => ({
        detail: 'Invalid CSV file format',
      }),
    } as Response)

    const csvFile = new File(['content'], 'test.csv', { type: 'text/csv' })

    await expect(
      analyzeFertility({
        csvFile,
        dependentVar: 'TFR',
        independentVars: ['unmarried'],
      })
    ).rejects.toThrow('Invalid CSV file format')
  })

  it('throws error with status code when detail is not provided', async () => {
    const mockFetch = vi.mocked(fetch)
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({}),
    } as Response)

    const csvFile = new File(['content'], 'test.csv', { type: 'text/csv' })

    await expect(
      analyzeFertility({
        csvFile,
        dependentVar: 'TFR',
        independentVars: ['unmarried'],
      })
    ).rejects.toThrow('Request failed with status 500')
  })

  it('includes all independent variables in FormData', async () => {
    const mockResult: FixedEffectsResult = {
      nobs: 100,
      params: {},
      std_errors: {},
      tstats: {},
      pvalues: {},
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

    const csvFile = new File(['content'], 'test.csv', { type: 'text/csv' })
    const independentVars = ['var1', 'var2', 'var3']

    await analyzeFertility({
      csvFile,
      dependentVar: 'TFR',
      independentVars,
    })

    // Verify FormData was created with correct data
    const callArgs = mockFetch.mock.calls[0]
    const formData = callArgs[1]?.body as FormData

    expect(formData.get('dependent_var')).toBe('TFR')
    expect(formData.get('csv_file')).toBe(csvFile)
    expect(formData.getAll('independent_vars')).toEqual(independentVars)
  })
})
