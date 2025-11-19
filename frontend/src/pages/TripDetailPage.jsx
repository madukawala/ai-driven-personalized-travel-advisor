import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import { FaArrowLeft, FaCalendar, FaDollarSign, FaCloudRain } from 'react-icons/fa'
import { getTrip } from '../services/api'
import { format } from 'date-fns'

export default function TripDetailPage() {
  const { id } = useParams()

  const { data: trip, isLoading, error } = useQuery({
    queryKey: ['trip', id],
    queryFn: () => getTrip(id),
  })

  if (isLoading) {
    return <div className="text-center py-12">Loading trip details...</div>
  }

  if (error || !trip) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-red-600 mb-4">Trip not found</h2>
        <Link to="/trips" className="btn-primary">
          Back to Trips
        </Link>
      </div>
    )
  }

  const itinerary = trip.itinerary_json

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <Link to="/trips" className="btn-secondary">
          <FaArrowLeft className="inline mr-2" />
          Back to Trips
        </Link>
        <span
          className={`px-3 py-1 rounded text-sm font-medium ${
            trip.status === 'completed'
              ? 'bg-green-100 text-green-800'
              : trip.status === 'confirmed'
              ? 'bg-blue-100 text-blue-800'
              : 'bg-yellow-100 text-yellow-800'
          }`}
        >
          {trip.status}
        </span>
      </div>

      {/* Trip Overview */}
      <div className="card">
        <h1 className="text-3xl font-bold mb-4">{trip.destination}</h1>

        <div className="grid md:grid-cols-3 gap-4 text-sm">
          <div>
            <div className="flex items-center text-gray-600 mb-1">
              <FaCalendar className="mr-2" />
              <span>Dates</span>
            </div>
            <p className="font-semibold">
              {format(new Date(trip.start_date), 'MMM d')} -{' '}
              {format(new Date(trip.end_date), 'MMM d, yyyy')}
            </p>
          </div>

          <div>
            <div className="flex items-center text-gray-600 mb-1">
              <FaDollarSign className="mr-2" />
              <span>Budget</span>
            </div>
            <p className="font-semibold">
              {trip.budget} {trip.budget_currency}
            </p>
            {itinerary?.summary && (
              <p className="text-xs text-gray-600">
                Est. Cost: ${itinerary.summary.total_estimated_cost.toFixed(2)}
              </p>
            )}
          </div>

          <div>
            <div className="flex items-center text-gray-600 mb-1">
              <span>Quality Score</span>
            </div>
            <p className="font-semibold">
              {trip.quality_score ? `${trip.quality_score}/100` : 'N/A'}
            </p>
          </div>
        </div>

        {trip.interests && trip.interests.length > 0 && (
          <div className="mt-4">
            <p className="text-sm text-gray-600 mb-2">Interests:</p>
            <div className="flex flex-wrap gap-2">
              {trip.interests.map((interest, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
                >
                  {interest}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Daily Itinerary */}
      {itinerary?.daily_itineraries && itinerary.daily_itineraries.length > 0 && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-6">Itinerary</h2>

          <div className="space-y-6">
            {itinerary.daily_itineraries.map((day, idx) => (
              <div key={idx} className="border-l-4 border-primary-600 pl-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-lg font-semibold">
                    Day {day.day_number} - {format(new Date(day.date), 'EEEE, MMM d')}
                  </h3>
                  {day.estimated_cost && (
                    <span className="text-sm text-gray-600">
                      ${day.estimated_cost.toFixed(2)}
                    </span>
                  )}
                </div>

                {day.weather && (
                  <div className="flex items-center text-sm text-gray-600 mb-3">
                    <FaCloudRain className="mr-2" />
                    <span>
                      {day.weather.condition}, {day.weather.high}°C / {day.weather.low}
                      °C
                    </span>
                    {day.weather.rain_chance > 30 && (
                      <span className="ml-2 text-yellow-600">
                        ({day.weather.rain_chance}% rain)
                      </span>
                    )}
                  </div>
                )}

                {day.activities && day.activities.length > 0 && (
                  <div className="space-y-3">
                    {day.activities.map((activity, actIdx) => (
                      <div
                        key={actIdx}
                        className="p-3 bg-gray-50 rounded"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <p className="font-medium text-sm">
                              {activity.time_slot || activity.description}
                            </p>
                            {activity.description && activity.time_slot && (
                              <p className="text-sm text-gray-600 mt-1">
                                {activity.description}
                              </p>
                            )}
                          </div>
                          {activity.cost > 0 && (
                            <span className="text-sm text-gray-600 ml-2">
                              ${activity.cost}
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {day.recommendations && day.recommendations.length > 0 && (
                  <div className="mt-3 p-3 bg-blue-50 rounded">
                    <p className="text-sm font-medium text-blue-900 mb-1">
                      Recommendations:
                    </p>
                    {day.recommendations.map((rec, recIdx) => (
                      <p key={recIdx} className="text-sm text-blue-800">
                        • {rec}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Risk Analysis */}
      {trip.risk_analysis && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-4">Risk Analysis</h2>

          <div className="grid md:grid-cols-3 gap-4">
            {trip.risk_analysis.budget_risk && (
              <div className="p-4 border rounded">
                <h3 className="font-semibold mb-2">Budget Risk</h3>
                <p
                  className={`text-lg font-bold ${
                    trip.risk_analysis.budget_risk.overrun_risk === 'high'
                      ? 'text-red-600'
                      : trip.risk_analysis.budget_risk.overrun_risk === 'medium'
                      ? 'text-yellow-600'
                      : 'text-green-600'
                  }`}
                >
                  {trip.risk_analysis.budget_risk.overrun_risk.toUpperCase()}
                </p>
              </div>
            )}

            {trip.risk_analysis.weather_risk && (
              <div className="p-4 border rounded">
                <h3 className="font-semibold mb-2">Weather Risk</h3>
                <p className="text-sm text-gray-600">
                  {trip.risk_analysis.weather_risk.rainy_days} rainy days expected
                </p>
              </div>
            )}

            {trip.risk_analysis.crowding_risk && (
              <div className="p-4 border rounded">
                <h3 className="font-semibold mb-2">Crowding Risk</h3>
                <p className="text-lg font-bold">
                  {trip.risk_analysis.crowding_risk.risk_level.toUpperCase()}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
