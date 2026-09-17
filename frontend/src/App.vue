<template>
  <router-view />
</template>

<script>
import { applyTheme, getTheme } from './utils/theme'
import { setUnauthorizedHandler } from './services/api'

export default {
  name: 'App',
  created() { applyTheme(getTheme()); setUnauthorizedHandler(() => { if (!['/login', '/signup'].includes(this.$route.path)) this.$router.replace('/login') }) }
}
</script>

<style>
#app { min-height: 100vh; }
</style>