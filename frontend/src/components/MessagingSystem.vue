<template>
  <div class="messaging-system">
    <el-drawer
      v-model="showMessaging"
      direction="rtl"
      size="400px"
      :with-header="false"
    >
      <div class="messaging-container">
        <!-- Conversations List -->
        <div class="conversations-list" v-if="!activeConversation">
          <div class="conversations-header">
            <h3>Messages</h3>
            <el-button type="primary" @click="startNewConversation">
              New Message
            </el-button>
          </div>

          <div class="conversations-search">
            <el-input
              v-model="searchQuery"
              placeholder="Search conversations..."
              prefix-icon="Search"
            />
          </div>

          <div class="conversations">
            <div
              v-for="conversation in filteredConversations"
              :key="conversation.id"
              class="conversation-item"
              :class="{ active: activeConversation?.id === conversation.id }"
              @click="selectConversation(conversation)"
            >
              <el-avatar :src="conversation.participant.avatar" />
              <div class="conversation-info">
                <div class="conversation-header">
                  <span class="participant-name">{{ conversation.participant.name }}</span>
                  <span class="last-message-time">{{ formatTime(conversation.lastMessage?.timestamp) }}</span>
                </div>
                <div class="conversation-preview">
                  <span class="last-message">{{ conversation.lastMessage?.content }}</span>
                  <el-badge
                    v-if="conversation.unreadCount > 0"
                    :value="conversation.unreadCount"
                    class="unread-badge"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Active Conversation -->
        <div v-else class="active-conversation">
          <div class="conversation-header">
            <el-button @click="activeConversation = null">
              <el-icon><ArrowLeft /></el-icon>
            </el-button>
            <div class="participant-info">
              <el-avatar :src="activeConversation.participant.avatar" />
              <span>{{ activeConversation.participant.name }}</span>
            </div>
            <el-dropdown>
              <el-button>
                <el-icon><More /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="clearConversation">
                    Clear Conversation
                  </el-dropdown-item>
                  <el-dropdown-item @click="blockUser">
                    Block User
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>

          <div class="messages-container" ref="messagesContainer">
            <div
              v-for="message in activeConversation.messages"
              :key="message.id"
              class="message"
              :class="{ 'message-sent': message.senderId === currentUserId }"
            >
              <div class="message-content">
                {{ message.content }}
                <span class="message-time">{{ formatTime(message.timestamp) }}</span>
              </div>
            </div>
          </div>

          <div class="message-input">
            <el-input
              v-model="newMessage"
              type="textarea"
              :rows="3"
              placeholder="Type a message..."
              @keyup.enter.ctrl="sendMessage"
            />
            <el-button
              type="primary"
              :disabled="!newMessage.trim()"
              @click="sendMessage"
            >
              Send
            </el-button>
          </div>
        </div>

        <!-- New Conversation -->
        <div v-if="showNewConversation" class="new-conversation">
          <div class="new-conversation-header">
            <el-button @click="showNewConversation = false">
              <el-icon><ArrowLeft /></el-icon>
            </el-button>
            <h3>New Message</h3>
          </div>

          <div class="user-search">
            <el-input
              v-model="userSearchQuery"
              placeholder="Search users..."
              prefix-icon="Search"
              @input="searchUsers"
            />
          </div>

          <div class="search-results">
            <div
              v-for="user in searchResults"
              :key="user.id"
              class="user-item"
              @click="startConversationWithUser(user)"
            >
              <el-avatar :src="user.avatar" />
              <div class="user-info">
                <span class="user-name">{{ user.name }}</span>
                <span class="user-title">{{ user.title }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search,
  ArrowLeft,
  More
} from '@element-plus/icons-vue'
import axios from 'axios'

const showMessaging = ref(false)
const activeConversation = ref(null)
const showNewConversation = ref(false)
const conversations = ref([])
const searchQuery = ref('')
const userSearchQuery = ref('')
const searchResults = ref([])
const newMessage = ref('')
const messagesContainer = ref(null)
const currentUserId = ref(null) // This should be set from your auth store

