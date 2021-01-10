import Vue from 'vue'

Vue.filter('limit', (value: string, size: number) => {
  if (!value) return ''
  value = value.toString()

  if (value.length <= size) {
    return value
  }
  return value.substr(0, size) + '...'
})

Vue.filter('prettyDateTime', (rawDateTime: string) => {
  const prettyDateTime =
    rawDateTime.slice(8, 10) +
    '.' +
    rawDateTime.slice(5, 7) +
    '.' +
    rawDateTime.slice(0, 4) +
    ' at ' +
    rawDateTime.slice(11, 16)
  return prettyDateTime
})
