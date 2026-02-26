import { createRouter, createWebHistory } from 'vue-router'
import ProfessorList from '../components/ProfessorList.vue'
import ReviewForm from '../components/ReviewForm.vue'
import LoginView from '../components/LoginView.vue'
import ProfessorDetail from '../components/ProfessorDetail.vue'

const routes = [
  { path: '/professors', component: ProfessorList },
  { path: '/professor/1', component: ProfessorDetail },
  { path: '/reviews/:professorId', component: ReviewForm },
  { path: '/login', component: LoginView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router