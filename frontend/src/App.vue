<template>
  <el-container class="app-container">
    <el-header>
      <nav class="nav-menu">
        <router-link to="/" class="logo">Gulf South Scholars Hub</router-link>
        <div class="nav-links">
          <router-link to="/research">Research</router-link>
          <router-link to="/events">Events</router-link>
          <router-link to="/resources">Resources</router-link>
          <template v-if="isAuthenticated">
            <router-link to="/profile">Profile</router-link>
            <el-button @click="handleLogout" type="text">Logout</el-button>
          </template>
          <template v-else>
            <router-link to="/login">Login</router-link>
            <router-link to="/register">Register</router-link>
          </template>
        </div>
      </nav>
    </el-header>

    <el-main>
      <el-alert
        v-if="error"
        :title="error"
        type="error"
        show-icon
        @close="clearError"
      />
      
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <el-footer>
      <p>&copy; {{ new Date().getFullYear() }} Gulf South Scholars Hub. All rights reserved.</p>
    </el-footer>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const store = useStore()
const router = useRouter()

const isAuthenticated = computed(() => store.getters.isAuthenticated)
const error = computed(() => store.getters.error)

const handleLogout = async () => {
  try {
    await store.dispatch('logout')
    router.push('/login')
    ElMessage.success('Logged out successfully')
  } catch (err) {
    ElMessage.error('Failed to logout')
  }
}

const clearError = () => {
  store.commit('setError', null)
}
</script>

<style>
.app-container {
  min-height: 100vh;
}

.nav-menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 100%;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: #409EFF;
}

.nav-links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-links a {
  text-decoration: none;
  color: #606266;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #409EFF;
}

.nav-links a.router-link-active {
  color: #409EFF;
}

.el-main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.el-footer {
  text-align: center;
  padding: 20px;
  color: #909399;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
