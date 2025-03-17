<template>
  <div class="events-container">
    <div class="header-section">
      <h1>Events & Conferences</h1>
      <el-button type="primary" @click="showCreateDialog = true" v-if="isAuthenticated">
        Create Event
      </el-button>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchQuery"
            placeholder="Search events..."
            prefix-icon="Search"
            clearable
            @input="handleSearch"
          />
        </el-col>
        <el-col :span="8">
          <el-select v-model="eraFilter" placeholder="Filter by Era" clearable>
            <el-option label="Colonial" value="colonial" />
            <el-option label="Antebellum" value="antebellum" />
            <el-option label="Civil War" value="civil_war" />
            <el-option label="Reconstruction" value="reconstruction" />
            <el-option label="Modern" value="modern" />
          </el-select>
        </el-col>
        <el-col :span="8">
          <el-select v-model="typeFilter" placeholder="Filter by Type" clearable>
            <el-option label="Conference" value="conference" />
            <el-option label="Workshop" value="workshop" />
            <el-option label="Lecture" value="lecture" />
            <el-option label="Exhibition" value="exhibition" />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <!-- Events List -->
    <el-row :gutter="20" class="events-grid">
      <el-col v-for="event in filteredEvents" :key="event.id" :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="event-card" :body-style="{ padding: '0px' }">
          <div class="event-header">
            <h3>{{ event.title }}</h3>
            <el-tag :type="getEventTypeTag(event.type)">{{ event.type }}</el-tag>
          </div>
          <div class="event-content">
            <p class="description">{{ event.description }}</p>
            <div class="meta-info">
              <p><el-icon><Calendar /></el-icon> {{ formatDate(event.date) }}</p>
              <p><el-icon><Location /></el-icon> {{ event.location }}</p>
              <p><el-icon><User /></el-icon> {{ event.organizer }}</p>
            </div>
          </div>
          <div class="event-actions">
            <el-button-group>
              <el-button type="primary" @click="handleViewDetails(event)">View Details</el-button>
              <el-button 
                type="success" 
                @click="handleRegister(event)"
                v-if="isAuthenticated && !event.isRegistered"
              >
                Register
              </el-button>
              <el-button 
                type="danger" 
                @click="handleUnregister(event)"
                v-if="isAuthenticated && event.isRegistered"
              >
                Unregister
              </el-button>
              <el-button 
                type="warning" 
                @click="handleEdit(event)"
                v-if="isAuthenticated && (event.organizer === currentUser?.id || isAdmin)"
              >
                Edit
              </el-button>
              <el-button 
                type="danger" 
                @click="handleDelete(event)"
                v-if="isAuthenticated && (event.organizer === currentUser?.id || isAdmin)"
              >
                Delete
              </el-button>
            </el-button-group>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Create/Edit Dialog -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingEvent ? 'Edit Event' : 'Create New Event'"
      width="50%"
    >
      <el-form
        ref="formRef"
        :model="eventForm"
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="Title" prop="title">
          <el-input v-model="eventForm.title" placeholder="Event title" />
        </el-form-item>

        <el-form-item label="Description" prop="description">
          <el-input
            v-model="eventForm.description"
            type="textarea"
            :rows="4"
            placeholder="Event description"
          />
        </el-form-item>

        <el-form-item label="Type" prop="type">
          <el-select v-model="eventForm.type" placeholder="Select event type">
            <el-option label="Conference" value="conference" />
            <el-option label="Workshop" value="workshop" />
            <el-option label="Lecture" value="lecture" />
            <el-option label="Exhibition" value="exhibition" />
          </el-select>
        </el-form-item>

        <el-form-item label="Date" prop="date">
          <el-date-picker
            v-model="eventForm.date"
            type="datetime"
            placeholder="Select date and time"
          />
        </el-form-item>

        <el-form-item label="Location" prop="location">
          <el-input v-model="eventForm.location" placeholder="Event location" />
        </el-form-item>

        <el-form-item label="Era Focus" prop="eraFocus">
          <el-select v-model="eventForm.eraFocus" placeholder="Select era">
            <el-option label="Colonial" value="colonial" />
            <el-option label="Antebellum" value="antebellum" />
            <el-option label="Civil War" value="civil_war" />
            <el-option label="Reconstruction" value="reconstruction" />
            <el-option label="Modern" value="modern" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">Cancel</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            {{ editingEvent ? 'Update' : 'Create' }}
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Delete Confirmation -->
    <el-dialog
      v-model="showDeleteDialog"
      title="Confirm Delete"
      width="30%"
    >
      <p>Are you sure you want to delete this event?</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDeleteDialog = false">Cancel</el-button>
          <el-button type="danger" @click="confirmDelete" :loading="loading">
            Delete
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Calendar, Location, User } from '@element-plus/icons-vue'
import axios from 'axios'

