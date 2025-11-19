import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { FaPlane, FaComments, FaHistory, FaUser } from 'react-icons/fa'
import ChatPage from './pages/ChatPage'
import TripsPage from './pages/TripsPage'
import TripDetailPage from './pages/TripDetailPage'
import HomePage from './pages/HomePage'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex flex-col">
        {/* Navigation */}
        <nav className="bg-white shadow-md border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link to="/" className="flex items-center space-x-2">
                  <FaPlane className="text-primary-600 text-2xl" />
                  <span className="text-xl font-bold text-gray-900">
                    AI Travel Advisor
                  </span>
                </Link>
              </div>

              <div className="flex items-center space-x-4">
                <Link
                  to="/chat"
                  className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <FaComments className="text-primary-600" />
                  <span>Chat</span>
                </Link>

                <Link
                  to="/trips"
                  className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <FaHistory className="text-primary-600" />
                  <span>My Trips</span>
                </Link>

                <Link
                  to="/profile"
                  className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <FaUser className="text-primary-600" />
                  <span>Profile</span>
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 pb-24">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/trips" element={<TripsPage />} />
            <Route path="/trips/:id" element={<TripDetailPage />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 mt-auto">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <p className="text-center text-gray-600">
              © 2025 AI Travel Advisor. Powered by RAG & LangGraph.
            </p>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  )
}

export default App
