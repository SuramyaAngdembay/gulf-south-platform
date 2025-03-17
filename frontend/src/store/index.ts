import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: false,
    loading: false,
    error: null
  },
  mutations: {
    setUser(state, user) {
      state.user = user
      state.isAuthenticated = !!user
    },
    setToken(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    setLoading(state, loading) {
      state.loading = loading
    },
    setError(state, error) {
      state.error = error
    },
    logout(state) {
      state.user = null
      state.token = null
      state.isAuthenticated = false
      localStorage.removeItem('token')
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        commit('setLoading', true)
        const response = await axios.post('http://localhost:5000/api/auth/login', credentials)
        const { token, user } = response.data
        commit('setToken', token)
        commit('setUser', user)
        return user
      } catch (error) {
        commit('setError', error.response?.data?.error || 'Login failed')
        throw error
      } finally {
        commit('setLoading', false)
      }
    },
    async register({ commit }, userData) {
      try {
        commit('setLoading', true)
        const response = await axios.post('http://localhost:5000/api/auth/register', userData)
        const { token, user } = response.data
        commit('setToken', token)
        commit('setUser', user)
        return user
      } catch (error) {
        commit('setError', error.response?.data?.error || 'Registration failed')
        throw error
      } finally {
        commit('setLoading', false)
      }
    },
    async fetchUserProfile({ commit }) {
      try {
        commit('setLoading', true)
        const response = await axios.get('http://localhost:5000/api/users/profile', {
          headers: { Authorization: `Bearer ${this.state.token}` }
        })
        commit('setUser', response.data)
        return response.data
      } catch (error) {
        commit('setError', error.response?.data?.error || 'Failed to fetch profile')
        throw error
      } finally {
        commit('setLoading', false)
      }
    },
    logout({ commit }) {
      commit('logout')
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    currentUser: state => state.user,
    isLoading: state => state.loading,
    error: state => state.error
  }
}) 