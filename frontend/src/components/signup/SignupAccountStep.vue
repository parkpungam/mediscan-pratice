<template>
  <form class="signup-form" novalidate @submit.prevent="requestNext">
    <SignupProgress :step="1" />

    <div class="form-field">
      <label for="signup-email">이메일</label>
      <input
        id="signup-email"
        type="email"
        autocomplete="email"
        maxlength="254"
        :value="form.email"
        placeholder="name@example.com"
        :aria-invalid="Boolean(emailMessage)"
        aria-describedby="email-message"
        @input="updateEmail"
      />
      <p id="email-message" class="field-message" :class="emailMessageClass" aria-live="polite">
        {{ emailMessage }}
      </p>
    </div>

    <div class="form-field">
      <label for="signup-password">비밀번호</label>
      <div class="input-with-action">
        <input
          id="signup-password"
          :type="showPassword ? 'text' : 'password'"
          autocomplete="new-password"
          maxlength="64"
          :value="form.password"
          placeholder="영문·숫자·특수문자 포함 8~64자"
          :aria-invalid="Boolean(passwordMessage)"
          aria-describedby="password-message"
          @input="updateField('password', $event.target.value)"
        />
        <button
          class="visibility-button"
          type="button"
          :aria-label="showPassword ? '비밀번호 숨기기' : '비밀번호 보기'"
          @click="showPassword = !showPassword"
        >
          {{ showPassword ? '숨김' : '보기' }}
        </button>
      </div>
      <p id="password-message" class="field-message error">{{ passwordMessage }}</p>
    </div>

    <div class="form-field">
      <label for="signup-password-confirm">비밀번호 확인</label>
      <div class="input-with-action">
        <input
          id="signup-password-confirm"
          :type="showPasswordConfirm ? 'text' : 'password'"
          autocomplete="new-password"
          maxlength="64"
          :value="form.passwordConfirm"
          :aria-invalid="Boolean(passwordConfirmMessage)"
          aria-describedby="password-confirm-message"
          @input="updateField('passwordConfirm', $event.target.value)"
        />
        <button
          class="visibility-button"
          type="button"
          :aria-label="showPasswordConfirm ? '비밀번호 확인 숨기기' : '비밀번호 확인 보기'"
          @click="showPasswordConfirm = !showPasswordConfirm"
        >
          {{ showPasswordConfirm ? '숨김' : '보기' }}
        </button>
      </div>
      <p id="password-confirm-message" class="field-message error">{{ passwordConfirmMessage }}</p>
    </div>

    <fieldset class="agreement-group">
      <legend class="sr-only">가입 동의</legend>
      <label class="check-row check-row--all">
        <input type="checkbox" :checked="allAgreements" @change="toggleAll($event.target.checked)" />
        <span>전체 동의</span>
      </label>
      <label class="check-row">
        <input
          type="checkbox"
          :checked="form.termsAccepted"
          @change="updateField('termsAccepted', $event.target.checked)"
        />
        <span><strong>[필수]</strong> 이용약관 동의</span>
      </label>
      <label class="check-row">
        <input
          type="checkbox"
          :checked="form.privacyAccepted"
          @change="updateField('privacyAccepted', $event.target.checked)"
        />
        <span><strong>[필수]</strong> 개인정보 수집 및 이용동의</span>
      </label>
      <label class="check-row">
        <input
          type="checkbox"
          :checked="form.ageConfirmed"
          @change="updateField('ageConfirmed', $event.target.checked)"
        />
        <span><strong>[필수]</strong> 만 14세 이상입니다</span>
      </label>
      <label class="check-row">
        <input
          type="checkbox"
          :checked="form.marketingAccepted"
          @change="updateField('marketingAccepted', $event.target.checked)"
        />
        <span><em>[선택]</em> 마케팅 정보 이메일 수신 동의</span>
      </label>
    </fieldset>

    <button class="primary-button" type="submit" :disabled="!canContinue || checkingEmail">
      {{ checkingEmail ? '이메일 확인 중…' : '다음' }}
    </button>

    <p class="login-copy">이미 계정이 있으신가요? <button type="button" @click="$emit('login')">로그인</button></p>
    <p v-if="loginNotice" class="demo-result" aria-live="polite">{{ loginNotice }}</p>
    <p class="demo-hint">화면 시연용 · 실제 중복 조회나 정보 저장은 하지 않습니다.</p>
  </form>
</template>

<script>
import SignupProgress from './SignupProgress.vue'
import { isValidEmail, isValidPassword } from '../../utils/signupValidation'

export default {
  name: 'SignupAccountStep',
  components: { SignupProgress },
  emits: ['update-field', 'next', 'login'],
  props: {
    form: {
      type: Object,
      required: true
    },
    emailCheckState: {
      type: String,
      default: 'idle'
    },
    loginNotice: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      showPassword: false,
      showPasswordConfirm: false
    }
  },
  computed: {
    allAgreements() {
      return (
        this.form.termsAccepted &&
        this.form.privacyAccepted &&
        this.form.ageConfirmed &&
        this.form.marketingAccepted
      )
    },
    canContinue() {
      return (
        isValidEmail(this.form.email) &&
        isValidPassword(this.form.password) &&
        this.form.password === this.form.passwordConfirm &&
        this.form.termsAccepted &&
        this.form.privacyAccepted &&
        this.form.ageConfirmed
      )
    },
    checkingEmail() {
      return this.emailCheckState === 'loading'
    },
    emailMessage() {
      if (this.form.email && !isValidEmail(this.form.email)) return '올바른 이메일 형식으로 입력해 주세요.'
      if (this.emailCheckState === 'duplicate') return '이미 가입된 이메일입니다.'
      if (this.emailCheckState === 'error') return '중복 확인에 실패했습니다. 다시 시도해 주세요.'
      return ''
    },
    emailMessageClass() {
      return this.emailMessage ? 'error' : ''
    },
    passwordMessage() {
      if (this.form.password && !isValidPassword(this.form.password)) {
        return '영문·숫자·특수문자를 포함해 8~64자로 입력해 주세요.'
      }
      return ''
    },
    passwordConfirmMessage() {
      if (this.form.passwordConfirm && this.form.password !== this.form.passwordConfirm) {
        return '비밀번호가 일치하지 않습니다.'
      }
      return ''
    }
  },
  methods: {
    updateField(field, value) {
      this.$emit('update-field', field, value)
    },
    updateEmail(event) {
      const emailWithoutSpaces = event.target.value.replace(/\s/g, '')
      event.target.value = emailWithoutSpaces
      this.updateField('email', emailWithoutSpaces)
    },
    toggleAll(checked) {
      this.updateField('termsAccepted', checked)
      this.updateField('privacyAccepted', checked)
      this.updateField('ageConfirmed', checked)
      this.updateField('marketingAccepted', checked)
    },
    requestNext() {
      if (this.canContinue) this.$emit('next')
    }
  }
}
</script>
