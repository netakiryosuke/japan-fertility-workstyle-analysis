import type { FixedEffectsResult } from "../types/fixedEffectsResult"
import calculateSignificanceStars from "../utils/calculateSignificantStars"
import formatNumber from "../utils/formatNumber"

interface Props {
    result: FixedEffectsResult
}

export default function CoefficientTable({ result }: Props) {
    const variables = Object.keys(result.params)

    return (
        <div className="overflow-x-auto">
            <table className="min-w-full border border-gray-200 text-sm">
                <thead className="bg-gray-50">
                    <tr>
                        <th className="px-3 py-2 text-left">Variable</th>
                        <th className="px-3 py-2 text-right">Coef.</th>
                        <th className="px-3 py-2 text-right">Std. Err.</th>
                        <th className="px-3 py-2 text-right">t</th>
                        <th className="px-3 py-2 text-right">P&gt;|t|</th>
                    </tr>
                </thead>

                <tbody>
                    {variables.map(v => {
                        const p = result.pvalues[v]
                        return (
                            <tr key={v} className="border-t">
                                <td className="px-3 py-2">{v}</td>
                                <td className="px-3 py-2 text-right">
                                    {formatNumber(result.params[v])}
                                </td>
                                <td className="px-3 py-2 text-right">
                                    {formatNumber(result.std_errors[v])}
                                </td>
                                <td className="px-3 py-2 text-right">
                                    {formatNumber(result.tstats[v])}
                                </td>
                                <td
                                    className={`px-3 py-2 text-right ${p < 0.05 ? "font-semibold text-gray-900" : "text-gray-600"
                                        }`}
                                >
                                    {formatNumber(p)} {calculateSignificanceStars(p)}
                                </td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    )
}
