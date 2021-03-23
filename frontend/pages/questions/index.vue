<template>
  <v-row>
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
      <QuestionSearchForm
        class="mb-4"
        :search="search"
        @submit="onSubmitSearch"
      />
      <div v-if="isFetchingQuestions">
        <LoadingSpinner />
      </div>
      <div v-else>
        <div v-if="questions.length">
          <PreviewQuestionCard
            v-for="question in questions"
            :key="question.id"
            :question="question"
          />
          <v-row justify="center">
            <v-col>
              <v-container class="max-width">
                <v-pagination
                  v-model="search.page"
                  :length="search.limit"
                  :total-visible="7"
                  @input="onSubmitSearch"
                ></v-pagination>
              </v-container>
            </v-col>
          </v-row>
        </div>
        <div v-else>
          <p class="no-questions">No questions found.</p>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { PreviewQuestion, QuestionSearch } from './question.model'
import QuestionService from '~/services/QuestionService'

@Component
export default class QuestionList extends Vue {
  questions: PreviewQuestion[] = []
  isFetchingQuestions = false
  search: QuestionSearch = {
    limit: 10,
    page: 1,
    text: '',
    tagIds: [],
    sort: 'relevant',
    ascending: false,
    answered: false,
    user: '',
  }

  fetch() {
    return Promise.all([this.getQuestions()])
  }

  getQuestions() {
    this.isFetchingQuestions = true
    QuestionService.getQuestions(this.$axios, this.search)
      .then((questions) => {
        this.questions = questions
      })
      .catch((error) => console.log(error))
      .finally(() => (this.isFetchingQuestions = false))
  }

  onSubmitSearch() {
    this.getQuestions()
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
