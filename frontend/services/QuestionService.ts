export default {
  async getQuestions($axios: any) {
    const { data }: { data: any } = await $axios.get('/questions/')
    return data
  },
  async getQuestion($axios: any, questionId: string) {
    const { data }: { data: any } = await $axios.get(
      '/questions/' + questionId + '/'
    )
    return data
  },
  async createQuestion($axios: any, question: any) {
    const response = await $axios.post('/questions/', question)
    return response
  },
  async editQuestion($axios: any, questionId: string, question: any) {
    const response = await $axios.patch(
      '/questions/' + questionId + '/',
      question
    )
    return response
  },
  async deleteQuestion($axios: any, questionId: string) {
    const response = await $axios.delete('/questions/' + questionId + '/')
    return response
  },
  async voteQuestion($axios: any, questionId: string, userVote: number) {
    const { data }: { data: any } = await $axios.get(
      '/questions/' + questionId + '/?vote=' + userVote
    )
    return data
  },
  async getComment($axios: any, commentId: string) {
    const { data }: { data: any } = await $axios.get(
      '/comments/' + commentId + '/'
    )
    return data
  },
  async editComment($axios: any, commentId: string, comment: any) {
    const response = await $axios.patch('/comments/' + commentId + '/', comment)
    return response
  },
  async deleteComment($axios: any, commentId: string) {
    const response = await $axios.delete('/comments/' + commentId + '/')
    return response
  },
}
