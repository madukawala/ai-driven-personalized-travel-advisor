import { FaCheckCircle, FaExclamationTriangle, FaChartPie } from 'react-icons/fa'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

export default function TripResultCard({ tripResult }) {
  const { itinerary, risk_analysis, quality_score } = tripResult

  // Prepare budget breakdown data for pie chart
  const budgetData = itinerary?.summary
    ? [
        { name: 'Accommodation', value: itinerary.summary.total_estimated_cost * 0.4 },
        { name: 'Activities', value: itinerary.summary.total_estimated_cost * 0.3 },
        { name: 'Food', value: itinerary.summary.total_estimated_cost * 0.2 },
        { name: 'Transport', value: itinerary.summary.total_estimated_cost * 0.1 },
      ]
    : []

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']

  return (
    <div className="card space-y-6">
      <h3 className="text-xl font-bold">Trip Summary</h3>

      {/* Quality Score */}
      {risk_analysis?.quality_score && (
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">Trip Quality Score</span>
            <span className="text-2xl font-bold text-primary-600">
              {risk_analysis.quality_score.overall_score}/100
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full"
              style={{ width: `${risk_analysis.quality_score.overall_score}%` }}
            />
          </div>
          <p className="text-xs text-gray-600 mt-1">
            {risk_analysis.quality_score.comfort_level}
          </p>
        </div>
      )}

      {/* Budget */}
      {itinerary?.summary && (
        <div>
          <h4 className="font-semibold mb-2">Budget Breakdown</h4>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600">Estimated Cost</span>
            <span className="font-semibold">
              ${itinerary.summary.total_estimated_cost.toFixed(2)}
            </span>
          </div>
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm text-gray-600">Daily Average</span>
            <span className="text-sm">
              ${itinerary.summary.average_daily_cost.toFixed(2)}/day
            </span>
          </div>

          {/* Budget Pie Chart */}
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={budgetData}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={60}
                fill="#8884d8"
                dataKey="value"
              >
                {budgetData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Risks */}
      {risk_analysis && (
        <div>
          <h4 className="font-semibold mb-2">Risk Analysis</h4>
          <div className="space-y-2">
            {risk_analysis.budget_risk && (
              <div className="flex items-start space-x-2">
                <FaChartPie className="text-blue-600 mt-1" />
                <div className="text-sm">
                  <span className="font-medium">Budget Risk: </span>
                  <span
                    className={`${
                      risk_analysis.budget_risk.overrun_risk === 'high'
                        ? 'text-red-600'
                        : risk_analysis.budget_risk.overrun_risk === 'medium'
                        ? 'text-yellow-600'
                        : 'text-green-600'
                    }`}
                  >
                    {risk_analysis.budget_risk.overrun_risk}
                  </span>
                </div>
              </div>
            )}

            {risk_analysis.weather_risk && (
              <div className="flex items-start space-x-2">
                <FaExclamationTriangle className="text-yellow-600 mt-1" />
                <div className="text-sm">
                  <span className="font-medium">Weather: </span>
                  <span>
                    {risk_analysis.weather_risk.rainy_days} rainy days expected
                  </span>
                </div>
              </div>
            )}

            {risk_analysis.crowding_risk && (
              <div className="flex items-start space-x-2">
                <FaCheckCircle className="text-green-600 mt-1" />
                <div className="text-sm">
                  <span className="font-medium">Crowding: </span>
                  <span>{risk_analysis.crowding_risk.risk_level}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Warnings */}
      {tripResult.warnings && tripResult.warnings.length > 0 && (
        <div className="p-3 bg-yellow-50 border border-yellow-200 rounded">
          <h4 className="font-semibold text-yellow-800 mb-2 text-sm">Warnings</h4>
          {tripResult.warnings.map((warning, idx) => (
            <p key={idx} className="text-xs text-yellow-700">
              • {warning}
            </p>
          ))}
        </div>
      )}
    </div>
  )
}
