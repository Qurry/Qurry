<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="mb-5">New Question</h1>
        <QuestionForm :question="question" @submit="onSubmit" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../../services/QuestionService'
import { CreateEditQuestion } from './question.model'

@Component
export default class QuestionCreate extends Vue {
  question: CreateEditQuestion = {
    title: '',
    body: '',
    tagIds: [],
  }

  onSubmit() {
    QuestionService.createQuestion(this.$axios, this.question)
      .then((res) => {
        if (res.status === 201) {
          this.$router.push('/questions/' + res.data.questionId)
        } else {
          console.log(res)
        }
      })
      .catch((e) => console.log(e))
  }
}
</script>

<style scoped></style>
