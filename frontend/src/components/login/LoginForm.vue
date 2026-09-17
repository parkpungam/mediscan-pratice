<template>
  <form class="signup-form" novalidate @submit.prevent="submit">
    <div class="form-field"><label for="login-email">이메일</label><input id="login-email" type="email" autocomplete="email" :value="email" placeholder="이메일을 입력하세요" @input="$emit('update:email', $event.target.value.replace(/\s/g, ''))" /></div>
    <div class="form-field"><label for="login-password">비밀번호</label><div class="input-with-action"><input id="login-password" :type="showPassword ? 'text' : 'password'" autocomplete="current-password" :value="password" placeholder="비밀번호를 입력하세요" @input="$emit('update:password', $event.target.value)" /><button class="visibility-button" type="button" :aria-label="showPassword ? '비밀번호 숨기기' : '비밀번호 보기'" @click="showPassword=!showPassword">{{ showPassword ? '숨김' : '보기' }}</button></div></div>
    <p v-if="error" class="field-message error" aria-live="polite">{{ error }}</p>
    <button class="primary-button" type="submit" :disabled="!email || !password || loading">{{ loading ? '로그인 중…' : '로그인' }}</button>
    <p class="login-copy">계정이 없으신가요? <button type="button" @click="$router.push('/signup')">회원가입</button></p>
  </form>
</template>
<script>
export default { name:'LoginForm', emits:['update:email','update:password','submit'], props:{email:String,password:String,loading:Boolean,error:String}, data(){return{showPassword:false}}, methods:{submit(){if(this.email&&this.password&&!this.loading)this.$emit('submit')}} }
</script>
