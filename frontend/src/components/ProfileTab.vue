<script setup>
import { ref, computed, watch } from "vue"
import api from "@/api/axios"

const props = defineProps({
  profile: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['message', 'profile-updated', 'logout'])

// === LOCAL STATE ===
const isEditing = ref(false)
const showPasswordForm = ref(false)
const showDeleteConfirm = ref(false)

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

// === DERIVED ===
const fullName = computed(() => {
  return [props.profile.f_name, props.profile.m_name, props.profile.l_name]
    .filter(Boolean)
    .join(" ")
})

const getInitials = () => {
  const first = props.profile.f_name ? props.profile.f_name[0] : ""
  const last = props.profile.l_name ? props.profile.l_name[0] : ""
  return `${first}${last}`.toUpperCase()
}

// === HELPERS ===
const seedEditForm = () => {
  editForm.value = {
    username: props.profile.username || "",
    email: props.profile.email || "",
    f_name: props.profile.f_name || "",
    m_name: props.profile.m_name || "",
    l_name: props.profile.l_name || "",
  }
}

// Keep editForm in sync when the parent passes fresh profile data
// (initial fetch, or after another update). Skip while editing so we
// don't clobber the user's in-progress changes.
watch(
  () => props.profile,
  () => {
    if (!isEditing.value) seedEditForm()
  },
  { deep: true, immediate: true }
)

// === ACTIONS ===
const toggleEdit = async () => {
  if (!isEditing.value) {
    seedEditForm()
    isEditing.value = true
    return
  }
  await saveProfile()
}

const cancelEdit = () => {
  seedEditForm()
  isEditing.value = false
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
      emit('message', { text: "No changes to save", type: "error" })
      return
    }

    const res = await api.patch("me/update/", payload)

    emit('profile-updated', res.data)
    isEditing.value = false
    emit('message', { text: "Profile updated successfully.", type: "success" })
  } catch (err) {
    console.error("PATCH /me/update failed:", err.response?.data || err.message)
    emit('message', { text: "Failed to update profile.", type: "error" })
  }
}

const changePassword = async () => {
  if (
    !passwordForm.value.current_password ||
    !passwordForm.value.new_password ||
    !passwordForm.value.confirm_password
  ) {
    emit('message', { text: "Please fill in all password fields.", type: "error" })
    return
  }

  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    emit('message', { text: "New password and confirm password do not match.", type: "error" })
    return
  }

  try {
    await api.patch("me/update/", {
      current_password: passwordForm.value.current_password,
      password: passwordForm.value.new_password,
    })

    emit('message', { text: "Password updated successfully.", type: "success" })
    showPasswordForm.value = false

    passwordForm.value = {
      current_password: "",
      new_password: "",
      confirm_password: "",
    }
  } catch (err) {
    console.error("PATCH /me/update password failed:", err.response?.data || err.message)
    emit('message', {
      text:
        err.response?.data?.error ||
        err.response?.data?.current_password?.[0] ||
        "Failed to update password.",
      type: "error",
    })
  }
}

const deleteAccount = async () => {
  try {
    await api.delete("me/delete/")
    showDeleteConfirm.value = false
    emit('message', { text: "Deleted account.", type: "success" })
    emit('logout')
  } catch (err) {
    console.error("DELETE /me/delete failed:", err.response?.status, err.response?.data || err.message)
    emit('message', { text: "Could not delete account.", type: "error" })
    showDeleteConfirm.value = false
  }
}
</script>

