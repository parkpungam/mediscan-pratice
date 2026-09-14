<template>
  <section class="email-notice" aria-labelledby="email-notice-title">
    <SignupProgress :step="3" />

    <div class="email-icon" aria-hidden="true">
      <svg viewBox="0 0 120 90">
        <rect x="10" y="15" width="86" height="60" rx="7"></rect>
        <path d="M14 22l39 31 39-31"></path>
      </svg>
      <span>✓</span>
    </div>

    <h2 id="email-notice-title">인증메일 발송 안내</h2>
    <p class="notice-lead">회원가입 정보 입력이 완료되었습니다</p>
    <p class="email-address">{{ email }}</p>
    <p class="notice-copy">이메일 인증 후 모든 학습 기능을 이용할 수 있습니다.</p>

    <button class="primary-button" type="button" :disabled="resendState === 'loading'" @click="$emit('resend')">
      {{ resendState === 'loading' ? '재발송 확인 중…' : '인증메일 다시 보내기' }}
    </button>
    <button class="secondary-button full-width" type="button" @click="$emit('change-email')">이메일 주소 변경</button>
    <button class="text-button" type="button" @click="$emit('login')">로그인으로 이동</button>

    <p v-if="resendState === 'sent'" class="demo-result" aria-live="polite">
      시연 상태가 갱신되었습니다. 실제 이메일은 발송되지 않았습니다.
    </p>
    <p v-if="loginNotice" class="demo-result" aria-live="polite">{{ loginNotice }}</p>
    <p class="demo-hint">화면 시연용 · 실제 이메일은 발송되지 않습니다.</p>
  </section>
</template>

<script>
import SignupProgress from './SignupProgress.vue'

export default {
  name: 'SignupEmailNotice',
  components: { SignupProgress },
  emits: ['resend', 'change-email', 'login'],
  props: {
    email: {
      type: String,
      required: true
    },
    resendState: {
      type: String,
      default: 'idle'
    },
    loginNotice: {
      type: String,
      default: ''
    }
  }
}
</script>
