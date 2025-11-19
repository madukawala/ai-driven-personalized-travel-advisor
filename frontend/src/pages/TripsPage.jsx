import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { FaMapMarkerAlt, FaCalendar, FaDollarSign, FaStar } from 'react-icons/fa'
import { listTrips } from '../services/api'
import { format } from 'date-fns'

export default function TripsPage() {
  const { data: trips, isLoading, error } = useQuery({
    queryKey: ['trips'],
    queryFn: () => listTrips(1),
  })

  if (isLoading) {
    return <div className="text-center py-12">Loading your trips...</div>
  }

  if (error) {
    return (
      <div className="text-center py-12 text-red-600">
        Error loading trips: {error.message}
      </div>
    )
  }

  if (!trips || trips.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold mb-4">No trips yet</h2>
        <p className="text-gray-600 mb-6">
          Start planning your first trip with our AI advisor
        </p>
        <Link to="/chat" className="btn-primary">
          Plan a Trip
        </Link>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">My Trips</h1>
        <Link to="/chat" className="btn-primary">
          Plan New Trip
        </Link>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {trips.map((trip) => (
          <Link
            key={trip.id}
            to={`/trips/${trip.id}`}
            className="card hover:shadow-lg transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <h3 className="text-xl font-semibold">{trip.destination}</h3>
              <span
                className={`px-2 py-1 rounded text-xs font-medium ${
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

            <div className="space-y-2 text-sm text-gray-600">
              <div className="flex items-center">
                <FaMapMarkerAlt className="mr-2 text-primary-600" />
                <span>{trip.destination}</span>
              </div>

              <div className="flex items-center">
                <FaCalendar className="mr-2 text-primary-600" />
                <span>
                  {format(new Date(trip.start_date), 'MMM d')} -{' '}
                  {format(new Date(trip.end_date), 'MMM d, yyyy')}
                </span>
              </div>

              <div className="flex items-center">
                <FaDollarSign className="mr-2 text-primary-600" />
                <span>
                  {trip.budget} {trip.budget_currency}
                </span>
              </div>

              {trip.quality_score && (
                <div className="flex items-center">
                  <FaStar className="mr-2 text-yellow-500" />
                  <span>Quality Score: {trip.quality_score}/100</span>
                </div>
              )}
            </div>

            {trip.interests && trip.interests.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-1">
                {trip.interests.slice(0, 3).map((interest, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-gray-100 rounded text-xs text-gray-600"
                  >
                    {interest}
                  </span>
                ))}
                {trip.interests.length > 3 && (
                  <span className="px-2 py-1 bg-gray-100 rounded text-xs text-gray-600">
                    +{trip.interests.length - 3}
                  </span>
                )}
              </div>
            )}
          </Link>
        ))}
      </div>
    </div>
  )
}
