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
      <div class="question-container">
        <div class="question-votes-container">
          <v-icon class="vote-icon"> mdi-arrow-up-bold </v-icon><br />
          <span>{{ question.votes }}</span> <br />
          <v-icon class="vote-icon"> mdi-arrow-down-bold </v-icon>
        </div>
        <div class="question-body-container">
          <h1 class="mb-3"><MathJax :data="question.title" /></h1>
          <p><MathJax :data="question.body" /></p>

          <div class="question-footer">
            <v-btn
              color="primary"
              :to="'/questions/' + id + '/edit'"
              small
              outlined
              class="mr-1"
            >
              Edit
            </v-btn>

            <v-dialog v-model="dialog" persistent max-width="290">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  small
                  v-bind="attrs"
                  outlined
                  class="mr-5"
                  v-on="on"
                >
                  Delete
                </v-btn>
              </template>
              <v-card>
                <v-card-title class="headline">
                  Do you really want to delete this question?
                </v-card-title>
                <v-card-text>This action can't be undone.</v-card-text>
                <v-card-actions>
                  <v-btn color="error" @click="onDelete(id)"> Delete </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn color="#ddd" @click="dialog = false"> Cancel </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>

            <p class="question-info">
              by {{ question.user.username }} on
              {{ question.dateTime | prettyDateTime }}
            </p>
          </div>
        </div>
      </div>
      <h2 class="mt-5">
        {{ question.answers.length }} Answer{{
          question.answers.length != 1 ? 's' : ''
        }}
      </h2>
      <div v-for="answer in question.answers" :key="answer.id">
        <p>{{ answer.body }} by {{ answer.user.username }}</p>
        <hr />
      </div>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../../../services/QuestionService'
import { PreviewQuestion } from './../question.model'

@Component
export default class QuestionDetail extends Vue {
  dialog = false
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

  onDelete(questionId: string) {
    QuestionService.deleteQuestion(this.$axios, questionId)
      .then((_res) => {
        this.$router.push('/questions')
      })
      .catch((error) => console.log(error))
  }
}
</script>

<style scoped>
.question-info {
  color: #888888;
  margin-bottom: 5px;
  margin-left: auto;
}
.vote-icon {
  font-size: 40px;
}
.question-container {
  display: flex;
}
.question-votes-container {
  width: 50px;
}
.question-body-container {
  flex: 1;
}
.question-footer {
  display: flex;
}
</style>
