<script setup>
import { ref, computed, onMounted, nextTick} from "vue"
import { useRouter } from 'vue-router'
import api from "@/api/axios"
import Navbar from "./Navbar.vue"

// Routing logic 
const router = useRouter()

// similar logic to logging out in Navbar.vue 

const logout = () => {
    localStorage.removeItem('access_token') 
    localStorage.removeItem('refresh_token')
    router.push('/')
}


// === USER INFORMATION FUNCTIONS === 

// Align with GET /me request 
const profile = ref({
  username: "",
  email: "",
  f_name: "",
  m_name: "",
  l_name: "",
  profile_picture_url: "",
  can_change_password: true, 
})

// TODO: Replace with GET /me/reviews/ THIS IS FILLER DATA. 
const userReviews = ref([
  {
    review_id: 1,
    professor_name: "Dr. Maria Santos",
    review_rating: 5,
    comment_text: "Very clear lectures and fair grading. One of the best professors I’ve had.",
    review_date: "2026-04-01",
    received_grade: "A",
    helpful_count: 12,
  },
  {
    review_id: 2,
    professor_name: "Prof. Juan Dela Cruz",
    review_rating: 4,
    comment_text: "Workload was heavy, but I learned a lot. Class discussions were very engaging.",
    review_date: "2026-03-20",
    received_grade: "B+",
    helpful_count: 7,
  },
])

// TODO: Replace with GET /me/favorites/ THIS IS FILLER DATA
const favoriteProfessors = ref([
  {
    professor_id: 1,
    f_name: "Ana",
    m_name: "R.",
    l_name: "Reyes",
    email: "ana.reyes@school.edu",
  },
  {
    professor_id: 2,
    f_name: "Miguel",
    m_name: "",
    l_name: "Torres",
    email: "miguel.torres@school.edu",
  },
])

// === UI STATE ===
const message = ref("")
const messageType = ref("success") // "success" or "error"
const messageBannerRef = ref(null)
const activePanel = ref(null)

const togglePanel = (panelName) => {
  activePanel.value = activePanel.value === panelName ? null : panelName
}

// Separate editable form so the mock profile card stays clean
const editForm = ref({
  username: "",
  email: "",
  f_name: "",
  m_name: "",
  l_name: "",
})

const passwordForm = ref({
  current_password: "",
  new_password: "",
  confirm_password: "",
})

const fullName = computed(() => {
  return [
    profile.value.f_name,
    profile.value.m_name,
    profile.value.l_name,
  ]
    .filter(Boolean)
    .join(" ")
})

const fetchProfile = async () => {
  try {
    const res = await api.get("me/")
    console.log("GET /me success:", res.data)
    profile.value = res.data
  } catch (err) {
    console.error("GET /me failed:", err.response?.status, err.response?.data || err.message)
    showMessage("Failed to load profile.", "error")
  }
}

// Updated logic for handling showing the message for filling out forms 
const showMessage = async (text, type = "success") => {
  message.value = text
  messageType.value = type

  await nextTick()

  if (messageBannerRef.value) {
    messageBannerRef.value.scrollIntoView({
      behavior: "smooth",
      block: "start",
    })
  } else {
    window.scrollTo({ top: -100, behavior: "smooth" })
  }
}

onMounted(() => {
  fetchProfile()
})

// TODO: Later, align with PATCH request in user information 
const chooseAvatar = async () => {
  if (!profile.value.profile_picture_url?.trim()) {
    showMessage("No profile picture URL provided.", "error")
    return
  }

  try {
    const res = await api.patch("me/update/", {
      profile_picture_url: profile.value.profile_picture_url.trim(),
    })

    profile.value = {
      ...profile.value,
      ...res.data,
    }

    showMessage("Profile picture updated successfully.", "success")
  } catch (err) {
    console.error("PATCH /me/update avatar failed:", err.response?.data || err.message)
    showMessage("Failed to update profile picture.", "error")
  }
}

const saveProfile = async () => {
  try {
    const payload = {}

    if (editForm.value.username.trim()) payload.username = editForm.value.username.trim()
    if (editForm.value.email.trim()) payload.email = editForm.value.email.trim()
    if (editForm.value.f_name.trim()) payload.f_name = editForm.value.f_name.trim()
    if (editForm.value.m_name.trim()) payload.m_name = editForm.value.m_name.trim()
    if (editForm.value.l_name.trim()) payload.l_name = editForm.value.l_name.trim()

    if (Object.keys(payload).length === 0) {
      showMessage("No changes to save", "error")
      return
    }

    const res = await api.patch("me/update/", payload)
    profile.value = {
      ...profile.value,
      ...res.data,
    }

    showMessage("Profile updated successfully.", "success")
    activePanel.value = null

    editForm.value = {
      username: "",
      email: "",
      f_name: "",
      m_name: "",
      l_name: "",
    }
  } catch (err) {
    console.error("PATCH /me/update failed:", err.response?.data || err.message)
    showMessage("Failed to update profile.", "error") 
  }
}

