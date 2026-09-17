<template>
  <main class="signup-page">
    <header class="site-header"><button class="brand-home" type="button" aria-label="로그인 화면으로 이동" @click="$router.push('/login')"><BrandLogo /></button><div class="auth-theme-switch" role="group" aria-label="화면 테마"><button type="button" :class="{ active: theme === 'light' }" @click="changeTheme('light')">라이트</button><button type="button" :class="{ active: theme === 'dark' }" @click="changeTheme('dark')">다크</button></div></header>
    <div class="background-grid" aria-hidden="true"></div><div class="orb orb--left" aria-hidden="true"></div><div class="orb orb--right" aria-hidden="true"></div>
    <section class="signup-shell">
      <h1><span>다시 만나서 반가워요</span><br />로그인해 주세요</h1>
      <div class="signup-card"><LoginForm :email="email" :password="password" :keep-signed-in="keepSignedIn" :loading="loading" :error="error" @update:email="email=$event" @update:password="password=$event" @update:keep-signed-in="keepSignedIn=$event" @submit="login" /></div>
    </section>
  </main>
</template>

<script>
import BrandLogo from '../components/common/BrandLogo.vue'
import LoginForm from '../components/login/LoginForm.vue'
import { request } from '../services/api'
import { applyTheme, getTheme } from '../utils/theme'

export default {
  name: 'LoginView',
  components: { BrandLogo, LoginForm },
  data() { return { email: '', password: '', keepSignedIn: false, loading: false, error: '', theme: getTheme() } },
  methods: {
    changeTheme(theme) { this.theme = applyTheme(theme) },
    async login() {
      this.loading = true; this.error = ''
      try { await request('/v1/auth/login', { method: 'POST', body: JSON.stringify({ email: this.email, password: this.password, keepSignedIn: this.keepSignedIn }) }); this.password = ''; this.$router.push('/main') }
      catch (error) { this.error = error.status === 401 ? '이메일 또는 비밀번호가 올바르지 않습니다.' : '일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.' }
      finally { this.loading = false }
    }
  }
}
</script>