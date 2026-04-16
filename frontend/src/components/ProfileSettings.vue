<script setup>
import { ref, onMounted, nextTick } from "vue"
import { useRouter } from 'vue-router'
import api from "@/api/axios"
import Navbar from "./Navbar.vue"
import ProfileTab from "./ProfileTab.vue"
import FavoritesTab from "./FavoritesTab.vue"
import ReviewsTab from "./ReviewsTab.vue"
import ModerationTab from "./ModerationTab.vue"

const router = useRouter()

// === SHARED STATE OWNED BY PARENT ===
const activeTab = ref("profile") // "profile" | "favorites" | "reviews" | "moderation"

// Profile is fetched here (once) so the tab nav can decide whether to show
// the moderation tab. ProfileTab receives it as a prop and emits updates.
const profile = ref({
  username: "",
  email: "",
  f_name: "",
  m_name: "",
  l_name: "",
  profile_picture_url: "",
  can_change_password: true,
  is_moderator: false,
  institution: "",
})

// Message banner — shared across tabs so any child can show feedback.
const message = ref("")
const messageType = ref("success")
const messageBannerRef = ref(null)

const showMessage = async ({ text, type = "success" }) => {
  message.value = text
  messageType.value = type

  await nextTick()

  if (messageBannerRef.value) {
    messageBannerRef.value.scrollIntoView({ behavior: "smooth", block: "start" })
  } else {
    window.scrollTo({ top: -100, behavior: "smooth" })
  }
}

const fetchProfile = async () => {
  try {
    const res = await api.get("me/")
    profile.value = res.data
  } catch (err) {
    console.error("GET /me failed:", err.response?.status, err.response?.data || err.message)
    showMessage({ text: "Failed to load profile.", type: "error" })
  }
}

onMounted(() => {
  fetchProfile()
})

const handleProfileUpdated = (updated) => {
  profile.value = { ...profile.value, ...updated }
}

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/')
}

const selectTab = (tab) => {
  // Defensive: never let a non-moderator land on the moderation tab,
  // even if this function were called programmatically.
  if (tab === 'moderation' && !profile.value.is_moderator) return
  activeTab.value = tab
}
</script>

<template>
  <div>
    <Navbar />

    <main class="profile-page">
      <!-- LEFT SIDEBAR : TAB NAVIGATION -->
      <aside class="profile-sidebar">
        <nav class="tab-nav" aria-label="Profile navigation">
          <button
            class="tab-btn"
            :class="{ 'tab-btn-active': activeTab === 'profile' }"
            @click="selectTab('profile')"
          >
            profile
          </button>

          <button
            class="tab-btn"
            :class="{ 'tab-btn-active': activeTab === 'favorites' }"
            @click="selectTab('favorites')"
          >
            favorites
          </button>

          <button
            class="tab-btn"
            :class="{ 'tab-btn-active': activeTab === 'reviews' }"
            @click="selectTab('reviews')"
          >
            reviews
          </button>

          <button
            v-if="profile.is_moderator"
            class="tab-btn"
            :class="{ 'tab-btn-active': activeTab === 'moderation' }"
            @click="selectTab('moderation')"
          >
            moderation
          </button>
        </nav>
      </aside>

      <!-- RIGHT CONTENT -->
      <section class="profile-content">
        <div
          v-if="message"
          ref="messageBannerRef"
          class="message-banner"
          :class="messageType === 'error' ? 'message-banner-error' : 'message-banner-success'"
        >
          {{ message }}
        </div>

        <ProfileTab
          v-if="activeTab === 'profile'"
          :profile="profile"
          @message="showMessage"
          @profile-updated="handleProfileUpdated"
          @logout="handleLogout"
        />

        <FavoritesTab
          v-else-if="activeTab === 'favorites'"
          @message="showMessage"
        />

        <ReviewsTab
          v-else-if="activeTab === 'reviews'"
          @message="showMessage"
        />

        <!-- Second guard on render: even if activeTab ends up here somehow,
             we only render when the user is actually a moderator. -->
        <ModerationTab
          v-else-if="activeTab === 'moderation' && profile.is_moderator"
          :profile="profile"
          @message="showMessage"
        />
      </section>
    </main>
  </div>
</template>

<style scoped>
.profile-page {
  display: flex;
  gap: 1.5rem;
  padding: 2rem;
  background: #f5f5f5;
  min-height: calc(100vh - 80px);
  align-items: flex-start;
}

.profile-sidebar {
  width: 220px;
  flex-shrink: 0;
}

.tab-nav {
  background: white;
  border-radius: 14px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
}

.tab-btn {
  border: 1px solid #d1d5db;
  background: #fff;
  color: #374151;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
  text-transform: lowercase;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}

.tab-btn:hover {
  background: #f3f4f6;
}

.tab-btn-active {
  background: #719294;
  color: white;
  border-color: #719294;
  box-shadow: inset 0 0 0 2px white;
}

.profile-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.message-banner {
  padding: 0.9rem 1rem;
  border-radius: 12px;
  font-weight: 600;
}

.message-banner-success {
  background: #e8f4e8;
  color: #2f6b2f;
  border: 1px solid #c6e2c6;
}

.message-banner-error {
  background: #fdeaea;
  color: #a12626;
  border: 1px solid #f2b8b8;
}

@media (max-width: 980px) {
  .profile-page {
    flex-direction: column;
  }

  .profile-sidebar {
    width: 100%;
  }

  .tab-nav {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .tab-btn {
    flex: 1 1 auto;
    text-align: center;
  }
}
</style>