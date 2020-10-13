import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
})

interface Question {
  id: number
  title: string
  body: string
}

export default {
  async getQuestions() {
    const { data }: { data: any } = await apiClient.get('/questions')
    return data.questions as Question[]
  },
}