const filteredConversations = computed(() => {
  if (!searchQuery.value) {
    return conversations.value
  }
  const query = searchQuery.value.toLowerCase()
  return conversations.value.filter(conv => 
    conv.participant.name.toLowerCase().includes(query) ||
    conv.lastMessage?.content.toLowerCase().includes(query)
  )
})

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date

  // Less than 1 minute
  if (diff < 60000) {
    return 'Just now'
  }
  // Less than 1 hour
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000)
    return `${minutes}m ago`
  }
  // Less than 24 hours
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours}h ago`
  }
  // Less than 7 days
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000)
    return `${days}d ago`
  }
  // Otherwise, show the date
  return date.toLocaleDateString()
}

const selectConversation = async (conversation) => {
  try {
    const response = await axios.get(`/api/conversations/${conversation.id}/messages`)
    activeConversation.value = {
      ...conversation,
      messages: response.data
    }
    await markConversationAsRead(conversation.id)
  } catch (error) {
    ElMessage.error('Failed to load conversation')
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !activeConversation.value) return

  try {
    const response = await axios.post(`/api/conversations/${activeConversation.value.id}/messages`, {
      content: newMessage.value
    })
    
    activeConversation.value.messages.push(response.data)
    newMessage.value = ''
    
    await nextTick()
    scrollToBottom()
  } catch (error) {
    ElMessage.error('Failed to send message')
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const markConversationAsRead = async (conversationId) => {
  try {
    await axios.post(`/api/conversations/${conversationId}/read`)
    const conversation = conversations.value.find(c => c.id === conversationId)
    if (conversation) {
      conversation.unreadCount = 0
    }
  } catch (error) {
    console.error('Failed to mark conversation as read:', error)
  }
}

const startNewConversation = () => {
  showNewConversation.value = true
}

const searchUsers = async () => {
  if (!userSearchQuery.value.trim()) {
    searchResults.value = []
    return
  }

  try {
    const response = await axios.get('/api/users/search', {
      params: { q: userSearchQuery.value }
    })
    searchResults.value = response.data
  } catch (error) {
    ElMessage.error('Failed to search users')
  }
}

const startConversationWithUser = async (user) => {
  try {
    const response = await axios.post('/api/conversations', {
      participantId: user.id
    })
    
    conversations.value.unshift(response.data)
    showNewConversation.value = false
    selectConversation(response.data)
  } catch (error) {
    ElMessage.error('Failed to start conversation')
  }
}

const clearConversation = async () => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to clear this conversation?',
      'Warning',
      {
        confirmButtonText: 'Clear',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )

    await axios.delete(`/api/conversations/${activeConversation.value.id}`)
    conversations.value = conversations.value.filter(
      c => c.id !== activeConversation.value.id
    )
    activeConversation.value = null
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to clear conversation')
    }
  }
}

const blockUser = async () => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to block this user?',
      'Warning',
      {
        confirmButtonText: 'Block',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )

    await axios.post(`/api/users/${activeConversation.value.participant.id}/block`)
    ElMessage.success('User blocked successfully')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to block user')
    }
  }
}

const fetchConversations = async () => {
  try {
    const response = await axios.get('/api/conversations')
    conversations.value = response.data
  } catch (error) {
    ElMessage.error('Failed to fetch conversations')
  }
}

// Set up WebSocket connection for real-time messages
let ws: WebSocket | null = null

const setupWebSocket = () => {
  ws = new WebSocket(process.env.VUE_APP_WS_URL || 'ws://localhost:8000/ws/messages')
  
  ws.onmessage = (event) => {
    const message = JSON.parse(event.data)
    
    // Update conversation list
    const conversation = conversations.value.find(c => c.id === message.conversationId)
    if (conversation) {
      conversation.lastMessage = message
      conversation.unreadCount++
      
      // If this is the active conversation, add the message and mark as read
      if (activeConversation.value?.id === message.conversationId) {
        activeConversation.value.messages.push(message)
        markConversationAsRead(message.conversationId)
        nextTick(() => scrollToBottom())
      }
    }
  }

  ws.onclose = () => {
    // Attempt to reconnect after 5 seconds
    setTimeout(setupWebSocket, 5000)
  }
}

onMounted(() => {
  fetchConversations()
  setupWebSocket()
})

onUnmounted(() => {
  if (ws) {
    ws.close()
  }
})
</script>

<style scoped>
.messaging-system {
  display: inline-block;
}

.messaging-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.conversations-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
}

.conversations-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.conversations-search {
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
}

.conversations {
  flex: 1;
  overflow-y: auto;
}

.conversation-item {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.conversation-item:hover {
  background-color: #f5f7fa;
}

.conversation-item.active {
  background-color: #ecf5ff;
}

.conversation-info {
  flex: 1;
  min-width: 0;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.participant-name {
  font-weight: 500;
}

.last-message-time {
  color: #909399;
  font-size: 0.8rem;
}

.conversation-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.last-message {
  color: #606266;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.unread-badge {
  flex-shrink: 0;
}

.active-conversation {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.conversation-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
}

.participant-info {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 70%;
  align-self: flex-start;
}

.message-sent {
  align-self: flex-end;
}

.message-content {
  padding: 8px 12px;
  border-radius: 8px;
  background-color: #f5f7fa;
  position: relative;
}

.message-sent .message-content {
  background-color: #ecf5ff;
}

.message-time {
  font-size: 0.7rem;
  color: #909399;
  margin-top: 4px;
  display: block;
}

.message-input {
  padding: 16px;
  border-top: 1px solid #ebeef5;
  display: flex;
  gap: 8px;
}

.new-conversation {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.new-conversation-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
}

.new-conversation-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.user-search {
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
}

.search-results {
  flex: 1;
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.user-item:hover {
  background-color: #f5f7fa;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
}

.user-title {
  color: #909399;
  font-size: 0.8rem;
}
</style> 