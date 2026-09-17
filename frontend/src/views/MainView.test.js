import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import MainView from './MainView.vue'
import { request } from '../services/api'

vi.mock('../services/api', () => ({ request: vi.fn() }))

const mountView = () => {
  const replace = vi.fn()
  const push = vi.fn()
  return { wrapper: mount(MainView, { global: { mocks: { $router: { replace, push } } } }), replace, push }
}

describe('MainView', () => {
  beforeEach(() => vi.resetAllMocks())

  it('renders the three menus for a verified user', async () => {
    request.mockResolvedValue({ email: 'student@example.local', nickname: '테스트학생', emailVerified: true })
    const { wrapper } = mountView()
    await flushPromises()
    expect(wrapper.text()).toContain('테스트학생님')
    expect(wrapper.findAll('.menu-card')).toHaveLength(3)
  })

  it('leaves common unauthenticated redirects to the API client', async () => {
    request.mockRejectedValue(new Error('UNAUTHENTICATED'))
    const { wrapper, replace } = mountView()
    await flushPromises()
    expect(replace).not.toHaveBeenCalled()
    expect(wrapper.find('.loading-state').exists()).toBe(false)
  })

  it('does not route an unverified user to signup for email changes', async () => {
    request.mockResolvedValue({ email: 'student@example.local', nickname: '테스트학생', emailVerified: false })
    const { wrapper, push } = mountView()
    await flushPromises()
    const emailChange = wrapper.findAll('button').find((button) => button.text() === '이메일 변경')
    await emailChange.trigger('click')
    expect(push).not.toHaveBeenCalled()
    expect(wrapper.text()).toContain('이메일 변경 기능은 아직 준비 중입니다.')
  })
  it('prioritizes the verification notice for an unverified user', async () => {
    request.mockResolvedValue({ email: 'student@example.local', nickname: '테스트학생', emailVerified: false })
    const { wrapper } = mountView()
    await flushPromises()
    await wrapper.find('.menu-card').trigger('click')
    expect(wrapper.text()).toContain('이메일 인증 후 모든 학습 기능을 이용할 수 있습니다.')
    expect(wrapper.text()).not.toContain('기능은 아직 준비 중입니다.')
  })
})