import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
})

export default {
  async register(username: string, email: string, password: string) {
    const bodyFormData = new FormData()
    bodyFormData.append('username', username)
    bodyFormData.append('email', email)
    bodyFormData.append('password', password)

    const res = await apiClient({
      method: 'post',
      url: '/register',
      data: bodyFormData,
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return res
  },
}
