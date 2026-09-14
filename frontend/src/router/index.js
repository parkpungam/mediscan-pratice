import { createRouter, createWebHistory } from 'vue-router'
import SignupView from '../views/SignupView.vue'

const routes = [
  {
    path: '/',
    redirect: '/signup'
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
