<template>
  <div class="resources-container">
    <div class="header-section">
      <h1>Research Resources</h1>
      <el-button type="primary" @click="showCreateDialog = true" v-if="isAuthenticated">
        Add Resource
      </el-button>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchQuery"
            placeholder="Search resources..."
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
            <el-option label="Article" value="article" />
            <el-option label="Book" value="book" />
            <el-option label="Document" value="document" />
            <el-option label="Video" value="video" />
            <el-option label="Audio" value="audio" />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <!-- Resources List -->
    <el-row :gutter="20" class="resources-grid">
      <el-col v-for="resource in filteredResources" :key="resource.id" :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="resource-card" :body-style="{ padding: '0px' }">
          <div class="resource-header">
            <h3>{{ resource.title }}</h3>
            <el-tag :type="getResourceTypeTag(resource.type)">{{ resource.type }}</el-tag>
          </div>
          <div class="resource-content">
            <p class="description">{{ resource.description }}</p>
            <div class="meta-info">
              <p><el-icon><User /></el-icon> {{ resource.author }}</p>
              <p><el-icon><Calendar /></el-icon> {{ formatDate(resource.publishedDate) }}</p>
              <p><el-icon><Collection /></el-icon> {{ resource.eraFocus }}</p>
            </div>
            <div class="resource-links" v-if="resource.links && resource.links.length">
              <el-button 
                v-for="link in resource.links" 
                :key="link.url"
                type="primary" 
                link
                @click="openLink(link.url)"
              >
                {{ link.title }}
              </el-button>
            </div>
          </div>
          <div class="resource-actions">
            <el-button-group>
              <el-button 
                type="warning" 
                @click="handleEdit(resource)"
                v-if="isAuthenticated && (resource.author === currentUser?.id || isAdmin)"
              >
                Edit
              </el-button>
              <el-button 
                type="danger" 
                @click="handleDelete(resource)"
                v-if="isAuthenticated && (resource.author === currentUser?.id || isAdmin)"
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
      :title="editingResource ? 'Edit Resource' : 'Add New Resource'"
      width="50%"
    >
      <el-form
        ref="formRef"
        :model="resourceForm"
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="Title" prop="title">
          <el-input v-model="resourceForm.title" placeholder="Resource title" />
        </el-form-item>

        <el-form-item label="Description" prop="description">
          <el-input
            v-model="resourceForm.description"
            type="textarea"
            :rows="4"
            placeholder="Resource description"
          />
        </el-form-item>

        <el-form-item label="Type" prop="type">
          <el-select v-model="resourceForm.type" placeholder="Select resource type">
            <el-option label="Article" value="article" />
            <el-option label="Book" value="book" />
            <el-option label="Document" value="document" />
            <el-option label="Video" value="video" />
            <el-option label="Audio" value="audio" />
          </el-select>
        </el-form-item>

        <el-form-item label="Era Focus" prop="eraFocus">
          <el-select v-model="resourceForm.eraFocus" placeholder="Select era">
            <el-option label="Colonial" value="colonial" />
            <el-option label="Antebellum" value="antebellum" />
            <el-option label="Civil War" value="civil_war" />
            <el-option label="Reconstruction" value="reconstruction" />
            <el-option label="Modern" value="modern" />
          </el-select>
        </el-form-item>

        <el-form-item label="Published Date" prop="publishedDate">
          <el-date-picker
            v-model="resourceForm.publishedDate"
            type="date"
            placeholder="Select date"
          />
        </el-form-item>

        <el-form-item label="Links" prop="links">
          <div v-for="(link, index) in resourceForm.links" :key="index" class="link-item">
            <el-row :gutter="10">
              <el-col :span="10">
                <el-input v-model="link.title" placeholder="Link title" />
              </el-col>
              <el-col :span="12">
                <el-input v-model="link.url" placeholder="URL" />
              </el-col>
              <el-col :span="2">
                <el-button type="danger" circle @click="removeLink(index)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </el-col>
            </el-row>
          </div>
          <el-button type="primary" @click="addLink">Add Link</el-button>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">Cancel</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            {{ editingResource ? 'Update' : 'Create' }}
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
      <p>Are you sure you want to delete this resource?</p>
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
import { User, Calendar, Collection, Delete } from '@element-plus/icons-vue'
import axios from 'axios'

