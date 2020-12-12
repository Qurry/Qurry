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
    <p>Error while fetching question: {{ $fetchState.error.message }}</p>
  </v-row>
  <v-row v-else>
    <v-col>
      <h1 class="mb-3">{{ question.title }}</h1>
      <p>{{ question.body }}</p>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../../services/QuestionService'
import { PreviewQuestion } from './question.model'

@Component
export default class QuestionDetail extends Vue {
  question?: PreviewQuestion
  id = this.$route.params.id
  fetch() {
    return Promise.all([
      QuestionService.getQuestion(this.$axios, this.id)
        .then((question) => {
          this.question = question
        })
        .catch((error) => console.log(error)),
    ])
  }
}
</script>

<style scoped></style>
