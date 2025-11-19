import { Link } from 'react-router-dom'
import { FaRobot, FaChartLine, FaGlobeAmericas, FaLightbulb } from 'react-icons/fa'

export default function HomePage() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center py-12">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          AI-Powered Travel Planning
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Let our AI advisor create personalized, optimized travel itineraries based on your
          preferences, budget, and real-time data.
        </p>
        <div className="flex justify-center space-x-4">
          <Link to="/chat" className="btn-primary text-lg px-8 py-3">
            Start Planning
          </Link>
          <Link to="/trips" className="btn-secondary text-lg px-8 py-3">
            View My Trips
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card text-center">
          <FaRobot className="text-4xl text-primary-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold mb-2">AI-Powered</h3>
          <p className="text-gray-600">
            Advanced RAG system with LangGraph orchestration for intelligent planning
          </p>
        </div>

        <div className="card text-center">
          <FaChartLine className="text-4xl text-primary-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold mb-2">Risk Analysis</h3>
          <p className="text-gray-600">
            Real-time weather, budget, and crowding risk analysis for better decisions
          </p>
        </div>

        <div className="card text-center">
          <FaGlobeAmericas className="text-4xl text-primary-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold mb-2">Real-Time Data</h3>
          <p className="text-gray-600">
            Live weather, events, currency rates, and travel advisories
          </p>
        </div>

        <div className="card text-center">
          <FaLightbulb className="text-4xl text-primary-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold mb-2">Smart Recommendations</h3>
          <p className="text-gray-600">
            Personalized suggestions based on your interests and travel history
          </p>
        </div>
      </div>

      {/* How It Works */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div>
            <div className="flex items-center mb-3">
              <span className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-3">
                1
              </span>
              <h3 className="font-semibold">Tell Us Your Plans</h3>
            </div>
            <p className="text-gray-600 ml-11">
              Chat with our AI about your destination, dates, budget, and interests.
            </p>
          </div>

          <div>
            <div className="flex items-center mb-3">
              <span className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-3">
                2
              </span>
              <h3 className="font-semibold">AI Analyzes & Plans</h3>
            </div>
            <p className="text-gray-600 ml-11">
              Our system fetches real-time data and creates an optimized itinerary.
            </p>
          </div>

          <div>
            <div className="flex items-center mb-3">
              <span className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-3">
                3
              </span>
              <h3 className="font-semibold">Review & Refine</h3>
            </div>
            <p className="text-gray-600 ml-11">
              Get a detailed itinerary with risks, costs, and alternatives to adjust as needed.
            </p>
          </div>
        </div>
      </div>

      {/* Example Queries */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">Try These Examples</h2>
        <div className="space-y-3">
          <Link
            to="/chat"
            className="block p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <p className="text-gray-800">
              "Plan me a food and art trip in Tokyo from Sept 2-6 with a $700 budget"
            </p>
          </Link>
          <Link
            to="/chat"
            className="block p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <p className="text-gray-800">
              "I want a 5-day cultural tour of Rome with vegan food options and no early mornings"
            </p>
          </Link>
          <Link
            to="/chat"
            className="block p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <p className="text-gray-800">
              "Create a budget-friendly Barcelona itinerary for architecture lovers, $500 total"
            </p>
          </Link>
        </div>
      </div>
    </div>
  )
}
