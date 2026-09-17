import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import SignupProfileStep from './SignupProfileStep.vue'

const createForm = (overrides = {}) => ({
  nickname: '', major: '', majorOther: '', signupSource: '', signupSourceOther: '',
  ...overrides
})

const mountStep = (form, nicknameCheckState = 'idle') => mount(SignupProfileStep, {
  props: { form, nicknameCheckState, signupState: 'idle' }
})

describe('SignupProfileStep', () => {
  it('shows guidance choices before selection', () => {
    const wrapper = mountStep(createForm())
    expect(wrapper.get('#signup-major option').text()).toBe('전공을 선택하세요')
    expect(wrapper.get('#signup-source option').text()).toBe('메디스캔노트를 알게 된 경로를 선택해 주세요')
  })

  it('allows signup without a source when nickname confirmation and major are valid', async () => {
    const wrapper = mountStep(createForm({ nickname: '학습자', major: '방사선학과' }), 'available')
    expect(wrapper.get('button[type="submit"]').attributes('disabled')).toBeUndefined()
    await wrapper.get('form').trigger('submit')
    expect(wrapper.emitted('signup')).toHaveLength(1)
  })
})