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
  { path: '/moderation', component: ModeratorView, meta: {
    title: "Moderator Dashboard"
  }},
  { path: '/professors', component: ProfessorList },
  { path: '/professor/:professorId', component: ProfessorDetail },
  { path: '/reviews/:professorId', component: ReviewForm },
  { path: '/login', component: LoginView, meta: {
    title: "Login to Proffable"
  } },
  { path: '/sign-up', component: Register, meta: {
    title: "Join Proffable"
  }},
  { path: '/profile', component: ProfileSettings, meta: {
    title: "Proffable - Profile Settings"
  } },
  { path: '/', component: HomePage, meta: {
    title: "Proffable | Professor Ratings & Reviews"
  } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const siteTitle = to.meta.title || 'Proffable';
  document.title = siteTitle;

  const favicon = to.meta.favicon || "/ProffableLogo.png";
  let link = document.querySelector("link[rel~='icon']");
  if (!link) {
    link = document.createElement('link');
    link.rel = 'icon';
    document.getElementsByTagName('head')[0].appendChild(link);
  }
  link.href = favicon;

  next();
});

export default router