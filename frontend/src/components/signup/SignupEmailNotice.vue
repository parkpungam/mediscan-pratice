<template>
  <section class="email-notice" aria-labelledby="email-notice-title">
    <SignupProgress :step="3" />
    <div class="email-icon" aria-hidden="true"><svg viewBox="0 0 120 90"><rect x="10" y="15" width="86" height="60" rx="7"></rect><path d="M14 22l39 31 39-31"></path></svg><span>✓</span></div>
    <h2 id="email-notice-title">인증메일 발송 안내</h2>
    <p class="notice-lead">회원가입 정보 입력이 완료되었습니다</p>
    <p class="email-address">{{ email }}</p>
    <p class="notice-copy">이메일 인증 후 모든 학습 기능을 이용할 수 있습니다.</p>
    <button class="primary-button" type="button" :disabled="resendState === 'loading' || cooldownSeconds > 0" @click="$emit('resend')">{{ resendState === 'loading' ? '재발송 확인 중…' : cooldownSeconds > 0 ? cooldownSeconds + '초 후 재발송 가능' : '인증메일 다시 보내기' }}</button>
    <button v-if="developmentToken && verificationState !== 'verified'" class="secondary-button full-width" type="button" :disabled="verificationState === 'loading'" @click="$emit('verify')">{{ verificationState === 'loading' ? '인증 처리 중…' : '개발용 이메일 인증 완료' }}</button>
    <button class="secondary-button full-width" type="button" @click="$emit('change-email')">이메일 주소 변경</button>
    <button class="text-button" type="button" @click="$emit('login')">로그인으로 이동</button>
    <p v-if="resendState === 'sent'" class="demo-result" aria-live="polite">인증 안내가 다시 준비되었습니다. 실제 이메일은 발송되지 않았습니다.</p>
    <p v-if="resendState === 'error' || verificationState === 'error'" class="field-error" aria-live="polite">요청을 처리하지 못했습니다. 잠시 후 다시 시도해 주세요.</p>
    <p v-if="verificationState === 'verified'" class="demo-result" aria-live="polite">개발 환경에서 이메일 인증이 완료되었습니다.</p>
    <p v-if="loginNotice" class="demo-result" aria-live="polite">{{ loginNotice }}</p>
    <p class="demo-hint">개발 환경 안내 · 실제 이메일은 발송되지 않습니다.</p>
  </section>
</template>

<script>
import SignupProgress from './SignupProgress.vue'

export default {
  name: 'SignupEmailNotice',
  components: { SignupProgress },
  emits: ['resend', 'verify', 'change-email', 'login'],
  props: {
    email: { type: String, required: true },
    resendState: { type: String, default: 'idle' },
    cooldownSeconds: { type: Number, default: 0 },
    developmentToken: { type: String, default: '' },
    verificationState: { type: String, default: 'idle' },
    loginNotice: { type: String, default: '' }
  }
}
</script>
