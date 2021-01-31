import { NuxtAxiosInstance } from '@nuxtjs/axios'
import {
  CreateEditAnswer,
  CreateEditComment,
  CreateEditQuestion,
  DetailQuestion,
  PreviewQuestion,
  QuestionSearch,
} from '~/pages/questions/question.model'

export default {
  async getQuestions($axios: NuxtAxiosInstance, search: QuestionSearch) {
    const { data }: { data: PreviewQuestion[] } = await $axios.get(
      '/questions/?search=' + search.text
    )
    return data
  },
  async getQuestion($axios: NuxtAxiosInstance, questionId: string) {
    const { data }: { data: DetailQuestion } = await $axios.get(
      '/questions/' + questionId + '/'
    )
    return data
  },
  async createQuestion($axios: NuxtAxiosInstance, question: any) {
    const response = await $axios.post('/questions/', question)
    return response
  },
  async editQuestion(
    $axios: NuxtAxiosInstance,
    questionId: string,
    question: CreateEditQuestion
  ) {
    const response = await $axios.patch(
      '/questions/' + questionId + '/',
      question
    )
    return response
  },
  async deleteQuestion($axios: NuxtAxiosInstance, questionId: string) {
    const response = await $axios.delete('/questions/' + questionId + '/')
    return response
  },
  async votePost($axios: NuxtAxiosInstance, path: string, userVote: number) {
    const { data }: { data: { questionId: string } } = await $axios.get(
      path + '/?vote=' + userVote
    )
    return data
  },
  async createComment(
    $axios: NuxtAxiosInstance,
    comment: CreateEditComment,
    path: string
  ) {
    const response = await $axios.post(path + '/comments/', comment)
    return response
  },
  async editComment(
    $axios: NuxtAxiosInstance,
    commentId: string,
    comment: CreateEditComment
  ) {
    const response = await $axios.patch('/comments/' + commentId + '/', comment)
    return response
  },
  async deleteComment($axios: NuxtAxiosInstance, commentId: string) {
    const response = await $axios.delete('/comments/' + commentId + '/')
    return response
  },
  async createAnswer(
    $axios: NuxtAxiosInstance,
    answer: CreateEditAnswer,
    path: string
  ) {
    const response = await $axios.post(path + '/answers/', answer)
    return response
  },
  async editAnswer(
    $axios: NuxtAxiosInstance,
    answerId: string,
    answer: CreateEditAnswer
  ) {
    const response = await $axios.patch('/answers/' + answerId + '/', answer)
    return response
  },
  async deleteAnswer($axios: NuxtAxiosInstance, answerId: string) {
    const response = await $axios.delete('/answers/' + answerId + '/')
    return response
  },
}
