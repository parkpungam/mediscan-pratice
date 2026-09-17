import { describe, expect, it } from 'vitest'
import { getNicknameError, isValidEmail, isValidPassword } from './signupValidation'

describe('signup validation', () => {
  it('accepts only a 254-character email address at the maximum length', () => {
    const localPart = 'a'.repeat(242)
    expect(isValidEmail(`${localPart}@example.com`)).toBe(true)
    expect(isValidEmail(`${localPart}a@example.com`)).toBe(false)
    expect(isValidEmail('invalid-email')).toBe(false)
  })

  it('enforces password boundaries and requires an allowed symbol', () => {
    expect(isValidPassword('Ab1!xyz')).toBe(false)
    expect(isValidPassword('Ab1!xyz0')).toBe(true)
    expect(isValidPassword(`Ab1!${'x'.repeat(60)}`)).toBe(true)
    expect(isValidPassword(`Ab1!${'x'.repeat(61)}`)).toBe(false)
    expect(isValidPassword('abcd1234가')).toBe(false)
    expect(isValidPassword('Ab1!가나다라마바사')).toBe(true)
    expect(isValidPassword('Ab1! xyz0')).toBe(false)
  })

  it('enforces nickname character and length rules', () => {
    expect(getNicknameError('가')).not.toBe('')
    expect(getNicknameError('가나다라마바사아')).toBe('')
    expect(getNicknameError('abcd')).toBe('')
    expect(getNicknameError('abc')).not.toBe('')
    expect(getNicknameError('1234')).not.toBe('')
    expect(getNicknameError('name!')).not.toBe('')
  })
})