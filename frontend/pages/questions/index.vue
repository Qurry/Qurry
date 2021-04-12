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
      <div v-if="$store.state.isLoadingQuestions">
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
                  :length="numOfpages"
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

@Component
export default class QuestionList extends Vue {
  questions: PreviewQuestion[] = []
  search: QuestionSearch = {
    limit: 10,
    page: 1,
    words: '',
    tagIds: [],
    orderBy: '-votes',
    answered: true,
  }

  created() {
    this.getQuestions()
  }

  get numOfpages() {
    return Math.ceil(this.$store.state.numOfQuestions / this.search.limit)
  }

  async getQuestions() {
    await this.$store.dispatch('getQuestions', this.search)
    this.questions = this.$store.state.questions
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
