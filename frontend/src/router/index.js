import { createRouter, createWebHistory } from 'vue-router'
import ProfessorList from '../components/ProfessorList.vue'
import ReviewForm from '../components/ReviewForm.vue'
import LoginView from '../components/LoginView.vue'
import Register from '../components/Register.vue'
import ProfessorDetail from '../components/ProfessorDetail.vue'
import HomePage from '../components/HomePage.vue'
import ProfileSettings from '../components/ProfileSettings.vue'
import ModeratorView from '../components/ModeratorView.vue'

const routes = [
  { path: '/moderation', component: ModeratorView },
  { path: '/professors', component: ProfessorList },
  { path: '/professor/:professorId', component: ProfessorDetail },
  { path: '/reviews/:professorId', component: ReviewForm },
  { path: '/login', component: LoginView },
  { path: '/sign-up', component: Register},
  { path: '/profile', component: ProfileSettings },
  { path: '/', component: HomePage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router