import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import SignupAccountStep from './SignupAccountStep.vue'

const createForm = (overrides = {}) => ({
  email: '', password: '', passwordConfirm: '',
  termsAccepted: false, privacyAccepted: false, ageConfirmed: false, marketingAccepted: false,
  ...overrides
})

const mountStep = (form = createForm()) => mount(SignupAccountStep, {
  props: { form, emailCheckState: 'idle', loginNotice: '' }
})

describe('SignupAccountStep', () => {
  it('removes all whitespace from an email before emitting the field update', async () => {
    const wrapper = mountStep()
    await wrapper.get('#signup-email').setValue(' name @ example.com ')
    expect(wrapper.emitted('update-field')).toContainEqual(['email', 'name@example.com'])
  })

  it('selects and clears every agreement through the all-agreements control', async () => {
    const wrapper = mountStep()
    const allAgreements = wrapper.get('input[type="checkbox"]')
    await allAgreements.setValue(true)
    expect(wrapper.emitted('update-field')).toEqual([
      ['termsAccepted', true], ['privacyAccepted', true], ['ageConfirmed', true], ['marketingAccepted', true]
    ])
  })

  it('permits continuing without marketing consent when required fields are valid', async () => {
    const wrapper = mountStep(createForm({
      email: 'learner@example.com', password: 'Ab1!valid', passwordConfirm: 'Ab1!valid',
      termsAccepted: true, privacyAccepted: true, ageConfirmed: true
    }))
    expect(wrapper.get('button[type="submit"]').attributes('disabled')).toBeUndefined()
    await wrapper.get('form').trigger('submit')
    expect(wrapper.emitted('next')).toHaveLength(1)
  })
})