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

// === STYLE TOKENS (shared across the tab) ===
const fieldRow =
  'flex items-center gap-4 max-[980px]:flex-col max-[980px]:items-stretch max-[980px]:gap-1.5'
const fieldLabel =
  'w-[110px] shrink-0 text-text-main font-medium text-sm max-[980px]:w-auto'
const fieldInput =
  'flex-1 px-3 py-2.5 border border-gray-300 rounded-lg text-sm text-text-main bg-surface transition-colors min-w-0 focus:outline-none focus:border-primary focus:bg-card disabled:bg-card disabled:border-gray-200 disabled:text-text-muted disabled:cursor-not-allowed'
const passwordInput =
  'w-full p-3 border border-gray-300 rounded-xl box-border text-text-main bg-surface focus:outline-none focus:border-primary focus:bg-card transition-colors'
const btnPrimary =
  'bg-primary hover:bg-primary-hover text-white px-6 py-2.5 rounded-full font-semibold text-sm shadow-md cursor-pointer transition-all active:scale-[0.98] border-0'
const btnSecondary =
  'bg-card hover:bg-surface text-text-main border border-gray-200 px-6 py-2.5 rounded-full font-semibold text-sm cursor-pointer transition-colors'
const btnDanger =
  'bg-red-600 hover:bg-red-700 text-white px-6 py-2.5 rounded-full font-semibold text-sm cursor-pointer transition-all border-0'
const btnGhost =
  'bg-transparent text-text-muted hover:bg-surface border border-gray-200 px-4 py-2 rounded-full font-semibold text-sm cursor-pointer transition-colors'
const btnGhostDanger =
  'bg-transparent text-red-600 hover:bg-red-50 border border-red-200 px-4 py-2 rounded-full font-semibold text-sm cursor-pointer transition-colors'
</script>

<template>
  <div class="bg-card rounded-[24px] p-8 shadow-xl border border-gray-100 text-left">
    <div
      class="flex gap-8 items-start max-[980px]:flex-col-reverse max-[980px]:items-center"
    >
      <!-- Form fields (left) -->
      <div class="flex-1 flex flex-col gap-4 min-w-0 max-[980px]:w-full">
        <div :class="fieldRow">
          <label for="username" :class="fieldLabel">Username</label>
          <input
            id="username"
            v-model="editForm.username"
            type="text"
            :disabled="!isEditing"
            :class="fieldInput"
          />
        </div>

        <div :class="fieldRow">
          <label for="email" :class="fieldLabel">Email</label>
          <input
            id="email"
            v-model="editForm.email"
            type="email"
            :disabled="!isEditing"
            :class="fieldInput"
          />
        </div>

        <div :class="fieldRow">
          <label for="f_name" :class="fieldLabel">First Name</label>
          <input
            id="f_name"
            v-model="editForm.f_name"
            type="text"
            :disabled="!isEditing"
            :class="fieldInput"
          />
        </div>

        <div :class="fieldRow">
          <label for="m_name" :class="fieldLabel">Middle Name</label>
          <input
            id="m_name"
            v-model="editForm.m_name"
            type="text"
            :disabled="!isEditing"
            :class="fieldInput"
          />
        </div>

        <div :class="fieldRow">
          <label for="l_name" :class="fieldLabel">Last Name</label>
          <input
            id="l_name"
            v-model="editForm.l_name"
            type="text"
            :disabled="!isEditing"
            :class="fieldInput"
          />
        </div>

        <div class="flex gap-3 mt-2">
          <button :class="btnPrimary" @click="toggleEdit">
            {{ isEditing ? "Save" : "Edit" }}
          </button>
          <button v-if="isEditing" :class="btnSecondary" @click="cancelEdit">
            Cancel
          </button>
        </div>
      </div>

      <!-- Avatar (right) -->
      <div
        class="flex flex-col items-center gap-2 w-[180px] shrink-0 max-[980px]:w-auto"
      >
        <div class="flex justify-center">
          <img
            v-if="profile.profile_picture_url"
            :src="profile.profile_picture_url"
            alt="Profile picture"
            class="w-[140px] h-[140px] rounded-full border-4 border-primary object-cover bg-gray-200"
          />
          <div
            v-else
            class="w-[140px] h-[140px] rounded-full border-4 border-primary bg-gray-200 flex items-center justify-center text-text-main text-3xl font-bold"
          >
            {{ getInitials() }}
          </div>
        </div>
        <p
          class="mt-2 mb-0 text-base font-bold text-text-main text-center break-words"
        >
          {{ fullName || "User Name" }}
        </p>
        <p class="m-0 text-text-muted text-sm break-words">
          @{{ profile.username }}
        </p>
      </div>
    </div>

    <!-- Secondary actions -->
    <div class="flex gap-3 mt-8 pt-6 border-t border-gray-200 flex-wrap">
      <button
        v-if="profile.can_change_password"
        :class="btnGhost"
        @click="showPasswordForm = !showPasswordForm"
      >
        {{ showPasswordForm ? "Close Password Form" : "Change Password" }}
      </button>

      <button :class="btnGhostDanger" @click="showDeleteConfirm = true">
        Delete Account
      </button>
    </div>

    <!-- Change Password panel -->
    <div v-if="showPasswordForm" class="mt-6 pt-6 border-t border-gray-200">
      <label class="block mt-3 mb-1 text-text-main font-medium text-sm">
        Current Password
      </label>
      <input
        v-model="passwordForm.current_password"
        type="password"
        :class="passwordInput"
      />

      <label class="block mt-3 mb-1 text-text-main font-medium text-sm">
        New Password
      </label>
      <input
        v-model="passwordForm.new_password"
        type="password"
        :class="passwordInput"
      />

      <label class="block mt-3 mb-1 text-text-main font-medium text-sm">
        Confirm New Password
      </label>
      <input
        v-model="passwordForm.confirm_password"
        type="password"
        :class="passwordInput"
      />

      <button :class="[btnPrimary, 'mt-4']" @click="changePassword">
        Update Password
      </button>
    </div>

    <!-- Delete Confirm Modal -->
    <div
      v-if="showDeleteConfirm"
      class="fixed inset-0 flex items-center justify-center bg-black/30 z-50"
    >
      <div class="bg-card rounded-2xl p-6 w-[360px] shadow-xl text-center">
        <h3 class="text-xl font-bold text-text-main mb-3">Delete Account</h3>
        <p class="text-text-muted mb-5">
          Are you sure you want to delete your profile? This action cannot be
          undone.
        </p>

        <div class="flex justify-center gap-3">
          <button :class="btnSecondary" @click="showDeleteConfirm = false">
            Cancel
          </button>
          <button :class="btnDanger" @click="deleteAccount">
            Yes, Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>