<template>
  <form class="signup-form" novalidate @submit.prevent="requestSignup">
    <SignupProgress :step="2" />

    <div class="form-field">
      <label for="signup-nickname">닉네임</label>
      <div class="input-with-button">
        <input
          id="signup-nickname"
          type="text"
          autocomplete="nickname"
          :value="form.nickname"
          placeholder="사용할 닉네임을 입력하세요"
          :aria-invalid="Boolean(nicknameMessage && nicknameCheckState !== 'available')"
          aria-describedby="nickname-message"
          @input="updateField('nickname', $event.target.value)"
        />
        <button
          class="outline-action"
          type="button"
          :disabled="Boolean(nicknameError) || nicknameCheckState === 'loading'"
          @click="$emit('check-nickname')"
        >
          {{ nicknameCheckState === 'loading' ? '확인 중…' : '중복 확인' }}
        </button>
      </div>
      <p id="nickname-message" class="field-message" :class="nicknameMessageClass" aria-live="polite">
        {{ nicknameMessage }}
      </p>
    </div>

    <div class="form-field">
      <label for="signup-major">전공</label>
      <select id="signup-major" :value="form.major" @change="updateField('major', $event.target.value)">
        <option value="" disabled>전공을 선택하세요</option>
        <option v-for="major in majorOptions" :key="major" :value="major">{{ major }}</option>
      </select>
      <input
        v-if="form.major === '기타 보건의료계열'"
        class="conditional-input"
        type="text"
        :value="form.majorOther"
        placeholder="전공을 직접 입력해 주세요"
        aria-label="기타 보건의료계열 전공 직접 입력"
        @input="updateField('majorOther', $event.target.value)"
      />
    </div>

    <div class="form-field">
      <label for="signup-source">가입 경로 <span>(선택)</span></label>
      <select id="signup-source" :value="form.signupSource" @change="updateField('signupSource', $event.target.value)">
        <option value="">메디스캔노트를 알게 된 경로를 선택해 주세요</option>
        <option v-for="source in sourceOptions" :key="source" :value="source">{{ source }}</option>
      </select>
      <input
        v-if="form.signupSource === '기타'"
        class="conditional-input"
        type="text"
        :value="form.signupSourceOther"
        placeholder="알게 된 경로를 입력해 주세요"
        aria-label="가입 경로 직접 입력"
        @input="updateField('signupSourceOther', $event.target.value)"
      />
    </div>

    <div class="button-row">
      <button class="secondary-button" type="button" :disabled="signupState === 'loading'" @click="$emit('previous')">
        이전
      </button>
      <button class="primary-button" type="submit" :disabled="!canSubmit || signupState === 'loading'">
        {{ signupState === 'loading' ? '가입 정보 확인 중…' : '가입하고 인증메일 받기' }}
      </button>
    </div>

    <p v-if="signupState === 'error'" class="submit-error" role="alert">
      가입 시연에 실패했습니다. 입력 상태를 확인하고 다시 시도해 주세요.
    </p>
    <p class="demo-hint">화면 시연용 · 실제 정보는 저장되지 않습니다.</p>
  </form>
</template>

<script>
import SignupProgress from './SignupProgress.vue'
import { MAJOR_OPTIONS, SOURCE_OPTIONS } from '../../constants/signup'
import { getNicknameError } from '../../utils/signupValidation'

export default {
  name: 'SignupProfileStep',
  components: { SignupProgress },
  emits: ['update-field', 'check-nickname', 'previous', 'signup'],
  props: {
    form: {
      type: Object,
      required: true
    },
    nicknameCheckState: {
      type: String,
      default: 'idle'
    },
    signupState: {
      type: String,
      default: 'idle'
    }
  },
  data() {
    return {
      majorOptions: MAJOR_OPTIONS,
      sourceOptions: SOURCE_OPTIONS
    }
  },
  computed: {
    nicknameError() {
      return getNicknameError(this.form.nickname)
    },
    nicknameMessage() {
      if (this.form.nickname && this.nicknameError) return this.nicknameError
      if (this.nicknameCheckState === 'available') return '사용 가능한 닉네임입니다.'
      if (this.nicknameCheckState === 'duplicate') return '이미 사용 중인 닉네임입니다.'
      if (this.nicknameCheckState === 'error') return '중복 확인에 실패했습니다. 다시 시도해 주세요.'
      if (this.form.nickname) return '닉네임 중복 확인이 필요합니다.'
      return ''
    },
    nicknameMessageClass() {
      return this.nicknameCheckState === 'available' ? 'success' : this.nicknameMessage ? 'error' : ''
    },
    hasValidMajor() {
      if (!this.form.major) return false
      if (this.form.major === '기타 보건의료계열') return Boolean(this.form.majorOther.trim())
      return true
    },
    hasValidSource() {
      if (this.form.signupSource !== '기타') return true
      return Boolean(this.form.signupSourceOther.trim())
    },
    canSubmit() {
      return this.nicknameCheckState === 'available' && this.hasValidMajor && this.hasValidSource
    }
  },
  methods: {
    updateField(field, value) {
      this.$emit('update-field', field, value)
    },
    requestSignup() {
      if (this.canSubmit) this.$emit('signup')
    }
  }
}
</script>
