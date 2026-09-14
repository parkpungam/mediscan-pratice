const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const ALLOWED_NICKNAME_PATTERN = /^[가-힣A-Za-z0-9]+$/
const HANGUL_PATTERN = /[가-힣]/
const NUMBER_ONLY_PATTERN = /^\d+$/

export function isValidEmail(value) {
  return EMAIL_PATTERN.test(value)
}

export function isValidPassword(value) {
  return (
    value.length >= 8 &&
    /[A-Za-z]/.test(value) &&
    /\d/.test(value) &&
    /[^A-Za-z\d\s]/.test(value) &&
    !/\s/.test(value)
  )
}

export function getNicknameError(value) {
  if (!value) return '닉네임을 입력해 주세요.'
  if (!ALLOWED_NICKNAME_PATTERN.test(value)) {
    return '한글, 영어, 숫자만 사용할 수 있습니다.'
  }
  if (NUMBER_ONLY_PATTERN.test(value)) {
    return '숫자로만 구성된 닉네임은 사용할 수 없습니다.'
  }

  const length = Array.from(value).length
  if (HANGUL_PATTERN.test(value) && (length < 2 || length > 8)) {
    return '한글이 포함된 닉네임은 2~8자로 입력해 주세요.'
  }
  if (!HANGUL_PATTERN.test(value) && (length < 4 || length > 14)) {
    return '영어·숫자 닉네임은 4~14자로 입력해 주세요.'
  }

  return ''
}
