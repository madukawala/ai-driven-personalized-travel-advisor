import { useState } from 'react'
import { format } from 'date-fns'

export default function TripPlanForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    destination: '',
    start_date: '',
    end_date: '',
    budget: '',
    budget_currency: 'USD',
    interests: [],
    constraints: {},
  })

  const interestOptions = [
    'food',
    'culture',
    'art',
    'history',
    'adventure',
    'nature',
    'shopping',
    'nightlife',
    'architecture',
    'photography',
  ]

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit({
      ...formData,
      budget: parseFloat(formData.budget),
      start_date: new Date(formData.start_date).toISOString(),
      end_date: new Date(formData.end_date).toISOString(),
    })
  }

  const toggleInterest = (interest) => {
    setFormData((prev) => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter((i) => i !== interest)
        : [...prev.interests, interest],
    }))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Destination
        </label>
        <input
          type="text"
          required
          value={formData.destination}
          onChange={(e) => setFormData({ ...formData, destination: e.target.value })}
          className="input-field"
          placeholder="e.g., Tokyo, Paris, New York"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Start Date
          </label>
          <input
            type="date"
            required
            value={formData.start_date}
            onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
            className="input-field"
            min={format(new Date(), 'yyyy-MM-dd')}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            End Date
          </label>
          <input
            type="date"
            required
            value={formData.end_date}
            onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
            className="input-field"
            min={formData.start_date || format(new Date(), 'yyyy-MM-dd')}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Budget</label>
          <input
            type="number"
            required
            value={formData.budget}
            onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
            className="input-field"
            placeholder="1000"
            min="0"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Currency
          </label>
          <select
            value={formData.budget_currency}
            onChange={(e) =>
              setFormData({ ...formData, budget_currency: e.target.value })
            }
            className="input-field"
          >
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
            <option value="GBP">GBP</option>
            <option value="JPY">JPY</option>
          </select>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Interests (select all that apply)
        </label>
        <div className="flex flex-wrap gap-2">
          {interestOptions.map((interest) => (
            <button
              key={interest}
              type="button"
              onClick={() => toggleInterest(interest)}
              className={`px-3 py-1 rounded-full text-sm ${
                formData.interests.includes(interest)
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {interest}
            </button>
          ))}
        </div>
      </div>

      <button type="submit" disabled={isLoading} className="btn-primary w-full">
        {isLoading ? 'Creating Trip...' : 'Create Trip Plan'}
      </button>
    </form>
  )
}
