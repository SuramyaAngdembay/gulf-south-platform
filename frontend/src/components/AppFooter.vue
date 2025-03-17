<template>
  <footer class="app-footer">
    <div class="footer-content">
      <!-- Main Footer Content -->
      <div class="footer-grid">
        <!-- About Section -->
        <div class="footer-section">
          <h3>About Gulf South Scholars Hub</h3>
          <p>A collaborative platform for researchers, scholars, and historians studying the Gulf South region's rich history and cultural heritage.</p>
          <div class="social-links">
            <a href="#" class="social-link" target="_blank" rel="noopener noreferrer">
              <el-icon><Twitter /></el-icon>
            </a>
            <a href="#" class="social-link" target="_blank" rel="noopener noreferrer">
              <el-icon><Facebook /></el-icon>
            </a>
            <a href="#" class="social-link" target="_blank" rel="noopener noreferrer">
              <el-icon><Linkedin /></el-icon>
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div class="footer-section">
          <h3>Quick Links</h3>
          <ul class="footer-links">
            <li><router-link to="/research">Research Projects</router-link></li>
            <li><router-link to="/events">Events & Conferences</router-link></li>
            <li><router-link to="/resources">Resources</router-link></li>
            <li><router-link to="/about">About Us</router-link></li>
          </ul>
        </div>

        <!-- Resources -->
        <div class="footer-section">
          <h3>Resources</h3>
          <ul class="footer-links">
            <li><router-link to="/resources/archives">Archives</router-link></li>
            <li><router-link to="/resources/publications">Publications</router-link></li>
            <li><router-link to="/resources/databases">Databases</router-link></li>
            <li><router-link to="/resources/guides">Research Guides</router-link></li>
          </ul>
        </div>

        <!-- Contact -->
        <div class="footer-section">
          <h3>Contact Us</h3>
          <ul class="footer-links">
            <li><el-icon><Message /></el-icon> contact@gulfsouthscholars.org</li>
            <li><el-icon><Location /></el-icon> New Orleans, LA</li>
            <li><el-icon><Phone /></el-icon> (504) 555-0123</li>
          </ul>
        </div>
      </div>

      <!-- Newsletter Signup -->
      <div class="newsletter-section">
        <h3>Stay Updated</h3>
        <p>Subscribe to our newsletter for the latest updates and research opportunities.</p>
        <el-form :model="newsletterForm" @submit.prevent="handleNewsletterSubmit">
          <el-input
            v-model="newsletterForm.email"
            placeholder="Enter your email"
            class="newsletter-input"
          >
            <template #append>
              <el-button type="primary" @click="handleNewsletterSubmit">
                Subscribe
              </el-button>
            </template>
          </el-input>
        </el-form>
      </div>

      <!-- Bottom Bar -->
      <div class="footer-bottom">
        <div class="copyright">
          © {{ new Date().getFullYear() }} Gulf South Scholars Hub. All rights reserved.
        </div>
        <div class="footer-legal">
          <router-link to="/privacy">Privacy Policy</router-link>
          <router-link to="/terms">Terms of Service</router-link>
          <router-link to="/accessibility">Accessibility</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Twitter,
  Facebook,
  Linkedin,
  Message,
  Location,
  Phone
} from '@element-plus/icons-vue'

const newsletterForm = reactive({
  email: ''
})

const handleNewsletterSubmit = async () => {
  try {
    // TODO: Implement newsletter subscription
    ElMessage.success('Thank you for subscribing to our newsletter!')
    newsletterForm.email = ''
  } catch (error) {
    ElMessage.error('Failed to subscribe. Please try again.')
  }
}
</script>

<style scoped>
.app-footer {
  background-color: #f5f7fa;
  padding: 60px 0 20px;
  margin-top: 60px;
  border-top: 1px solid #e4e7ed;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  margin-bottom: 40px;
}

.footer-section h3 {
  color: #303133;
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.footer-section p {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 20px;
}

.social-links {
  display: flex;
  gap: 15px;
}

.social-link {
  color: #409EFF;
  font-size: 1.2rem;
  transition: color 0.3s;
}

.social-link:hover {
  color: #66b1ff;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 12px;
}

.footer-links a {
  color: #606266;
  text-decoration: none;
  transition: color 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.footer-links a:hover {
  color: #409EFF;
}

.newsletter-section {
  text-align: center;
  padding: 40px 0;
  border-top: 1px solid #e4e7ed;
  border-bottom: 1px solid #e4e7ed;
  margin-bottom: 20px;
}

.newsletter-section h3 {
  color: #303133;
  margin-bottom: 10px;
}

.newsletter-section p {
  color: #606266;
  margin-bottom: 20px;
}

.newsletter-input {
  max-width: 500px;
  margin: 0 auto;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
}

.copyright {
  color: #909399;
  font-size: 0.9rem;
}

.footer-legal {
  display: flex;
  gap: 20px;
}

.footer-legal a {
  color: #909399;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s;
}

.footer-legal a:hover {
  color: #409EFF;
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .footer-legal {
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .footer-grid {
    grid-template-columns: 1fr;
  }

  .newsletter-input {
    width: 100%;
  }
}
</style> 