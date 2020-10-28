export default {
  async getQuestions($axios: any) {
    const { data }: { data: any } = await $axios.get('/questions')
    return data
  },
}
