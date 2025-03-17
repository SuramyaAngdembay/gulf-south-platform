<template>
  <div class="profile-container">
    <!-- Profile Header -->
    <div class="profile-header">
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="profile-avatar">
            <el-avatar :size="150" :src="profile.avatar">
              {{ profile.name?.charAt(0) }}
            </el-avatar>
            <el-upload
              v-if="isOwnProfile"
              class="avatar-uploader"
              action="/api/upload"
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
            >
              <el-button type="primary" size="small">Change Photo</el-button>
            </el-upload>
          </div>
        </el-col>
        <el-col :span="16">
          <div class="profile-info">
            <div class="profile-title">
              <h1>{{ profile.name }}</h1>
              <el-tag v-if="profile.role === 'admin'" type="danger">Admin</el-tag>
            </div>
            <p class="profile-title">{{ profile.title }}</p>
            <p class="profile-institution">{{ profile.institution }}</p>
            <div class="profile-stats">
              <div class="stat-item">
                <h3>{{ profile.projects?.length || 0 }}</h3>
                <p>Projects</p>
              </div>
              <div class="stat-item">
                <h3>{{ profile.publications?.length || 0 }}</h3>
                <p>Publications</p>
              </div>
              <div class="stat-item">
                <h3>{{ profile.events?.length || 0 }}</h3>
                <p>Events</p>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- Profile Content -->
    <el-row :gutter="20" class="profile-content">
      <el-col :span="16">
        <!-- About Section -->
        <el-card class="profile-section">
          <template #header>
            <div class="section-header">
              <h2>About</h2>
              <el-button 
                v-if="isOwnProfile"
                type="primary" 
                link
                @click="showEditAbout = true"
              >
                Edit
              </el-button>
            </div>
          </template>
          <div class="about-content">
            <p>{{ profile.bio || 'No bio available.' }}</p>
            <div class="research-interests">
              <h3>Research Interests</h3>
              <el-tag-group>
                <el-tag 
                  v-for="interest in profile.researchInterests" 
                  :key="interest"
                  class="interest-tag"
                >
                  {{ interest }}
                </el-tag>
              </el-tag-group>
            </div>
          </div>
        </el-card>

        <!-- Projects Section -->
        <el-card class="profile-section">
          <template #header>
            <div class="section-header">
              <h2>Research Projects</h2>
              <el-button 
                v-if="isOwnProfile"
                type="primary" 
                link
                @click="$router.push('/research')"
              >
                Add Project
              </el-button>
            </div>
          </template>
          <div class="projects-list">
            <el-empty v-if="!profile.projects?.length" description="No projects yet" />
            <div v-else v-for="project in profile.projects" :key="project.id" class="project-item">
              <h3>{{ project.title }}</h3>
              <p>{{ project.description }}</p>
              <div class="project-meta">
                <el-tag size="small">{{ project.status }}</el-tag>
                <span>{{ project.eraFocus }}</span>
              </div>
            </div>
          </div>
        </el-card>

        <!-- Publications Section -->
        <el-card class="profile-section">
          <template #header>
            <div class="section-header">
              <h2>Publications</h2>
              <el-button 
                v-if="isOwnProfile"
                type="primary" 
                link
                @click="showAddPublication = true"
              >
                Add Publication
              </el-button>
            </div>
          </template>
          <div class="publications-list">
            <el-empty v-if="!profile.publications?.length" description="No publications yet" />
            <div v-else v-for="pub in profile.publications" :key="pub.id" class="publication-item">
              <h3>{{ pub.title }}</h3>
              <p>{{ pub.authors }}</p>
              <p class="publication-meta">
                {{ pub.journal }}, {{ pub.year }}
                <el-button 
                  v-if="pub.url"
                  type="primary" 
                  link
                  @click="openLink(pub.url)"
                >
                  View
                </el-button>
              </p>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <!-- Contact Information -->
        <el-card class="profile-section">
          <template #header>
            <div class="section-header">
              <h2>Contact Information</h2>
              <el-button 
                v-if="isOwnProfile"
                type="primary" 
                link
                @click="showEditContact = true"
              >
                Edit
              </el-button>
            </div>
          </template>
          <div class="contact-info">
            <p><el-icon><Message /></el-icon> {{ profile.email }}</p>
            <p v-if="profile.phone"><el-icon><Phone /></el-icon> {{ profile.phone }}</p>
            <p v-if="profile.website">
              <el-icon><Link /></el-icon>
              <el-button type="primary" link @click="openLink(profile.website)">
                {{ profile.website }}
              </el-button>
            </p>
            <p v-if="profile.location"><el-icon><Location /></el-icon> {{ profile.location }}</p>
          </div>
        </el-card>

        <!-- Upcoming Events -->
        <el-card class="profile-section">
          <template #header>
            <div class="section-header">
              <h2>Upcoming Events</h2>
              <el-button 
                v-if="isOwnProfile"
                type="primary" 
                link
                @click="$router.push('/events')"
              >
                View All
              </el-button>
            </div>
          </template>
          <div class="events-list">
            <el-empty v-if="!profile.events?.length" description="No upcoming events" />
            <div v-else v-for="event in profile.events" :key="event.id" class="event-item">
              <h3>{{ event.title }}</h3>
              <p>{{ formatDate(event.date) }}</p>
              <el-tag size="small">{{ event.type }}</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Edit About Dialog -->
    <el-dialog
      v-model="showEditAbout"
      title="Edit About"
      width="50%"
    >
      <el-form
        ref="aboutFormRef"
        :model="aboutForm"
        :rules="aboutRules"
        label-position="top"
      >
        <el-form-item label="Bio" prop="bio">
          <el-input
            v-model="aboutForm.bio"
            type="textarea"
            :rows="4"
            placeholder="Write a brief bio"
          />
        </el-form-item>
        <el-form-item label="Research Interests" prop="researchInterests">
          <el-select
            v-model="aboutForm.researchInterests"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="Select or create research interests"
          >
            <el-option
              v-for="interest in commonInterests"
              :key="interest"
              :label="interest"
              :value="interest"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditAbout = false">Cancel</el-button>
          <el-button type="primary" @click="handleUpdateAbout" :loading="loading">
            Save Changes
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Edit Contact Dialog -->
    <el-dialog
      v-model="showEditContact"
      title="Edit Contact Information"
      width="50%"
    >
      <el-form
        ref="contactFormRef"
        :model="contactForm"
        :rules="contactRules"
        label-position="top"
      >
        <el-form-item label="Email" prop="email">
          <el-input v-model="contactForm.email" type="email" />
        </el-form-item>
        <el-form-item label="Phone" prop="phone">
          <el-input v-model="contactForm.phone" />
        </el-form-item>
        <el-form-item label="Website" prop="website">
          <el-input v-model="contactForm.website" />
        </el-form-item>
        <el-form-item label="Location" prop="location">
          <el-input v-model="contactForm.location" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditContact = false">Cancel</el-button>
          <el-button type="primary" @click="handleUpdateContact" :loading="loading">
            Save Changes
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Add Publication Dialog -->
    <el-dialog
      v-model="showAddPublication"
      title="Add Publication"
      width="50%"
    >
      <el-form
        ref="publicationFormRef"
        :model="publicationForm"
        :rules="publicationRules"
        label-position="top"
      >
        <el-form-item label="Title" prop="title">
          <el-input v-model="publicationForm.title" />
        </el-form-item>
        <el-form-item label="Authors" prop="authors">
          <el-input v-model="publicationForm.authors" />
        </el-form-item>
        <el-form-item label="Journal" prop="journal">
          <el-input v-model="publicationForm.journal" />
        </el-form-item>
        <el-form-item label="Year" prop="year">
          <el-input v-model="publicationForm.year" type="number" />
        </el-form-item>
        <el-form-item label="URL" prop="url">
          <el-input v-model="publicationForm.url" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddPublication = false">Cancel</el-button>
          <el-button type="primary" @click="handleAddPublication" :loading="loading">
            Add Publication
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { Message, Phone, Link, Location } from '@element-plus/icons-vue'
import axios from 'axios'

