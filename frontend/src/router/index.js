import { createRouter, createWebHistory } from 'vue-router'
import ProfessorList from '../components/ProfessorList.vue'
import ReviewForm from '../components/ReviewForm.vue'

const routes = [
  { path: '/', component: ProfessorList },
  { path: '/reviews/:professorId', component: ReviewForm }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router