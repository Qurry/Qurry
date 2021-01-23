import { NuxtAxiosInstance } from '@nuxtjs/axios'
import { User, RegistrationUser } from '~/pages/users/user.model'

export default {
  async register($axios: NuxtAxiosInstance, user: RegistrationUser) {
    const bodyFormData = new FormData()
    bodyFormData.append('username', user.username)
    bodyFormData.append('email', user.email)
    bodyFormData.append('password', user.password)

    const response = await $axios.post('/register/', bodyFormData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response
  },
  async getUsers($axios: NuxtAxiosInstance) {
    const { data }: { data: User[] } = await $axios.get('/users/')
    return data
  },
}
