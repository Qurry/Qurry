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
      <div class="question-header">
        <h1>Questions</h1>
        <v-btn
          to="/questions/create"
          color="secondary"
          class="new-question-btn"
        >
          New Question
        </v-btn>
      </div>
      <QuestionSearchForm class="mb-4" @submit="onSubmitSearch" />
      <div v-if="questions.length">
        <PreviewQuestionCard
          v-for="question in questions"
          :key="question.id"
          :question="question"
        />
      </div>
      <div v-else>
        <p class="no-questions">No questions found.</p>
      </div>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../../services/QuestionService'
import { PreviewQuestion, QuestionSearch } from './question.model'

@Component
export default class QuestionList extends Vue {
  questions: PreviewQuestion[] = []

  sortQuestions() {
    this.questions.sort((a: PreviewQuestion, b: PreviewQuestion) =>
      a.votes! < b.votes! ? 1 : b.votes! < a.votes! ? -1 : 0
    )
  }

  fetch() {
    return Promise.all([this.getQuestions()])
  }

  getQuestions(search: QuestionSearch = { text: '', tagIds: [] }) {
    QuestionService.getQuestions(this.$axios, search)
      .then((questions) => {
        this.questions = questions
        this.sortQuestions()
      })
      .catch((error) => console.log(error))
  }

  onSubmitSearch(search: QuestionSearch) {
    this.getQuestions(search)
  }
}
</script>

<style scoped>
.question-header {
  display: flex;
  margin-bottom: 10px;
}
.new-question-btn {
  margin-left: auto;
  margin-top: 7px;
}
p.no-questions {
  text-align: center;
}
</style>
