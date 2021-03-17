import { NuxtAxiosInstance } from '@nuxtjs/axios'
import { User } from '~/pages/users/user.model'

export default {
  async getUsers($axios: NuxtAxiosInstance) {
    const { data }: { data: User[] } = await $axios.get('/users/')
    return data
  },
}
