<template>
  <div class="global-search">
    <el-popover
      v-model:visible="showSearch"
      placement="bottom"
      :width="600"
      trigger="click"
    >
      <template #reference>
        <el-button class="search-trigger" @click="showSearch = true">
          <el-icon><Search /></el-icon>
          <span>Search...</span>
        </el-button>
      </template>

      <div class="search-container">
        <!-- Search Input -->
        <el-input
          v-model="searchQuery"
          placeholder="Search across all content..."
          class="search-input"
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <!-- Quick Filters -->
        <div class="quick-filters">
          <el-radio-group v-model="contentType" size="small">
            <el-radio-button label="all">All</el-radio-button>
            <el-radio-button label="research">Research</el-radio-button>
            <el-radio-button label="events">Events</el-radio-button>
            <el-radio-button label="resources">Resources</el-radio-button>
          </el-radio-group>
        </div>

        <!-- Advanced Filters -->
        <div class="advanced-filters">
          <el-collapse>
            <el-collapse-item title="Advanced Filters">
              <el-form :model="filters" label-width="100px">
                <!-- Era Filter -->
                <el-form-item label="Era">
                  <el-select v-model="filters.era" multiple placeholder="Select eras">
                    <el-option label="Colonial" value="colonial" />
                    <el-option label="Antebellum" value="antebellum" />
                    <el-option label="Civil War" value="civil_war" />
                    <el-option label="Reconstruction" value="reconstruction" />
                    <el-option label="Modern" value="modern" />
                  </el-select>
                </el-form-item>

                <!-- Date Range -->
                <el-form-item label="Date Range">
                  <el-date-picker
                    v-model="filters.dateRange"
                    type="daterange"
                    range-separator="to"
                    start-placeholder="Start date"
                    end-placeholder="End date"
                  />
                </el-form-item>

                <!-- Resource Type -->
                <el-form-item label="Resource Type">
                  <el-select v-model="filters.resourceType" multiple placeholder="Select types">
                    <el-option label="Article" value="article" />
                    <el-option label="Book" value="book" />
                    <el-option label="Document" value="document" />
                    <el-option label="Video" value="video" />
                    <el-option label="Audio" value="audio" />
                  </el-select>
                </el-form-item>

                <!-- Status -->
                <el-form-item label="Status">
                  <el-select v-model="filters.status" multiple placeholder="Select status">
                    <el-option label="Active" value="active" />
                    <el-option label="Completed" value="completed" />
                    <el-option label="Upcoming" value="upcoming" />
                    <el-option label="Archived" value="archived" />
                  </el-select>
                </el-form-item>
              </el-form>
            </el-collapse-item>
          </el-collapse>
        </div>

        <!-- Search Results -->
        <div class="search-results" v-if="searchQuery">
          <div v-if="loading" class="loading-state">
            <el-skeleton :rows="3" animated />
          </div>
          <template v-else>
            <div v-if="results.length === 0" class="no-results">
              No results found
            </div>
            <div v-else class="results-list">
              <div
                v-for="result in results"
                :key="result.id"
                class="result-item"
                @click="handleResultClick(result)"
              >
                <div class="result-icon">
                  <el-icon>
                    <component :is="getResultIcon(result.type)" />
                  </el-icon>
                </div>
                <div class="result-content">
                  <h4>{{ result.title }}</h4>
                  <p>{{ result.description }}</p>
                  <div class="result-meta">
                    <el-tag size="small">{{ result.type }}</el-tag>
                    <span>{{ formatDate(result.date) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- Recent Searches -->
        <div v-else class="recent-searches">
          <h3>Recent Searches</h3>
          <div class="recent-list">
            <div
              v-for="search in recentSearches"
              :key="search.id"
              class="recent-item"
              @click="loadRecentSearch(search)"
            >
              <el-icon><Timer /></el-icon>
              <span>{{ search.query }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Search,
  Document,
  Calendar,
  Collection,
  Timer,
  VideoCamera,
  Headset,
  Reading
} from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const showSearch = ref(false)
const searchQuery = ref('')
const contentType = ref('all')
const loading = ref(false)
const results = ref([])
const recentSearches = ref([])

const filters = reactive({
  era: [],
  dateRange: [],
  resourceType: [],
  status: []
})

// Watch for filter changes
watch([() => filters.era, () => filters.dateRange, () => filters.resourceType, () => filters.status], () => {
  if (searchQuery.value) {
    handleSearch()
  }
})

const handleSearch = async () => {
  if (!searchQuery.value) {
    results.value = []
    return
  }

  try {
    loading.value = true
    const response = await axios.get('/api/search', {
      params: {
        q: searchQuery.value,
        type: contentType.value,
        ...filters
      }
    })
    results.value = response.data
  } catch (error) {
    ElMessage.error('Search failed')
  } finally {
    loading.value = false
  }
}

const handleResultClick = (result) => {
  showSearch.value = false
  router.push(`/${result.type}/${result.id}`)
}

const getResultIcon = (type) => {
  const icons = {
    research: Collection,
    event: Calendar,
    article: Document,
    book: Reading,
    video: VideoCamera,
    audio: Headset
  }
  return icons[type] || Document
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

const loadRecentSearch = (search) => {
  searchQuery.value = search.query
  handleSearch()
}

// Load recent searches from localStorage
onMounted(() => {
  const saved = localStorage.getItem('recentSearches')
  if (saved) {
    recentSearches.value = JSON.parse(saved)
  }
})

// Save recent searches to localStorage
watch(searchQuery, (newQuery) => {
  if (newQuery) {
    const search = {
      id: Date.now(),
      query: newQuery,
      timestamp: new Date().toISOString()
    }
    recentSearches.value.unshift(search)
    recentSearches.value = recentSearches.value.slice(0, 5)
    localStorage.setItem('recentSearches', JSON.stringify(recentSearches.value))
  }
})
</script>

<style scoped>
.global-search {
  display: inline-block;
}

.search-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-container {
  padding: 20px;
}

.search-input {
  margin-bottom: 15px;
}

.quick-filters {
  margin-bottom: 15px;
}

.advanced-filters {
  margin-bottom: 15px;
}

.search-results {
  max-height: 400px;
  overflow-y: auto;
}

.result-item {
  display: flex;
  gap: 15px;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.result-item:hover {
  background-color: #f5f7fa;
}

.result-icon {
  color: #409EFF;
  font-size: 1.2rem;
}

.result-content {
  flex: 1;
}

.result-content h4 {
  margin: 0 0 5px 0;
  font-size: 1rem;
}

.result-content p {
  margin: 0 0 5px 0;
  color: #606266;
  font-size: 0.9rem;
}

.result-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #909399;
  font-size: 0.8rem;
}

.recent-searches {
  padding: 10px 0;
}

.recent-searches h3 {
  margin: 0 0 10px 0;
  font-size: 0.9rem;
  color: #909399;
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  color: #606266;
  transition: background-color 0.3s;
}

.recent-item:hover {
  background-color: #f5f7fa;
}

.loading-state {
  padding: 20px;
}

.no-results {
  text-align: center;
  color: #909399;
  padding: 20px;
}
</style> 