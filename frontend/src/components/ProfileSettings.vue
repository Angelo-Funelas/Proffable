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

// === STYLE TOKENS ===
const tabClass = (isActive) => [
  'px-4 py-3 rounded-xl text-sm font-semibold text-left cursor-pointer lowercase transition-all max-[980px]:flex-1 max-[980px]:text-center',
  isActive
    ? 'bg-primary text-white border border-primary shadow-md'
    : 'bg-card text-text-main border border-gray-100 hover:bg-surface',
]
</script>

<template>
  <div>
    <Navbar />

    <main
      class="flex gap-6 p-8 bg-surface min-h-[calc(100vh-80px)] items-start max-[980px]:flex-col"
    >
      <!-- LEFT SIDEBAR : TAB NAVIGATION -->
      <aside class="w-[220px] shrink-0 max-[980px]:w-full">
        <nav
          class="bg-card rounded-[24px] p-3 flex flex-col gap-2 shadow-xl border border-gray-100 max-[980px]:flex-row max-[980px]:flex-wrap"
          aria-label="Profile navigation"
        >
          <button
            :class="tabClass(activeTab === 'profile')"
            @click="selectTab('profile')"
          >
            profile
          </button>

          <button
            :class="tabClass(activeTab === 'favorites')"
            @click="selectTab('favorites')"
          >
            favorites
          </button>

          <button
            :class="tabClass(activeTab === 'reviews')"
            @click="selectTab('reviews')"
          >
            reviews
          </button>

          <button
            v-if="profile.is_moderator"
            :class="tabClass(activeTab === 'moderation')"
            @click="selectTab('moderation')"
          >
            moderation
          </button>
        </nav>
      </aside>

      <!-- RIGHT CONTENT -->
      <section class="flex-1 min-w-0 flex flex-col gap-6">
        <div
          v-if="message"
          ref="messageBannerRef"
          class="px-4 py-3 rounded-xl font-semibold border"
          :class="
            messageType === 'error'
              ? 'bg-red-50 text-red-700 border-red-200'
              : 'bg-emerald-50 text-emerald-700 border-emerald-200'
          "
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