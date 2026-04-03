<script setup>
    import { ref, onMounted } from "vue"
    import { useRouter } from "vue-router"
    import api from "@/api/axios"
import Navbar from "./Navbar.vue"

    const router = useRouter()

    const form = ref({
        username: "",
        email: "",
        f_name: "",
        m_name: "",
        l_name: "",
        profile_picture_url: "",
        password: "",
    })

    const message = ref("")

    const fetchProfile = async () => {
    try {
        const res = await api.get("me/")
        form.value = { ...form.value, ...res.data }
    } catch (err) {
        console.error(err)
    }
    }

    const updateProfile = async () => {
        try {
            await api.patch("me/update/", form.value)
            message.value = "Profile updated successfully!"
            if (form.value.password) {
                localStorage.removeItem("access")
                router.push("/login")
            }
        } catch (err) {
            console.error(err)
            message.value = "Error updating profile"
        }
    }

    onMounted(() => {
        fetchProfile()
    })
</script>

<template>
    <div>
        <Navbar/>
    </div>
</template>