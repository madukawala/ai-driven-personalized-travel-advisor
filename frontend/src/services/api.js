import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Trip APIs
export const createTrip = async (tripData) => {
  const response = await api.post('/api/trips', tripData)
  return response.data
}

export const getTrip = async (tripId) => {
  const response = await api.get(`/api/trips/${tripId}`)
  return response.data
}

export const listTrips = async (userId = 1) => {
  const response = await api.get('/api/trips', { params: { user_id: userId } })
  return response.data
}

export const updateTrip = async (tripId, tripData) => {
  const response = await api.put(`/api/trips/${tripId}`, tripData)
  return response.data
}

export const deleteTrip = async (tripId) => {
  await api.delete(`/api/trips/${tripId}`)
}

// Chat APIs
export const sendChatMessage = async (messageData) => {
  const response = await api.post('/api/chat', messageData)
  return response.data
}

export const listConversations = async (userId = 1) => {
  const response = await api.get('/api/conversations', { params: { user_id: userId } })
  return response.data
}

// User APIs
export const getCurrentUser = async () => {
  const response = await api.get('/api/users/me')
  return response.data
}

export const getUserPreferences = async (userId = 1) => {
  const response = await api.get('/api/users/preferences', { params: { user_id: userId } })
  return response.data
}

export const updateUserPreferences = async (preferences, userId = 1) => {
  const response = await api.post('/api/users/preferences', preferences, {
    params: { user_id: userId },
  })
  return response.data
}

export const getUserMemory = async (userId = 1) => {
  const response = await api.get(`/api/memory/${userId}`)
  return response.data
}

export default api