const store = useStore()
const route = useRoute()
const loading = ref(false)
const profile = ref({})
const showEditAbout = ref(false)
const showEditContact = ref(false)
const showAddPublication = ref(false)

const aboutFormRef = ref<FormInstance>()
const contactFormRef = ref<FormInstance>()
const publicationFormRef = ref<FormInstance>()

const aboutForm = reactive({
  bio: '',
  researchInterests: []
})

const contactForm = reactive({
  email: '',
  phone: '',
  website: '',
  location: ''
})

const publicationForm = reactive({
  title: '',
  authors: '',
  journal: '',
  year: '',
  url: ''
})

const commonInterests = [
  'Colonial History',
  'Antebellum Period',
  'Civil War',
  'Reconstruction',
  'Modern History',
  'Social History',
  'Cultural History',
  'Economic History',
  'Political History',
  'Military History'
]

const aboutRules = reactive<FormRules>({
  bio: [
    { required: true, message: 'Please enter your bio', trigger: 'blur' },
    { min: 50, message: 'Bio must be at least 50 characters', trigger: 'blur' }
  ],
  researchInterests: [
    { required: true, message: 'Please select at least one research interest', trigger: 'change' }
  ]
})

const contactRules = reactive<FormRules>({
  email: [
    { required: true, message: 'Please enter your email', trigger: 'blur' },
    { type: 'email', message: 'Please enter a valid email address', trigger: 'blur' }
  ],
  website: [
    { type: 'url', message: 'Please enter a valid URL', trigger: 'blur' }
  ]
})

