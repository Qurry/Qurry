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
        <VotingContainer
          :votes="question.votes"
          :user-vote="question.userVote"
          class="question-votes-container"
          @user-vote-change="changeUserVote"
        />
        <div class="question-body-container">
          <h1 class="mb-3"><MathJax :data="question.title" /></h1>
          <p><MathJax :data="question.body" /></p>

          <div class="question-footer">
            <v-btn
              color="secondary"
              :to="'/questions/' + question.id + '/edit'"
              small
              outlined
              class="mr-1"
            >
              Edit
            </v-btn>

            <v-dialog v-model="dialog" persistent max-width="290">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="secondary"
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
                  <v-btn color="error" @click="onDelete()"> Delete </v-btn>
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
import { DetailQuestion } from './../question.model'

@Component
export default class QuestionDetail extends Vue {
  dialog = false
  // improve this
  question: DetailQuestion = {
    id: '',
    title: '',
    body: '',
    votes: 0,
    userVote: 0,
    dateTime: '',
    user: {
      id: 0,
      username: '',
    },
    tagIds: [],
    answers: [],
  }

  fetch() {
    return Promise.all([
      QuestionService.getQuestion(this.$axios, this.$route.params.id)
        .then((question) => {
          this.question = question
        })
        .catch((error) => console.log(error)),
    ])
  }

  onDelete() {
    QuestionService.deleteQuestion(this.$axios, this.question.id)
      .then((res) => {
        if (res.status === 200) {
          this.$router.push('/questions')
        } else {
          console.log(res)
        }
      })
      .catch((error) => console.log(error))
  }

  changeUserVote(userVote: number) {
    QuestionService.voteQuestion(this.$axios, this.question.id, userVote)
      .then((_res) => {
        QuestionService.getQuestion(this.$axios, this.question.id)
          .then((question) => {
            this.question = question
          })
          .catch((error) => console.log(error))
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
