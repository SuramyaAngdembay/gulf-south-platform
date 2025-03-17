<template>
  <div class="notification-center">
    <el-popover
      v-model:visible="showNotifications"
      placement="bottom-end"
      :width="400"
      trigger="click"
    >
      <template #reference>
        <el-badge :value="unreadCount" :hidden="unreadCount === 0" class="notification-badge">
          <el-button class="notification-trigger" @click="showNotifications = true">
            <el-icon><Bell /></el-icon>
          </el-button>
        </el-badge>
      </template>

      <div class="notification-container">
        <div class="notification-header">
          <h3>Notifications</h3>
          <div class="header-actions">
            <el-button
              v-if="unreadCount > 0"
              type="text"
              size="small"
              @click="markAllAsRead"
            >
              Mark all as read
            </el-button>
            <el-button
              type="text"
              size="small"
              @click="clearAll"
            >
              Clear all
            </el-button>
          </div>
        </div>

        <div class="notification-filters">
          <el-radio-group v-model="filter" size="small">
            <el-radio-button label="all">All</el-radio-button>
            <el-radio-button label="unread">Unread</el-radio-button>
          </el-radio-group>
        </div>

        <div class="notification-list" v-if="filteredNotifications.length > 0">
          <div
            v-for="notification in filteredNotifications"
            :key="notification.id"
            class="notification-item"
            :class="{ unread: !notification.read }"
            @click="handleNotificationClick(notification)"
          >
            <div class="notification-icon">
              <el-icon>
                <component :is="getNotificationIcon(notification.type)" />
              </el-icon>
            </div>
            <div class="notification-content">
              <p class="notification-text">{{ notification.message }}</p>
              <div class="notification-meta">
                <span class="notification-time">{{ formatTime(notification.timestamp) }}</span>
                <el-tag size="small" :type="getNotificationType(notification.type)">
                  {{ notification.type }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="no-notifications">
          No notifications
        </div>
      </div>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Bell,
  Message,
  Calendar,
  Document,
  Collection,
  User,
  Warning,
  Success
} from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const showNotifications = ref(false)
const notifications = ref([])
const filter = ref('all')

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

const filteredNotifications = computed(() => {
  if (filter.value === 'all') {
    return notifications.value
  }
  return notifications.value.filter(n => !n.read)
})

const getNotificationIcon = (type) => {
  const icons = {
    message: Message,
    event: Calendar,
    document: Document,
    research: Collection,
    user: User,
    warning: Warning,
    success: Success
  }
  return icons[type] || Message
}

const getNotificationType = (type) => {
  const types = {
    message: 'primary',
    event: 'success',
    document: 'info',
    research: 'warning',
    user: 'success',
    warning: 'danger',
    success: 'success'
  }
  return types[type] || 'info'
}

const formatTime = (timestamp) => {
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

const handleNotificationClick = async (notification) => {
  if (!notification.read) {
    await markAsRead(notification.id)
  }

  // Handle navigation based on notification type
  switch (notification.type) {
    case 'event':
      router.push(`/events/${notification.data.eventId}`)
      break
    case 'document':
      router.push(`/resources/${notification.data.documentId}`)
      break
    case 'research':
      router.push(`/research/${notification.data.researchId}`)
      break
    case 'user':
      router.push(`/profile/${notification.data.userId}`)
      break
    case 'message':
      router.push('/messages')
      break
  }

  showNotifications.value = false
}

const markAsRead = async (notificationId) => {
  try {
    await axios.post(`/api/notifications/${notificationId}/read`)
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.read = true
    }
  } catch (error) {
    ElMessage.error('Failed to mark notification as read')
  }
}

const markAllAsRead = async () => {
  try {
    await axios.post('/api/notifications/read-all')
    notifications.value.forEach(n => n.read = true)
  } catch (error) {
    ElMessage.error('Failed to mark all notifications as read')
  }
}

const clearAll = async () => {
  try {
    await axios.delete('/api/notifications')
    notifications.value = []
  } catch (error) {
    ElMessage.error('Failed to clear notifications')
  }
}

const fetchNotifications = async () => {
  try {
    const response = await axios.get('/api/notifications')
    notifications.value = response.data
  } catch (error) {
    ElMessage.error('Failed to fetch notifications')
  }
}

// Fetch notifications when component is mounted
onMounted(() => {
  fetchNotifications()
})

// Set up WebSocket connection for real-time notifications
let ws: WebSocket | null = null

const setupWebSocket = () => {
  ws = new WebSocket(process.env.VUE_APP_WS_URL || 'ws://localhost:8000/ws/notifications')
  
  ws.onmessage = (event) => {
    const notification = JSON.parse(event.data)
    notifications.value.unshift(notification)
  }

  ws.onclose = () => {
    // Attempt to reconnect after 5 seconds
    setTimeout(setupWebSocket, 5000)
  }
}

onMounted(() => {
  setupWebSocket()
})

onUnmounted(() => {
  if (ws) {
    ws.close()
  }
})
</script>

<style scoped>
.notification-center {
  display: inline-block;
}

.notification-badge {
  margin-right: 8px;
}

.notification-trigger {
  padding: 8px;
}

.notification-container {
  display: flex;
  flex-direction: column;
  height: 500px;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
}

.notification-header h3 {
  margin: 0;
  font-size: 1rem;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.notification-filters {
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
}

.notification-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.notification-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.notification-item:hover {
  background-color: #f5f7fa;
}

.notification-item.unread {
  background-color: #ecf5ff;
}

.notification-icon {
  color: #409EFF;
  font-size: 1.2rem;
}

.notification-content {
  flex: 1;
}

.notification-text {
  margin: 0 0 4px 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.notification-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 0.8rem;
}

.no-notifications {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  font-size: 0.9rem;
}
</style> 