const store = useStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const resources = ref([])
const showCreateDialog = ref(false)
const showDeleteDialog = ref(false)
const editingResource = ref(null)
const searchQuery = ref('')
const eraFilter = ref('')
const typeFilter = ref('')

const resourceForm = reactive({
  title: '',
  description: '',
  type: '',
  eraFocus: '',
  publishedDate: '',
  links: []
})

const rules = reactive<FormRules>({
  title: [
    { required: true, message: 'Please enter resource title', trigger: 'blur' },
    { min: 3, message: 'Title must be at least 3 characters', trigger: 'blur' }
  ],
  description: [
    { required: true, message: 'Please enter resource description', trigger: 'blur' },
    { min: 10, message: 'Description must be at least 10 characters', trigger: 'blur' }
  ],
  type: [
    { required: true, message: 'Please select resource type', trigger: 'change' }
  ],
  eraFocus: [
    { required: true, message: 'Please select era focus', trigger: 'change' }
  ],
  publishedDate: [
    { required: true, message: 'Please select published date', trigger: 'change' }
  ]
})

const isAuthenticated = computed(() => store.getters.isAuthenticated)
const currentUser = computed(() => store.getters.currentUser)
const isAdmin = computed(() => currentUser.value?.role === 'admin')

const filteredResources = computed(() => {
  return resources.value.filter(resource => {
    const matchesSearch = resource.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         resource.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesEra = !eraFilter.value || resource.eraFocus === eraFilter.value
    const matchesType = !typeFilter.value || resource.type === typeFilter.value
    return matchesSearch && matchesEra && matchesType
  })
})

const getResourceTypeTag = (type: string) => {
  const types = {
    article: 'primary',
    book: 'success',
    document: 'warning',
    video: 'info',
    audio: 'danger'
  }
  return types[type] || 'info'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

const fetchResources = async () => {
  try {
    loading.value = true
    const response = await axios.get('/resources')
    resources.value = response.data
  } catch (error) {
    ElMessage.error('Failed to fetch resources')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    if (editingResource.value) {
      await axios.put(`/resources/${editingResource.value.id}`, resourceForm)
      ElMessage.success('Resource updated successfully')
    } else {
      await axios.post('/resources', resourceForm)
      ElMessage.success('Resource created successfully')
    }
    
    showCreateDialog.value = false
    fetchResources()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || 'Operation failed')
  } finally {
    loading.value = false
  }
}

const handleEdit = (resource) => {
  editingResource.value = resource
  Object.assign(resourceForm, resource)
  showCreateDialog.value = true
}

const handleDelete = (resource) => {
  editingResource.value = resource
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  try {
    loading.value = true
    await axios.delete(`/resources/${editingResource.value.id}`)
    ElMessage.success('Resource deleted successfully')
    showDeleteDialog.value = false
    fetchResources()
  } catch (error) {
    ElMessage.error('Failed to delete resource')
  } finally {
    loading.value = false
  }
}

const addLink = () => {
  resourceForm.links.push({ title: '', url: '' })
}

const removeLink = (index) => {
  resourceForm.links.splice(index, 1)
}

const openLink = (url) => {
  window.open(url, '_blank')
}

const handleSearch = () => {
  // Search is handled by computed property
}

onMounted(() => {
  fetchResources()
})
</script>

<style scoped>
.resources-container {
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

.resources-grid {
  margin-top: 20px;
}

.resource-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.resource-card:hover {
  transform: translateY(-5px);
}

.resource-header {
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resource-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.resource-content {
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

.resource-links {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 15px;
}

.resource-actions {
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

.link-item {
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}
</style> 