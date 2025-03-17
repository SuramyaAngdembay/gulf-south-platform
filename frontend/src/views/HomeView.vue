<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="hero-section">
          <h1>Welcome to Gulf South Scholars Hub</h1>
          <p class="subtitle">Connecting scholars and advancing research in the Gulf South region</p>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="feature-cards">
      <el-col :xs="24" :sm="12" :md="8">
        <el-card class="feature-card" @click="$router.push('/research')">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <h3>Research Projects</h3>
            </div>
          </template>
          <div class="card-content">
            <p>Explore ongoing research projects, collaborate with scholars, and share your findings.</p>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8">
        <el-card class="feature-card" @click="$router.push('/events')">
          <template #header>
            <div class="card-header">
              <el-icon><Calendar /></el-icon>
              <h3>Events & Conferences</h3>
            </div>
          </template>
          <div class="card-content">
            <p>Stay updated with upcoming events, conferences, and networking opportunities.</p>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8">
        <el-card class="feature-card" @click="$router.push('/resources')">
          <template #header>
            <div class="card-header">
              <el-icon><Collection /></el-icon>
              <h3>Resources</h3>
            </div>
          </template>
          <div class="card-content">
            <p>Access a curated collection of research materials, publications, and educational resources.</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="stats-section">
      <el-col :xs="24" :sm="12" :md="6">
        <div class="stat-card">
          <h2>{{ stats.projects || 0 }}</h2>
          <p>Active Projects</p>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="stat-card">
          <h2>{{ stats.events || 0 }}</h2>
          <p>Upcoming Events</p>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="stat-card">
          <h2>{{ stats.resources || 0 }}</h2>
          <p>Resources</p>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="stat-card">
          <h2>{{ stats.members || 0 }}</h2>
          <p>Active Members</p>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="cta-section">
      <el-col :span="24">
        <div class="cta-content">
          <h2>Join Our Community</h2>
          <p>Connect with scholars, share your research, and contribute to the study of the Gulf South region.</p>
          <el-button type="primary" size="large" @click="$router.push('/register')">
            Get Started
          </el-button>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Document, Calendar, Collection } from '@element-plus/icons-vue'
import axios from 'axios'

const stats = ref({
  projects: 0,
  events: 0,
  resources: 0,
  members: 0
})

const fetchStats = async () => {
  try {
    const response = await axios.get('/stats')
    stats.value = response.data
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #409EFF 0%, #2c3e50 100%);
  color: white;
  border-radius: 8px;
  margin-bottom: 40px;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.hero-section .subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
}

.feature-cards {
  margin-bottom: 40px;
}

.feature-card {
  cursor: pointer;
  transition: transform 0.3s;
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-header .el-icon {
  font-size: 24px;
  color: #409EFF;
}

.card-content {
  color: #606266;
}

.stats-section {
  margin-bottom: 40px;
}

.stat-card {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  height: 100%;
}

.stat-card h2 {
  font-size: 2rem;
  color: #409EFF;
  margin-bottom: 10px;
}

.stat-card p {
  color: #606266;
  margin: 0;
}

.cta-section {
  text-align: center;
  padding: 40px;
  background: #f5f7fa;
  border-radius: 8px;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-content h2 {
  margin-bottom: 20px;
}

.cta-content p {
  color: #606266;
  margin-bottom: 30px;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 40px 20px;
  }

  .hero-section h1 {
    font-size: 2rem;
  }

  .stat-card {
    margin-bottom: 20px;
  }
}
</style> 