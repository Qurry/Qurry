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
      <h1 class="mb-3">Alle Fragen</h1>
      <!-- <QuestionListCard
        v-for="question in questions"
        :key="question.id"
        :question="question"
      /> -->
      {{ questions }}
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../../services/QuestionService'
import { PreviewQuestion } from './question.model'

@Component
export default class QuestionList extends Vue {
  questions: PreviewQuestion[] = []

  fetch() {
    return Promise.all([
      QuestionService.getQuestions(this.$axios)
        .then((questions) => {
          this.questions = questions
        })
        .catch((error) => console.log(error)),
    ])
  }
}
</script>

<style scoped></style>
