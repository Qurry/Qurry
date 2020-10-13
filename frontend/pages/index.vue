<template>
  <v-row v-if="$fetchState.pending">
    <v-progress-circular
      :size="70"
      :width="7"
      color="primary"
      indeterminate
    ></v-progress-circular>
  </v-row>
  <v-row v-else-if="$fetchState.error">
    <p>Error while fetching questions: {{ $fetchState.error.message }}</p>
  </v-row>
  <v-row v-else>
    <v-col>
      <h1>Hello Qurry</h1>
      <div v-for="question in questions" :key="question.id">
        <h2>{{ question.title }}</h2>
        <p>{{ question.body }}</p>
      </div>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../services/QuestionService'

interface Question {
  id: number
  title: string
  body: string
}

@Component
export default class QuestioList extends Vue {
  questions: Question[] = []

  fetch() {
    return Promise.all([
      QuestionService.getQuestions()
        .then((questions) => {
          this.questions = questions
        })
        .catch((error) => console.log(error)),
    ])
  }
}
</script>
