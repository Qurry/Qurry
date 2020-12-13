export default {
  async getQuestions($axios: any) {
    const { data }: { data: any } = await $axios.get('/questions')
    return data
  },
  async getQuestion($axios: any, id: string) {
    const { data }: { data: any } = await $axios.get('/questions/' + id)
    return data
  },
  async createQuestion($axios: any, question: any) {
    const response = await $axios.post('/questions/', question)
    return response
  },
  async editQuestion($axios: any, questionId: number, question: any) {
    const response = await $axios.patch(
      '/questions/' + questionId + '/',
      question
    )
    return response
  },
  async deleteQuestion($axios: any, questionId: number) {
    const response = await $axios.delete('/questions/' + questionId)
    return response
  },
}
