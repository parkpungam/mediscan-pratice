import { createRouter, createWebHistory } from 'vue-router'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  {
    path: '/',
    redirect: '/signup'
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView, meta: { title: '회원가입' }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView, meta: { title: '로그인' }
  },
  {
    path: '/main',
    name: 'main',
    component: MainView, meta: { title: '메인' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.afterEach((to) => { document.title = (to.meta.title || '메디스캔노트') + ' - 메디스캔노트' })

export default router
