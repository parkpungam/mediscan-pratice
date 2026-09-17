import { describe, expect, it } from 'vitest'
import router from './index'

describe('router', () => {
  it('registers the main route with its component and tab title', () => {
    const route = router.resolve('/main')
    expect(route.name).toBe('main')
    expect(route.meta.title).toBe('메인')
    expect(route.matched[0].components.default).toBeTruthy()
  })
})