const store = useStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const events = ref([])
const showCreateDialog = ref(false)
const showDeleteDialog = ref(false)
const editingEvent = ref(null)
const searchQuery = ref('')
const eraFilter = ref('')
const typeFilter = ref('')

const eventForm = reactive({
  title: '',
  description: '',
  type: '',
  date: '',
  location: '',
  eraFocus: ''
})

const rules = reactive<FormRules>({
  title: [
    { required: true, message: 'Please enter event title', trigger: 'blur' },
    { min: 3, message: 'Title must be at least 3 characters', trigger: 'blur' }
  ],
  description: [
    { required: true, message: 'Please enter event description', trigger: 'blur' },
    { min: 10, message: 'Description must be at least 10 characters', trigger: 'blur' }
  ],
  type: [
    { required: true, message: 'Please select event type', trigger: 'change' }
  ],
  date: [
    { required: true, message: 'Please select event date', trigger: 'change' }
  ],
  location: [
    { required: true, message: 'Please enter event location', trigger: 'blur' }
  ],
  eraFocus: [
    { required: true, message: 'Please select era focus', trigger: 'change' }
  ]
})

const isAuthenticated = computed(() => store.getters.isAuthenticated)
const currentUser = computed(() => store.getters.currentUser)
const isAdmin = computed(() => currentUser.value?.role === 'admin')

const filteredEvents = computed(() => {
  return events.value.filter(event => {
    const matchesSearch = event.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         event.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesEra = !eraFilter.value || event.eraFocus === eraFilter.value
    const matchesType = !typeFilter.value || event.type === typeFilter.value
    return matchesSearch && matchesEra && matchesType
  })
})

const getEventTypeTag = (type: string) => {
  const types = {
    conference: 'primary',
    workshop: 'success',
    lecture: 'warning',
    exhibition: 'info'
  }
  return types[type] || 'info'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

const fetchEvents = async () => {
  try {
    loading.value = true
    const response = await axios.get('/events')
    events.value = response.data
  } catch (error) {
    ElMessage.error('Failed to fetch events')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    if (editingEvent.value) {
      await axios.put(`/events/${editingEvent.value.id}`, eventForm)
      ElMessage.success('Event updated successfully')
    } else {
      await axios.post('/events', eventForm)
      ElMessage.success('Event created successfully')
    }
    
    showCreateDialog.value = false
    fetchEvents()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || 'Operation failed')
  } finally {
    loading.value = false
  }
}

const handleViewDetails = (event) => {
  // Implement event details view
  console.log('View details:', event)
}

const handleRegister = async (event) => {
  try {
    loading.value = true
    await axios.post(`/events/${event.id}/register`)
    ElMessage.success('Successfully registered for event')
    fetchEvents()
  } catch (error) {
    ElMessage.error('Failed to register for event')
  } finally {
    loading.value = false
  }
}

const handleUnregister = async (event) => {
  try {
    loading.value = true
    await axios.delete(`/events/${event.id}/register`)
    ElMessage.success('Successfully unregistered from event')
    fetchEvents()
  } catch (error) {
    ElMessage.error('Failed to unregister from event')
  } finally {
    loading.value = false
  }
}

const handleEdit = (event) => {
  editingEvent.value = event
  Object.assign(eventForm, event)
  showCreateDialog.value = true
}

const handleDelete = (event) => {
  editingEvent.value = event
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  try {
    loading.value = true
    await axios.delete(`/events/${editingEvent.value.id}`)
    ElMessage.success('Event deleted successfully')
    showDeleteDialog.value = false
    fetchEvents()
  } catch (error) {
    ElMessage.error('Failed to delete event')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  // Search is handled by computed property
}

onMounted(() => {
  fetchEvents()
})
</script>

<style scoped>
.events-container {
  padding: 20px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filters-section {
  margin-bottom: 30px;
}

.events-grid {
  margin-top: 20px;
}

.event-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.event-card:hover {
  transform: translateY(-5px);
}

.event-header {
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.event-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.event-content {
  padding: 15px;
}

.description {
  color: #606266;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta-info {
  font-size: 0.9rem;
  color: #909399;
}

.meta-info p {
  margin: 5px 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.event-actions {
  padding: 15px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}
</style> 