const changePassword = async () => {
  if (
    !passwordForm.value.current_password ||
    !passwordForm.value.new_password ||
    !passwordForm.value.confirm_password
  ) {
    showMessage("Please fill in all password fields.", "error")
    return
  }

  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    showMessage("New password and confirm password do not match.", "error")
    return
  }

  try {
    await api.patch("me/update/", {
      current_password: passwordForm.value.current_password,
      password: passwordForm.value.new_password,
    })

    showMessage("Password updated successfully.", "success")
    activePanel.value = null

    passwordForm.value = {
      current_password: "",
      new_password: "",
      confirm_password: "",
    }
  } catch (err) {
    console.error("PATCH /me/update password failed:", err.response?.data || err.message)
    showMessage(
      err.response?.data?.error ||
      err.response?.data?.current_password?.[0] ||
      "Failed to update password.", 
      "error"
    )
  }
}

const deleteAccount = () => {
  // TODO: Replace with backend delete account endpoint
  showMessage("Deleted account.", "success")
}

const removeFavorite = (professorId) => {
  // TODO: Replace with DELETE /me/favorites/:id or equivalent endpoint
  favoriteProfessors.value = favoriteProfessors.value.filter(
    (prof) => prof.professor_id !== professorId
  )
  showMessage("Mock favorite professor removed.", "success")
}

const deleteReview = (reviewId) => {
  // TODO: Replace with DELETE /reviews/:id
  userReviews.value = userReviews.value.filter(
    (review) => review.review_id !== reviewId
  )
  showMessage("Mock review deleted.", "success")
}

