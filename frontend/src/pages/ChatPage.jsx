import { useState } from 'react'
import { FaPaperPlane, FaPlus, FaSpinner } from 'react-icons/fa'
import { useMutation } from '@tanstack/react-query'
import { sendChatMessage, createTrip } from '../services/api'
import ChatMessage from '../components/ChatMessage'
import TripPlanForm from '../components/TripPlanForm'
import TripResultCard from '../components/TripResultCard'

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        'Hi! I\'m your AI Travel Advisor. I can help you plan personalized trips based on your preferences, budget, and interests. You can either:\n\n1. Tell me about your travel plans in natural language (e.g., "Plan a 5-day food tour in Tokyo for $700")\n2. Use the form below to provide detailed trip information\n\nHow would you like to proceed?',
    },
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [showTripForm, setShowTripForm] = useState(false)
  const [tripResult, setTripResult] = useState(null)
  const [conversationId, setConversationId] = useState(null)

  // Chat mutation
  const chatMutation = useMutation({
    mutationFn: sendChatMessage,
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.message,
          metadata: data.metadata,
          suggestions: data.suggestions,
        },
      ])
      if (data.conversation_id) {
        setConversationId(data.conversation_id)
      }
    },
  })

  // Trip creation mutation
  const tripMutation = useMutation({
    mutationFn: createTrip,
    onSuccess: (data) => {
      setTripResult(data)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.message || 'Trip created successfully!',
          trip_data: data,
        },
      ])
      setShowTripForm(false)
    },
  })

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim()) return

    // Add user message
    const userMessage = { role: 'user', content: inputMessage }
    setMessages((prev) => [...prev, userMessage])
    setInputMessage('')

    // Send to API
    chatMutation.mutate({
      message: inputMessage,
      conversation_id: conversationId,
    })
  }

  const handleTripSubmit = (tripData) => {
    // Add user message showing trip request
    setMessages((prev) => [
      ...prev,
      {
        role: 'user',
        content: `Creating trip to ${tripData.destination} from ${new Date(
          tripData.start_date
        ).toLocaleDateString()} to ${new Date(tripData.end_date).toLocaleDateString()} with budget $${
          tripData.budget
        }`,
      },
    ])

    // Create trip
    tripMutation.mutate(tripData)
  }

  const handleQuickAction = (action) => {
    setInputMessage(action)
  }

  return (
    <div className="grid lg:grid-cols-3 gap-6 min-h-[500px]">
      {/* Chat Section */}
      <div className="lg:col-span-2 flex flex-col bg-white rounded-lg shadow-md max-h-[calc(100vh-250px)]">
        {/* Chat Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold">Chat with AI Travel Advisor</h2>
          <button
            onClick={() => setShowTripForm(!showTripForm)}
            className="btn-secondary text-sm"
          >
            <FaPlus className="inline mr-2" />
            {showTripForm ? 'Hide Form' : 'New Trip Form'}
          </button>
        </div>

        {/* Trip Form (if visible) */}
        {showTripForm && (
          <div className="p-4 border-b border-gray-200 bg-gray-50">
            <TripPlanForm
              onSubmit={handleTripSubmit}
              isLoading={tripMutation.isPending}
            />
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}

          {(chatMutation.isPending || tripMutation.isPending) && (
            <div className="flex items-center justify-center p-4">
              <FaSpinner className="animate-spin text-primary-600 text-2xl mr-2" />
              <span className="text-gray-600">
                {tripMutation.isPending ? 'Creating your trip...' : 'Thinking...'}
              </span>
            </div>
          )}
        </div>

        {/* Input Form */}
        <div className="p-4 border-t border-gray-200">
          {/* Quick Actions */}
          <div className="flex flex-wrap gap-2 mb-3">
            <button
              onClick={() => handleQuickAction('Show me my past trips')}
              className="text-xs px-3 py-1 bg-gray-100 rounded-full hover:bg-gray-200"
            >
              My Past Trips
            </button>
            <button
              onClick={() => handleQuickAction('What are popular destinations right now?')}
              className="text-xs px-3 py-1 bg-gray-100 rounded-full hover:bg-gray-200"
            >
              Popular Destinations
            </button>
            <button
              onClick={() => handleQuickAction('Help me plan a budget-friendly trip')}
              className="text-xs px-3 py-1 bg-gray-100 rounded-full hover:bg-gray-200"
            >
              Budget Tips
            </button>
          </div>

          {/* Message Input */}
          <form onSubmit={handleSendMessage} className="flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message here..."
              className="input-field"
              disabled={chatMutation.isPending}
            />
            <button
              type="submit"
              disabled={chatMutation.isPending || !inputMessage.trim()}
              className="btn-primary"
            >
              <FaPaperPlane />
            </button>
          </form>
        </div>
      </div>

      {/* Sidebar - Trip Result */}
      <div className="lg:col-span-1">
        {tripResult ? (
          <TripResultCard tripResult={tripResult} />
        ) : (
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Tips</h3>
            <ul className="space-y-3 text-sm text-gray-600">
              <li>• Be specific about your interests and constraints</li>
              <li>• Mention your budget and preferred dates</li>
              <li>• Ask about risks, weather, or local events</li>
              <li>• Request alternatives or modifications</li>
              <li>• Save trips for future reference</li>
            </ul>

            <h3 className="text-lg font-semibold mb-4 mt-6">Example Queries</h3>
            <div className="space-y-2">
              <button
                onClick={() =>
                  handleQuickAction(
                    'Plan a food and culture trip to Tokyo for 5 days with $800 budget'
                  )
                }
                className="w-full text-left p-2 text-sm bg-gray-50 rounded hover:bg-gray-100"
              >
                Food & culture in Tokyo
              </button>
              <button
                onClick={() =>
                  handleQuickAction(
                    'I want to visit Paris museums for 3 days, budget $600, no early mornings'
                  )
                }
                className="w-full text-left p-2 text-sm bg-gray-50 rounded hover:bg-gray-100"
              >
                Museums in Paris
              </button>
              <button
                onClick={() =>
                  handleQuickAction(
                    'Create a budget beach vacation in Thailand for a week under $500'
                  )
                }
                className="w-full text-left p-2 text-sm bg-gray-50 rounded hover:bg-gray-100"
              >
                Beach trip to Thailand
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
