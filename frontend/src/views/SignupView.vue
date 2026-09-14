<template>
  <main class="signup-page">
    <header class="site-header">
      <BrandLogo />
    </header>

    <div class="background-grid" aria-hidden="true"></div>
    <div class="orb orb--left" aria-hidden="true"></div>
    <div class="orb orb--right" aria-hidden="true"></div>

    <aside class="side-copy side-copy--left" aria-hidden="true">
      <span></span>
      <p>더 나은<br />의료의 내일을 위한<br />학습의 시작</p>
      <small>LEARNING CONNECTS<br />A HEALTHIER TOMORROW</small>
    </aside>
    <aside class="side-copy side-copy--right" aria-hidden="true">
      <span></span>
      <p>지식이 만드는<br />더 건강한 세상</p>
    </aside>

    <section class="signup-shell">
      <h1><span>의료영상 학습</span>을 시작하세요</h1>

      <div class="signup-card">
        <SignupAccountStep
          v-if="currentStep === 1"
          :form="form"
          :email-check-state="emailCheckState"
          :login-notice="loginNotice"
          @update-field="updateField"
          @next="checkEmailAndContinue"
          @login="showLoginNotice"
        />
        <SignupProfileStep
          v-else-if="currentStep === 2"
          :form="form"
          :nickname-check-state="nicknameCheckState"
          :signup-state="signupState"
          @update-field="updateField"
          @check-nickname="checkNickname"
          @previous="goToAccountStep"
          @signup="submitSignup"
        />
        <SignupEmailNotice
          v-else
          :email="form.email"
          :resend-state="resendState"
          :login-notice="loginNotice"
          @resend="resendEmail"
          @change-email="changeEmail"
          @login="showLoginNotice"
        />
      </div>

      <section class="demo-guide" aria-label="시연 상태 안내">
        <strong>데모 상태 확인</strong>
        <span>이메일: {{ demoValues.duplicateEmail }}(중복), {{ demoValues.lookupErrorEmail }}(조회 실패)</span>
        <span>닉네임: {{ demoValues.duplicateNickname }}(중복), {{ demoValues.lookupErrorNickname }}(조회 실패)</span>
      </section>
    </section>
  </main>
</template>

<script>
import BrandLogo from '../components/common/BrandLogo.vue'
import SignupAccountStep from '../components/signup/SignupAccountStep.vue'
import SignupProfileStep from '../components/signup/SignupProfileStep.vue'
import SignupEmailNotice from '../components/signup/SignupEmailNotice.vue'
import { DEMO_VALUES } from '../constants/signup'

const wait = (duration) => new Promise((resolve) => setTimeout(resolve, duration))

export default {
  name: 'SignupView',
  components: {
    BrandLogo,
    SignupAccountStep,
    SignupProfileStep,
    SignupEmailNotice
  },
  data() {
    return {
      currentStep: 1,
      emailCheckState: 'idle',
      nicknameCheckState: 'idle',
      signupState: 'idle',
      resendState: 'idle',
      loginNotice: '',
      demoValues: DEMO_VALUES,
      form: {
        email: '',
        password: '',
        passwordConfirm: '',
        termsAccepted: false,
        privacyAccepted: false,
        ageConfirmed: false,
        marketingAccepted: false,
        nickname: '',
        major: '',
        majorOther: '',
        signupSource: '',
        signupSourceOther: ''
      }
    }
  },
  methods: {
    updateField(field, value) {
      this.form[field] = value

      if (field === 'email') this.emailCheckState = 'idle'
      if (field === 'nickname') {
        this.nicknameCheckState = 'idle'
        this.signupState = 'idle'
      }
      if (field === 'major' && value !== '기타 보건의료계열') this.form.majorOther = ''
      if (field === 'signupSource' && value !== '기타') this.form.signupSourceOther = ''
    },
    async checkEmailAndContinue() {
      this.loginNotice = ''
      this.emailCheckState = 'loading'
      await wait(650)

      const email = this.form.email.toLowerCase()
      if (email === DEMO_VALUES.duplicateEmail) {
        this.emailCheckState = 'duplicate'
        return
      }
      if (email === DEMO_VALUES.lookupErrorEmail) {
        this.emailCheckState = 'error'
        return
      }

      this.emailCheckState = 'available'
      this.currentStep = 2
    },
    async checkNickname() {
      this.nicknameCheckState = 'loading'
      await wait(650)

      if (this.form.nickname === DEMO_VALUES.duplicateNickname) {
        this.nicknameCheckState = 'duplicate'
        return
      }
      if (this.form.nickname === DEMO_VALUES.lookupErrorNickname) {
        this.nicknameCheckState = 'error'
        return
      }

      this.nicknameCheckState = 'available'
    },
    async submitSignup() {
      this.signupState = 'loading'
      await wait(750)
      this.signupState = 'success'
      this.currentStep = 3
    },
    async resendEmail() {
      this.resendState = 'loading'
      this.loginNotice = ''
      await wait(650)
      this.resendState = 'sent'
    },
    goToAccountStep() {
      this.currentStep = 1
      this.loginNotice = ''
    },
    changeEmail() {
      this.currentStep = 1
      this.emailCheckState = 'idle'
      this.resendState = 'idle'
      this.loginNotice = ''
    },
    showLoginNotice() {
      this.loginNotice = '로그인 화면은 이번 회원가입 시연 범위에 포함되지 않습니다.'
    }
  }
}
</script>
