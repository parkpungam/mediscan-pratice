<template>
  <main class="signup-page">
    <header class="site-header"><BrandLogo /></header>
    <div class="background-grid" aria-hidden="true"></div><div class="orb orb--left" aria-hidden="true"></div><div class="orb orb--right" aria-hidden="true"></div>
    <section class="signup-shell">
      <h1><span>다시 만나서 반가워요</span><br />로그인해 주세요</h1>
      <div class="signup-card"><LoginForm :email="email" :password="password" :loading="loading" :error="error" @update:email="email=$event" @update:password="password=$event" @submit="login" /></div>
      <section v-if="loggedIn" class="demo-guide" aria-live="polite">
        <strong>로그인 상태</strong>
        <span>로그인되었습니다. 학습 메인 화면은 아직 구현되지 않아 이 안내를 표시합니다.</span>
        <span v-if="!user.emailVerified">이메일 인증 전에는 인증 관련 동작 외 핵심 기능을 이용할 수 없습니다.</span>
        <button class="text-button" type="button" :disabled="logoutLoading" @click="logout">{{ logoutLoading ? '로그아웃 중…' : '로그아웃' }}</button>
        <p v-if="logoutError" class="field-error">로그아웃을 완료하지 못했습니다. 다시 시도해 주세요.</p>
      </section>
    </section>
  </main>
</template>

<script>
import BrandLogo from '../components/common/BrandLogo.vue'
import LoginForm from '../components/login/LoginForm.vue'
import { request } from '../services/api'

export default {
  name: 'LoginView',
  components: { BrandLogo, LoginForm },
  data() { return { email: '', password: '', loading: false, error: '', loggedIn: false, logoutLoading: false, logoutError: '', user: {} } },
  methods: {
    async login() {
      this.loading = true; this.error = ''
      try {
        this.user = (await request('/v1/auth/login', { method: 'POST', body: JSON.stringify({ email: this.email, password: this.password }) })).user
        this.loggedIn = true; this.password = ''; this.logoutError = ''
      } catch (error) { this.error = '이메일 또는 비밀번호가 올바르지 않습니다.' }
      finally { this.loading = false }
    },
    async logout() {
      this.logoutLoading = true; this.logoutError = ''
      try {
        await request('/v1/auth/logout', { method: 'POST' })
        this.loggedIn = false; this.user = {}; this.password = ''
      } catch (error) { this.logoutError = 'LOGOUT_FAILED' }
      finally { this.logoutLoading = false }
    }
  }
}
</script>