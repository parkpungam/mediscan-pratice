<template>
  <div class="signup-progress" :aria-label="progressLabel">
    <div class="signup-progress__track" aria-hidden="true">
      <span class="signup-progress__line" :class="{ complete: step > 1 }"></span>
      <span class="signup-progress__point active">
        <span v-if="step > 1">✓</span>
        <span v-else>1</span>
      </span>
      <span class="signup-progress__point" :class="{ active: step >= 2 }">
        <span v-if="step > 2">✓</span>
        <span v-else>2</span>
      </span>
    </div>
    <p>{{ stepLabel }}</p>
  </div>
</template>

<script>
export default {
  name: 'SignupProgress',
  props: {
    step: {
      type: Number,
      required: true
    }
  },
  computed: {
    stepLabel() {
      if (this.step === 1) return '1 / 2  계정 정보'
      return '2 / 2  기본 정보'
    },
    progressLabel() {
      if (this.step === 1) return '회원가입 2단계 중 1단계, 계정 정보'
      if (this.step === 2) return '회원가입 2단계 중 2단계, 기본 정보'
      return '회원가입 정보 입력 완료'
    }
  }
}
</script>

<style scoped>
.signup-progress {
  margin-bottom: 29px;
  text-align: center;
}

.signup-progress__track {
  position: relative;
  display: flex;
  justify-content: space-between;
  width: 226px;
  margin: 0 auto;
}

.signup-progress__line {
  position: absolute;
  top: 15px;
  left: 31px;
  right: 31px;
  height: 3px;
  background: linear-gradient(90deg, var(--accent) 0 50%, #26363c 50% 100%);
}

.signup-progress__line.complete {
  background: var(--accent);
}

.signup-progress__point {
  position: relative;
  z-index: 1;
  display: grid;
  width: 32px;
  height: 32px;
  place-items: center;
  border-radius: 50%;
  background: #26343a;
  color: #eef7f7;
  font-weight: 700;
  box-shadow: 0 0 0 5px rgba(4, 17, 22, 0.75);
}

.signup-progress__point.active {
  background: var(--accent);
  color: #021a19;
}

.signup-progress p {
  margin: 9px 0 0;
  color: #f2f5f6;
  font-size: 15px;
}
</style>
