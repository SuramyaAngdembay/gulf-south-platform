<template>
  <div class="research-container">
    <div class="header-section">
      <h1>Research Projects</h1>
      <el-button type="primary" @click="showCreateDialog = true" v-if="isAuthenticated">
        Create Project
      </el-button>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchQuery"
            placeholder="Search projects..."
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
          <el-select v-model="statusFilter" placeholder="Filter by Status" clearable>
            <el-option label="Planning" value="planning" />
            <el-option label="In Progress" value="in_progress" />
            <el-option label="Completed" value="completed" />
            <el-option label="On Hold" value="on_hold" />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <!-- Projects List -->
    <el-row :gutter="20" class="projects-grid">
      <el-col v-for="project in filteredProjects" :key="project.id" :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="project-card" :body-style="{ padding: '0px' }">
          <div class="project-header">
            <h3>{{ project.title }}</h3>
            <el-tag :type="getStatusTag(project.status)">{{ project.status }}</el-tag>
          </div>
          <div class="project-content">
            <p class="description">{{ project.description }}</p>
            <div class="meta-info">
              <p><el-icon><User /></el-icon> {{ project.leadResearcher }}</p>
              <p><el-icon><Calendar /></el-icon> {{ formatDate(project.startDate) }}</p>
              <p><el-icon><Collection /></el-icon> {{ project.eraFocus }}</p>
            </div>
            <div class="researchers" v-if="project.researchers && project.researchers.length">
              <h4>Research Team</h4>
              <el-avatar-group>
                <el-avatar 
                  v-for="researcher in project.researchers" 
                  :key="researcher.id"
                  :size="32"
                  :src="researcher.avatar"
                >
                  {{ researcher.name.charAt(0) }}
                </el-avatar>
              </el-avatar-group>
            </div>
          </div>
          <div class="project-actions">
            <el-button-group>
              <el-button type="primary" @click="handleViewDetails(project)">View Details</el-button>
              <el-button 
                type="success" 
                @click="handleJoinProject(project)"
                v-if="isAuthenticated && !isProjectMember(project)"
              >
                Join Project
              </el-button>
              <el-button 
                type="warning" 
                @click="handleEdit(project)"
                v-if="isAuthenticated && (project.leadResearcher === currentUser?.id || isAdmin)"
              >
                Edit
              </el-button>
              <el-button 
                type="danger" 
                @click="handleDelete(project)"
                v-if="isAuthenticated && (project.leadResearcher === currentUser?.id || isAdmin)"
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
      :title="editingProject ? 'Edit Project' : 'Create New Project'"
      width="50%"
    >
      <el-form
        ref="formRef"
        :model="projectForm"
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="Title" prop="title">
          <el-input v-model="projectForm.title" placeholder="Project title" />
        </el-form-item>

        <el-form-item label="Description" prop="description">
          <el-input
            v-model="projectForm.description"
            type="textarea"
            :rows="4"
            placeholder="Project description"
          />
        </el-form-item>

        <el-form-item label="Status" prop="status">
          <el-select v-model="projectForm.status" placeholder="Select status">
            <el-option label="Planning" value="planning" />
            <el-option label="In Progress" value="in_progress" />
            <el-option label="Completed" value="completed" />
            <el-option label="On Hold" value="on_hold" />
          </el-select>
        </el-form-item>

        <el-form-item label="Start Date" prop="startDate">
          <el-date-picker
            v-model="projectForm.startDate"
            type="date"
            placeholder="Select start date"
          />
        </el-form-item>

        <el-form-item label="Expected End Date" prop="endDate">
          <el-date-picker
            v-model="projectForm.endDate"
            type="date"
            placeholder="Select expected end date"
          />
        </el-form-item>

        <el-form-item label="Era Focus" prop="eraFocus">
          <el-select v-model="projectForm.eraFocus" placeholder="Select era">
            <el-option label="Colonial" value="colonial" />
            <el-option label="Antebellum" value="antebellum" />
            <el-option label="Civil War" value="civil_war" />
            <el-option label="Reconstruction" value="reconstruction" />
            <el-option label="Modern" value="modern" />
          </el-select>
        </el-form-item>

        <el-form-item label="Research Team" prop="researchers">
          <el-select
            v-model="projectForm.researchers"
            multiple
            filterable
            remote
            :remote-method="searchResearchers"
            :loading="loadingResearchers"
            placeholder="Search and select researchers"
          >
            <el-option
              v-for="researcher in researcherOptions"
              :key="researcher.id"
              :label="researcher.name"
              :value="researcher.id"
            >
              <div class="researcher-option">
                <el-avatar :size="24" :src="researcher.avatar">
                  {{ researcher.name.charAt(0) }}
                </el-avatar>
                <span>{{ researcher.name }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">Cancel</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            {{ editingProject ? 'Update' : 'Create' }}
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
      <p>Are you sure you want to delete this project?</p>
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
import { ElMessage } from 'element-plus'
import { User, Calendar, Collection } from '@element-plus/icons-vue'
import axios from 'axios'

const store = useStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const loadingResearchers = ref(false)
const projects = ref([])
const showCreateDialog = ref(false)
const showDeleteDialog = ref(false)
const editingProject = ref(null)
const searchQuery = ref('')
const eraFilter = ref('')
const statusFilter = ref('')
const researcherOptions = ref([])

const projectForm = reactive({
  title: '',
  description: '',
  status: '',
  startDate: '',
  endDate: '',
  eraFocus: '',
  researchers: []
})

const rules = reactive<FormRules>({
  title: [
    { required: true, message: 'Please enter project title', trigger: 'blur' },
    { min: 3, message: 'Title must be at least 3 characters', trigger: 'blur' }
  ],
  description: [
    { required: true, message: 'Please enter project description', trigger: 'blur' },
    { min: 10, message: 'Description must be at least 10 characters', trigger: 'blur' }
  ],
  status: [
    { required: true, message: 'Please select project status', trigger: 'change' }
  ],
  startDate: [
    { required: true, message: 'Please select start date', trigger: 'change' }
  ],
  endDate: [
    { required: true, message: 'Please select expected end date', trigger: 'change' }
  ],
  eraFocus: [
    { required: true, message: 'Please select era focus', trigger: 'change' }
  ]
})

const isAuthenticated = computed(() => store.getters.isAuthenticated)
const currentUser = computed(() => store.getters.currentUser)
const isAdmin = computed(() => currentUser.value?.role === 'admin')

const filteredProjects = computed(() => {
  return projects.value.filter(project => {
    const matchesSearch = project.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         project.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesEra = !eraFilter.value || project.eraFocus === eraFilter.value
    const matchesStatus = !statusFilter.value || project.status === statusFilter.value
    return matchesSearch && matchesEra && matchesStatus
  })
})

const getStatusTag = (status: string) => {
  const types = {
    planning: 'info',
    in_progress: 'primary',
    completed: 'success',
    on_hold: 'warning'
  }
  return types[status] || 'info'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

const isProjectMember = (project) => {
  return project.researchers?.some(r => r.id === currentUser.value?.id)
}

const fetchProjects = async () => {
  try {
    loading.value = true
    const response = await axios.get('/research-projects')
    projects.value = response.data
  } catch (error) {
    ElMessage.error('Failed to fetch projects')
  } finally {
    loading.value = false
  }
}

const searchResearchers = async (query) => {
  if (query) {
    try {
      loadingResearchers.value = true
      const response = await axios.get(`/users/search?q=${query}`)
      researcherOptions.value = response.data
    } catch (error) {
      console.error('Failed to search researchers:', error)
    } finally {
      loadingResearchers.value = false
    }
  } else {
    researcherOptions.value = []
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    if (editingProject.value) {
      await axios.put(`/research-projects/${editingProject.value.id}`, projectForm)
      ElMessage.success('Project updated successfully')
    } else {
      await axios.post('/research-projects', projectForm)
      ElMessage.success('Project created successfully')
    }
    
    showCreateDialog.value = false
    fetchProjects()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || 'Operation failed')
  } finally {
    loading.value = false
  }
}

const handleViewDetails = (project) => {
  // Implement project details view
  console.log('View details:', project)
}

const handleJoinProject = async (project) => {
  try {
    loading.value = true
    await axios.post(`/research-projects/${project.id}/join`)
    ElMessage.success('Successfully joined project')
    fetchProjects()
  } catch (error) {
    ElMessage.error('Failed to join project')
  } finally {
    loading.value = false
  }
}

const handleEdit = (project) => {
  editingProject.value = project
  Object.assign(projectForm, project)
  showCreateDialog.value = true
}

const handleDelete = (project) => {
  editingProject.value = project
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  try {
    loading.value = true
    await axios.delete(`/research-projects/${editingProject.value.id}`)
    ElMessage.success('Project deleted successfully')
    showDeleteDialog.value = false
    fetchProjects()
  } catch (error) {
    ElMessage.error('Failed to delete project')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  // Search is handled by computed property
}

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.research-container {
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

.projects-grid {
  margin-top: 20px;
}

.project-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.project-card:hover {
  transform: translateY(-5px);
}

.project-header {
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.project-content {
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
  margin-bottom: 15px;
}

.meta-info p {
  margin: 5px 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.researchers {
  margin-bottom: 15px;
}

.researchers h4 {
  margin: 0 0 10px 0;
  font-size: 0.9rem;
  color: #606266;
}

.project-actions {
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

.researcher-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}
</style> 