const publicationRules = reactive<FormRules>({
  title: [
    { required: true, message: 'Please enter publication title', trigger: 'blur' }
  ],
  authors: [
    { required: true, message: 'Please enter authors', trigger: 'blur' }
  ],
  journal: [
    { required: true, message: 'Please enter journal name', trigger: 'blur' }
  ],
  year: [
    { required: true, message: 'Please enter publication year', trigger: 'blur' },
    { type: 'number', message: 'Year must be a number', trigger: 'blur' }
  ],
  url: [
    { type: 'url', message: 'Please enter a valid URL', trigger: 'blur' }
  ]
})

const currentUser = computed(() => store.getters.currentUser)
const isOwnProfile = computed(() => {
  const profileId = route.params.id
  return profileId === currentUser.value?.id
})

const fetchProfile = async () => {
  try {
    loading.value = true
    const profileId = route.params.id
    const response = await axios.get(`/member-profiles/${profileId}`)
    profile.value = response.data
    Object.assign(aboutForm, {
      bio: response.data.bio,
      researchInterests: response.data.researchInterests
    })
    Object.assign(contactForm, {
      email: response.data.email,
      phone: response.data.phone,
      website: response.data.website,
      location: response.data.location
    })
  } catch (error) {
    ElMessage.error('Failed to fetch profile')
  } finally {
    loading.value = false
  }
}

const handleAvatarSuccess = (response) => {
  profile.value.avatar = response.url
  ElMessage.success('Avatar updated successfully')
}

const beforeAvatarUpload = (file) => {
  const isJPG = file.type === 'image/jpeg'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('Avatar picture must be JPG format!')
  }
  if (!isLt2M) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
  }
  return isJPG && isLt2M
}

const handleUpdateAbout = async () => {
  if (!aboutFormRef.value) return
  
  try {
    await aboutFormRef.value.validate()
    loading.value = true
    
    await axios.put(`/member-profiles/${profile.value.id}/about`, aboutForm)
    ElMessage.success('Profile updated successfully')
    showEditAbout.value = false
    fetchProfile()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || 'Operation failed')
  } finally {
    loading.value = false
  }
}

const handleUpdateContact = async () => {
  if (!contactFormRef.value) return
  
  try {
    await contactFormRef.value.validate()
    loading.value = true
    
    await axios.put(`/member-profiles/${profile.value.id}/contact`, contactForm)
    ElMessage.success('Contact information updated successfully')
    showEditContact.value = false
    fetchProfile()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || 'Operation failed')
  } finally {
    loading.value = false
  }
}

const handleAddPublication = async () => {
  if (!publicationFormRef.value) return
  
  try {
    await publicationFormRef.value.validate()
    loading.value = true
    
    await axios.post(`/member-profiles/${profile.value.id}/publications`, publicationForm)
    ElMessage.success('Publication added successfully')
    showAddPublication.value = false
    fetchProfile()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || 'Operation failed')
  } finally {
    loading.value = false
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

const openLink = (url: string) => {
  window.open(url, '_blank')
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-header {
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.profile-avatar {
  text-align: center;
}

.profile-avatar .el-avatar {
  margin-bottom: 15px;
}

.profile-info {
  padding: 20px 0;
}

.profile-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.profile-title h1 {
  margin: 0;
}

.profile-title p {
  margin: 0;
  color: #606266;
}

.profile-institution {
  color: #909399;
  margin-bottom: 20px;
}

.profile-stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.stat-item h3 {
  margin: 0;
  font-size: 24px;
  color: #409EFF;
}

.stat-item p {
  margin: 5px 0 0 0;
  color: #909399;
}

.profile-content {
  margin-top: 20px;
}

.profile-section {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h2 {
  margin: 0;
  font-size: 1.2rem;
}

.about-content {
  color: #606266;
}

.research-interests {
  margin-top: 20px;
}

.interest-tag {
  margin: 5px;
}

.contact-info p {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
  color: #606266;
}

.project-item, .publication-item, .event-item {
  padding: 15px 0;
  border-bottom: 1px solid #ebeef5;
}

.project-item:last-child, .publication-item:last-child, .event-item:last-child {
  border-bottom: none;
}

.project-item h3, .publication-item h3, .event-item h3 {
  margin: 0 0 10px 0;
  font-size: 1.1rem;
}

.project-meta, .publication-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #909399;
  font-size: 0.9rem;
}

.publication-item p {
  margin: 5px 0;
  color: #606266;
}

@media (max-width: 768px) {
  .profile-header {
    padding: 20px;
  }

  .profile-stats {
    flex-direction: column;
    gap: 15px;
  }

  .profile-content {
    margin-top: 10px;
  }
}
</style> 