export default {
  async getQuestions($axios: any) {
    const { data }: { data: any } = await $axios.get('/questions')
    return data
  },
  async getQuestion($axios: any, questionId: string) {
    const { data }: { data: any } = await $axios.get('/questions/' + questionId)
    return data
  },
  async createQuestion($axios: any, question: any) {
    const response = await $axios.post('/questions', question)
    return response
  },
  async editQuestion($axios: any, questionId: string, question: any) {
    const response = await $axios.patch('/questions/' + questionId, question)
    return response
  },
  async deleteQuestion($axios: any, questionId: string) {
    const response = await $axios.delete('/questions/' + questionId)
    return response
  },
}
