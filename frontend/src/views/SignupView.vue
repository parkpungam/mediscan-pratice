<template>
  <main class="signup-page">
    <header class="site-header"><BrandLogo /></header>
    <div class="background-grid" aria-hidden="true"></div><div class="orb orb--left" aria-hidden="true"></div><div class="orb orb--right" aria-hidden="true"></div>
    <aside class="side-copy side-copy--left" aria-hidden="true"><span></span><p>더 나은<br />의료의 내일을 위한<br />학습의 시작</p><small>LEARNING CONNECTS<br />A HEALTHIER TOMORROW</small></aside>
    <aside class="side-copy side-copy--right" aria-hidden="true"><span></span><p>지식이 만드는<br />더 건강한 세상</p></aside>
    <section class="signup-shell">
      <h1><span>의료영상 학습</span>을 시작하세요</h1>
      <div class="signup-card">
        <SignupAccountStep v-if="currentStep === 1" :form="form" :email-check-state="emailCheckState" :login-notice="loginNotice" @update-field="updateField" @next="checkEmailAndContinue" @login="showLoginNotice" />
        <SignupProfileStep v-else-if="currentStep === 2" :form="form" :nickname-check-state="nicknameCheckState" :signup-state="signupState" :signup-error-message="signupErrorMessage" @update-field="updateField" @check-nickname="checkNickname" @previous="goToAccountStep" @signup="submitSignup" />
        <SignupEmailNotice v-else :email="form.email" :resend-state="resendState" :development-token="developmentToken" :verification-state="verificationState" :login-notice="loginNotice" @resend="resendEmail" @verify="verifyDevelopmentEmail" @change-email="changeEmail" @login="showLoginNotice" />
      </div>
      <section class="demo-guide" aria-label="가입 안내"><strong>가입 안내</strong><span>입력한 정보는 실제 서버에서 중복 확인 후 저장됩니다.</span></section>
    </section>
  </main>
</template>

<script>
import BrandLogo from '../components/common/BrandLogo.vue'
import SignupAccountStep from '../components/signup/SignupAccountStep.vue'
import SignupProfileStep from '../components/signup/SignupProfileStep.vue'
import SignupEmailNotice from '../components/signup/SignupEmailNotice.vue'
import { request } from '../services/api'

export default {
  name: 'SignupView',
  components: { BrandLogo, SignupAccountStep, SignupProfileStep, SignupEmailNotice },
  data() {
    return {
      currentStep: 1, emailCheckState: 'idle', nicknameCheckState: 'idle', signupState: 'idle', signupErrorMessage: '',
      resendState: 'idle', verificationState: 'idle', developmentToken: '', loginNotice: '',
      form: { email: '', password: '', passwordConfirm: '', termsAccepted: false, privacyAccepted: false, ageConfirmed: false, marketingAccepted: false, nickname: '', major: '', majorOther: '', signupSource: '', signupSourceOther: '' }
    }
  },
  methods: {
    updateField(field, value) {
      this.form[field] = value
      if (field === 'email') this.emailCheckState = 'idle'
      if (field === 'nickname') this.nicknameCheckState = 'idle'
      if (field === 'email' || field === 'nickname' || field === 'major' || field === 'majorOther' || field === 'signupSource' || field === 'signupSourceOther') this.signupErrorMessage = ''
      if (field === 'major' && value !== '기타 보건의료계열') this.form.majorOther = ''
      if (field === 'signupSource' && value !== '기타') this.form.signupSourceOther = ''
    },
    async checkEmailAndContinue() {
      this.loginNotice = ''; this.emailCheckState = 'loading'
      try {
        const result = await request('/v1/auth/email-availability?email=' + encodeURIComponent(this.form.email))
        if (!result.available) { this.emailCheckState = 'duplicate'; return }
        this.emailCheckState = 'available'; this.currentStep = 2
      } catch (error) { this.emailCheckState = 'error' }
    },
    async checkNickname() {
      this.nicknameCheckState = 'loading'
      try {
        const result = await request('/v1/users/nickname-availability?nickname=' + encodeURIComponent(this.form.nickname))
        this.nicknameCheckState = result.available ? 'available' : 'duplicate'
      } catch (error) { this.nicknameCheckState = 'error' }
    },
    async submitSignup() {
      this.signupState = 'loading'; this.signupErrorMessage = ''
      try {
        const result = await request('/v1/auth/register', { method: 'POST', body: JSON.stringify(this.form) })
        this.developmentToken = result.developmentToken || ''
        this.verificationState = 'idle'; this.signupState = 'success'; this.currentStep = 3
      } catch (error) {
        this.signupState = 'error'
        if (error.code === 'EMAIL_TAKEN') this.signupErrorMessage = '이미 가입된 이메일입니다. 이메일 주소를 변경해 주세요.'
        else if (error.code === 'NICKNAME_TAKEN') this.signupErrorMessage = '이미 사용 중인 닉네임입니다. 다른 닉네임을 입력해 주세요.'
        else if (error.code === 'INVALID_REGISTRATION') this.signupErrorMessage = '입력 내용을 다시 확인해 주세요.'
        else this.signupErrorMessage = '회원가입을 완료하지 못했습니다. 잠시 후 다시 시도해 주세요.'
      }
    },
    async resendEmail() {
      this.resendState = 'loading'
      try {
        const result = await request('/v1/auth/resend-verification', { method: 'POST', body: JSON.stringify({ email: this.form.email }) })
        this.developmentToken = result.developmentToken || ''; this.resendState = 'sent'
      } catch (error) { this.resendState = 'error' }
    },
    async verifyDevelopmentEmail() {
      if (!this.developmentToken) return
      this.verificationState = 'loading'
      try {
        await request('/v1/auth/verify-email', { method: 'POST', body: JSON.stringify({ token: this.developmentToken }) })
        this.developmentToken = ''; this.verificationState = 'verified'
      } catch (error) { this.verificationState = 'error' }
    },
    goToAccountStep() { this.currentStep = 1; this.loginNotice = '' },
    changeEmail() {
      this.currentStep = 1; this.emailCheckState = 'idle'; this.resendState = 'idle'; this.verificationState = 'idle'; this.developmentToken = ''; this.loginNotice = ''
    },
    showLoginNotice() { this.$router.push('/login') }
  }
}
</script>