const getInitials = (firstName, lastName) => {
  const first = firstName ? firstName[0] : ""
  const last = lastName ? lastName[0] : ""
  return `${first}${last}`.toUpperCase()
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

</script>

<template>
  <div>
    <Navbar />

    <main class="profile-page">
      <!-- LEFT SIDEBAR -->
      <aside class="profile-sidebar">
        <div class="profile-card">
          <div class="avatar-wrapper">
            <img
              v-if="profile.profile_picture_url"
              :src="profile.profile_picture_url"
              alt="Profile picture"
              class="avatar-image"
            />
            <div v-else class="avatar-placeholder">
              {{ getInitials(profile.f_name, profile.l_name) }}
            </div>
          </div>

          <h2 class="profile-name">{{ fullName || "User Name" }}</h2>
          <p class="profile-username">Username: @{{ profile.username }}</p>
          <p class="profile-email">Email: {{ profile.email }}</p>

          <div class="sidebar-actions">
            <button class="sidebar-btn" @click="chooseAvatar">
              Choose Avatar
            </button>

            <button class="sidebar-btn" @click="togglePanel('editProfile')">
                {{ activePanel === 'editProfile' ? "Close Edit Profile" : "Edit Profile" }}
            </button>

            <button v-if="profile.can_change_password" class="sidebar-btn" @click="togglePanel('changePassword')">
                {{ activePanel === 'changePassword' ? "Close Password Form" : "Change Password" }}
            </button>

            <button class="sidebar-btn danger-btn" @click="deleteAccount">
              Delete Account
            </button>
          </div>
        </div>

        <!-- EDIT PROFILE FORM -->
        <div v-if="activePanel === 'editProfile'" class="panel-card">
          <h3>Edit Profile</h3>

          <label>First Name</label>
          <input v-model="editForm.f_name" type="text" />

          <label>Middle Name</label>
          <input v-model="editForm.m_name" type="text" />

          <label>Last Name</label>
          <input v-model="editForm.l_name" type="text" />

          <label>Username</label>
          <input v-model="editForm.username" type="text" />

          <label>Email</label>
          <input v-model="editForm.email" type="email" />

          <button class="primary-btn" @click="saveProfile">Save Profile</button>
        </div>

        <!-- CHANGE PASSWORD FORM -->
        <div v-if="activePanel === 'changePassword'" class="panel-card">
          <h3>Change Password</h3>

          <label>Current Password</label>
          <input v-model="passwordForm.current_password" type="password" />

          <label>New Password</label>
          <input v-model="passwordForm.new_password" type="password" />

          <label>Confirm New Password</label>
          <input v-model="passwordForm.confirm_password" type="password" />

          <button class="primary-btn" @click="changePassword">Update Password</button>
        </div>
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

        <!-- FAVORITE PROFESSORS -->
        <section class="content-section">
          <h1 class="section-title">Favorite Professors</h1>

          <div v-if="favoriteProfessors.length === 0" class="empty-state">
            You don't have any favorite professors yet.
          </div>

          <div v-else class="favorites-grid">
            <div
              v-for="prof in favoriteProfessors"
              :key="prof.professor_id"
              class="favorite-card"
            >
              <div class="favorite-info">
                <h3>{{ prof.f_name }} {{ prof.m_name }} {{ prof.l_name }}</h3>
                <p>{{ prof.email || "No email available" }}</p>
              </div>

              <button class="secondary-btn" @click="removeFavorite(prof.professor_id)">
                Remove
              </button>
            </div>
          </div>
        </section>

        <!-- USER REVIEWS -->
        <section class="content-section">
          <h1 class="section-title">Your Reviews</h1>

          <div v-if="userReviews.length === 0" class="empty-state">
            You have not submitted any reviews yet. Share your experience to help other students choose professors.
          </div>

          <div v-else class="reviews-list">
            <article
              v-for="review in userReviews"
              :key="review.review_id"
              class="review-card"
            >
              <div class="review-header">
                <div>
                  <h3>{{ review.professor_name }}</h3>
                  <p class="review-date">{{ formatDate(review.review_date) }}</p>
                </div>

                <div class="review-rating">
                  {{ review.review_rating }}/5
                </div>
              </div>

              <p class="review-comment">{{ review.comment_text }}</p>

              <div class="review-meta">
                <span>Grade: {{ review.received_grade || "N/A" }}</span>
                <span>Helpful: {{ review.helpful_count }}</span>
              </div>

              <div class="review-actions">
                <!-- TODO: Later connect Edit to actual edit review page/modal -->
                <button class="secondary-btn">Edit</button>
                <button class="danger-btn small-btn" @click="deleteReview(review.review_id)">
                  Delete
                </button>
              </div>
            </article>
          </div>
        </section>
      </section>
    </main>
  </div>
</template>

<style scoped>
.profile-page {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  background: #f5f5f5;
  min-height: calc(100vh - 80px);
}

.profile-sidebar {
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.profile-card {
  background: #719294;
  color: white;
  border-radius: 18px;
  padding: 1.5rem;
  text-align: center;
}

.avatar-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.avatar-image,
.avatar-placeholder {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  border: 4px solid white;
  object-fit: cover;
  background: #d9d9d9;
}

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2f2f2f;
  font-size: 2rem;
  font-weight: 700;
}

.profile-name {
  margin: 0.25rem 0;
  font-size: 1.5rem;
}

.profile-username,
.profile-email {
  margin: 0.2rem 0;
  opacity: 0.95;
  word-break: break-word;
}

.sidebar-actions {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  margin-top: 1rem;
}

.sidebar-btn,
.primary-btn,
.secondary-btn,
.danger-btn {
  border: none;
  border-radius: 999px;
  padding: 0.7rem 1rem;
  font-size: 0.95rem;
  cursor: pointer;
}

.sidebar-btn,
.secondary-btn {
  background: white;
  color: #4f6c72;
  font-weight: 600;
}

.primary-btn {
  background: #719294;
  color: white;
  font-weight: 600;
  margin-top: 0.75rem;
}

.danger-btn {
  background: #c94b4b;
  color: white;
  font-weight: 600;
}

.small-btn {
  padding: 0.55rem 0.9rem;
  font-size: 0.85rem;
}


.panel-card {
  background: white;
  border-radius: 18px;
  padding: 1rem;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
}

.panel-card h3 {
  margin-top: 0;
  color: #4f5a43;
}

.panel-card label {
  display: block;
  margin-top: 0.75rem;
  margin-bottom: 0.25rem;
  color: #444;
}

.panel-card input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid;
  border-radius: 10px;
  box-sizing: border-box;
  color: #0B0D09;
}

.profile-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2rem;
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

.content-section {
  background: transparent;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  color: #5a624f;
  margin: 0 0 1rem 0;
}

.empty-state {
  font-size: 1.1rem;
  color: #444;
  background: transparent;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 320px));
  gap: 1rem;
}

.favorite-card,
.review-card {
  background: white;
  border-radius: 18px;
  padding: 1rem;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
}

.favorite-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.favorite-info h3,
.review-card h3 {
  margin: 0 0 0.3rem 0;
  color: #333;
}

.favorite-info p,
.review-date,
.review-comment,
.review-meta {
  margin: 0;
  color: #666;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.review-rating {
  background: #719294;
  color: white;
  padding: 0.45rem 0.8rem;
  border-radius: 999px;
  font-weight: 700;
}

.review-comment {
  margin-top: 0.85rem;
  line-height: 1.5;
}

.review-meta {
  margin-top: 0.85rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  font-size: 0.95rem;
}

.review-actions {
  margin-top: 1rem;
  display: flex;
  gap: 0.75rem;
}

@media (max-width: 980px) {
  .profile-page {
    flex-direction: column;
  }

  .profile-sidebar {
    width: 100%;
  }

  .section-title {
    font-size: 2.2rem;
  }
}
</style>