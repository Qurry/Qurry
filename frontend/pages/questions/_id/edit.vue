<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="mb-5">Edit Question {{ questionId }}</h1>
        <QuestionForm
          :question="question"
          @submit="onSubmit"
          @cancel="onCancel"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../../../services/QuestionService'
import { CreateEditQuestion } from './../question.model'

@Component
export default class QuestionCreate extends Vue {
  questionId = this.$route.params.id

  question: CreateEditQuestion = {
    title: '',
    body: '',
    tagIds: [],
    images: [],
  }

  fetch() {
    return Promise.all([
      QuestionService.getQuestion(this.$axios, this.questionId)
        .then((question) => {
          this.question = question
        })
        .catch((error) => console.log(error)),
    ])
  }

  onSubmit() {
    QuestionService.editQuestion(this.$axios, this.questionId, this.question)
      .then((res) => {
        if (res.status === 200) {
          this.$router.push('/questions/' + res.data.questionId)
        } else {
          console.log(res)
        }
      })
      .catch((e) => console.log(e))
  }

  onCancel() {
    this.$router.push('/questions/' + this.questionId)
  }
}
</script>

<style scoped></style>
