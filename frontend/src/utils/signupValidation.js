const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const ALLOWED_NICKNAME_PATTERN = /^[가-힣A-Za-z0-9]+$/
const HANGUL_PATTERN = /[가-힣]/
const NUMBER_ONLY_PATTERN = /^\d+$/
const ALLOWED_PASSWORD_SYMBOL = /[!@#$%^&*()\-_=+\[\]{};:'",.<>/?\\|`~]/

export function isValidEmail(value) {
  return value.length <= 254 && EMAIL_PATTERN.test(value)
}

export function isValidPassword(value) {
  return value.length >= 8 && value.length <= 64 && /[A-Za-z]/.test(value) && /\d/.test(value) && ALLOWED_PASSWORD_SYMBOL.test(value) && !/\s/.test(value)
}

export function getNicknameError(value) {
  if (!value) return '닉네임을 입력해 주세요.'
  if (!ALLOWED_NICKNAME_PATTERN.test(value)) return '한글, 영어, 숫자만 사용할 수 있습니다.'
  if (NUMBER_ONLY_PATTERN.test(value)) return '숫자로만 구성된 닉네임은 사용할 수 없습니다.'
  const length = Array.from(value).length
  if (HANGUL_PATTERN.test(value) && (length < 2 || length > 8)) return '한글이 포함된 닉네임은 2~8자로 입력해 주세요.'
  if (!HANGUL_PATTERN.test(value) && (length < 4 || length > 14)) return '영어·숫자 닉네임은 4~14자로 입력해 주세요.'
  return ''
}
export function getPasswordChecklist(value) { return [{ label: '8~64자', passed: value.length >= 8 && value.length <= 64 }, { label: '영문 포함', passed: /[A-Za-z]/.test(value) }, { label: '숫자 포함', passed: /\d/.test(value) }, { label: '특수문자 포함', passed: ALLOWED_PASSWORD_SYMBOL.test(value) }, { label: '공백 없음', passed: !/\s/.test(value) }] }
