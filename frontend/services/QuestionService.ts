import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
})

export default {
  async getQuestions() {
    const { data }: { data: any } = await apiClient.get('/questions')
    return data
  },
}
