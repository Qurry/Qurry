export default {
  async getQuestions($axios: any) {
    const { data }: { data: any } = await $axios.get('/questions')
    return data
  },
  async getQuestion($axios: any, id: string) {
    const { data }: { data: any } = await $axios.get('/questions/' + id)
    return data
  },
}
