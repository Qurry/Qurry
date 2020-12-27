import { NuxtAxiosInstance } from '@nuxtjs/axios'
import axios from 'axios'
import { User } from '~/pages/users/user.model'

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
  async getUsers($axios: NuxtAxiosInstance) {
    const { data }: { data: User[] } = await $axios.get('/users/')
    return data
  },
}
