import { FaUser, FaRobot, FaExclamationTriangle } from 'react-icons/fa'

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`chat-message ${isUser ? 'user' : 'assistant'} max-w-2xl`}
      >
        <div className="flex items-start space-x-2">
          <div className="flex-shrink-0">
            {isUser ? (
              <FaUser className="text-lg" />
            ) : (
              <FaRobot className="text-lg text-primary-600" />
            )}
          </div>
          <div className="flex-1">
            <p className="whitespace-pre-wrap">{message.content}</p>

            {/* Show warnings if present */}
            {message.trip_data?.warnings && message.trip_data.warnings.length > 0 && (
              <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded">
                <div className="flex items-start space-x-2">
                  <FaExclamationTriangle className="text-yellow-600 mt-1" />
                  <div>
                    {message.trip_data.warnings.map((warning, idx) => (
                      <p key={idx} className="text-sm text-yellow-800">
                        {warning}
                      </p>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Show suggestions */}
            {message.suggestions && message.suggestions.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2">
                {message.suggestions.map((suggestion, idx) => (
                  <button
                    key={idx}
                    className="text-xs px-3 py-1 bg-primary-100 text-primary-700 rounded-full hover:bg-primary-200"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
