export interface User {
  id: string
  username: string
  score?: number
  image?: string
}

export interface RegistrationUser {
  username: string
  email: string
  password: string
}