<template>
  <div class="tab-panel">
    <div class="profile-form-layout">
      <!-- Form fields (left) -->
      <div class="form-fields">
        <div class="field-row">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="editForm.username"
            type="text"
            :disabled="!isEditing"
          />
        </div>

        <div class="field-row">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="editForm.email"
            type="email"
            :disabled="!isEditing"
          />
        </div>

        <div class="field-row">
          <label for="f_name">First Name</label>
          <input
            id="f_name"
            v-model="editForm.f_name"
            type="text"
            :disabled="!isEditing"
          />
        </div>

        <div class="field-row">
          <label for="m_name">Middle Name</label>
          <input
            id="m_name"
            v-model="editForm.m_name"
            type="text"
            :disabled="!isEditing"
          />
        </div>

        <div class="field-row">
          <label for="l_name">Last Name</label>
          <input
            id="l_name"
            v-model="editForm.l_name"
            type="text"
            :disabled="!isEditing"
          />
        </div>

        <div class="form-actions">
          <button class="primary-btn" @click="toggleEdit">
            {{ isEditing ? "Save" : "Edit" }}
          </button>
          <button
            v-if="isEditing"
            class="secondary-btn"
            @click="cancelEdit"
          >
            Cancel
          </button>
        </div>
      </div>

      <!-- Avatar (right) -->
      <div class="avatar-column">
        <div class="avatar-wrapper">
          <img
            v-if="profile.profile_picture_url"
            :src="profile.profile_picture_url"
            alt="Profile picture"
            class="avatar-image"
          />
          <div v-else class="avatar-placeholder">
            {{ getInitials() }}
          </div>
        </div>
        <p class="avatar-name">{{ fullName || "User Name" }}</p>
        <p class="avatar-handle">@{{ profile.username }}</p>
      </div>
    </div>

    <!-- Secondary actions -->
    <div class="secondary-actions">
      <button
        v-if="profile.can_change_password"
        class="ghost-btn"
        @click="showPasswordForm = !showPasswordForm"
      >
        {{ showPasswordForm ? "Close Password Form" : "Change Password" }}
      </button>

      <button class="ghost-btn danger-ghost" @click="showDeleteConfirm = true">
        Delete Account
      </button>
    </div>

    <!-- Change Password panel -->
    <div v-if="showPasswordForm" class="password-panel">
      <label>Current Password</label>
      <input v-model="passwordForm.current_password" type="password" />

      <label>New Password</label>
      <input v-model="passwordForm.new_password" type="password" />

      <label>Confirm New Password</label>
      <input v-model="passwordForm.confirm_password" type="password" />

      <button class="primary-btn" @click="changePassword">
        Update Password
      </button>
    </div>

    <!-- Delete Confirm Modal -->
    <div
      v-if="showDeleteConfirm"
      class="fixed inset-0 flex items-center justify-center bg-black/30 z-50"
    >
      <div class="bg-white rounded-xl p-6 w-[360px] shadow-lg text-center">
        <h3 class="text-xl font-bold text-[#0B0D09] mb-3">Delete Account</h3>
        <p class="text-[#444] mb-5">
          Are you sure you want to delete your profile? This action cannot be undone.
        </p>

        <div class="flex justify-center gap-3">
          <button class="secondary-btn" @click="showDeleteConfirm = false">
            Cancel
          </button>
          <button class="danger-btn" @click="deleteAccount">
            Yes, Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tab-panel {
  background: white;
  border-radius: 14px;
  padding: 2rem;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
}

.profile-form-layout {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.form-fields {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 0;
}

.field-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.field-row label {
  width: 110px;
  flex-shrink: 0;
  color: #444;
  font-weight: 500;
  font-size: 0.95rem;
}

.field-row input {
  flex: 1;
  padding: 0.6rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #0B0D09;
  background: white;
  transition: border-color 0.15s, background 0.15s;
  min-width: 0;
}

.field-row input:disabled {
  background: #f9fafb;
  color: #4b5563;
  cursor: not-allowed;
}

.field-row input:focus {
  outline: none;
  border-color: #719294;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.avatar-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  width: 180px;
  flex-shrink: 0;
}

.avatar-wrapper {
  display: flex;
  justify-content: center;
}

.avatar-image,
.avatar-placeholder {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 4px solid #719294;
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

.avatar-name {
  margin: 0.5rem 0 0 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  text-align: center;
  word-break: break-word;
}

.avatar-handle {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
  word-break: break-word;
}

.secondary-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
  flex-wrap: wrap;
}

.ghost-btn {
  background: transparent;
  color: #4f6c72;
  border: 1px solid #d1d5db;
  padding: 0.55rem 1rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.15s;
}

.ghost-btn:hover {
  background: #f3f4f6;
}

.ghost-btn.danger-ghost {
  color: #c94b4b;
  border-color: #f2b8b8;
}

.ghost-btn.danger-ghost:hover {
  background: #fdeaea;
}

.password-panel {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.password-panel h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #4f5a43;
}

.password-panel label {
  display: block;
  margin-top: 0.75rem;
  margin-bottom: 0.25rem;
  color: #444;
}

.password-panel input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  box-sizing: border-box;
  color: #0B0D09;
}

.password-panel .primary-btn {
  margin-top: 1rem;
}

.primary-btn,
.secondary-btn,
.danger-btn {
  border: none;
  border-radius: 999px;
  padding: 0.7rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: filter 0.15s, transform 0.05s, background 0.15s;
}

.primary-btn {
  background: #719294;
  color: white;
}

.primary-btn:hover {
  filter: brightness(1.08);
}

.primary-btn:active {
  transform: scale(0.98);
}

.secondary-btn {
  background: white;
  color: #4f6c72;
  border: 1px solid #d1d5db;
}

.secondary-btn:hover {
  background: #f3f4f6;
}

.danger-btn {
  background: #c94b4b;
  color: white;
}

.danger-btn:hover {
  filter: brightness(1.08);
}

@media (max-width: 980px) {
  .profile-form-layout {
    flex-direction: column-reverse;
    align-items: center;
  }

  .form-fields {
    width: 100%;
  }

  .avatar-column {
    width: auto;
  }

  .field-row {
    flex-direction: column;
    align-items: stretch;
    gap: 0.35rem;
  }

  .field-row label {
    width: auto;
  }
}
</style>
