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
    <div class="stats">
      <v-icon class="vote-icon"> mdi-arrow-up-bold </v-icon><br />
      <span>{{ question.votes }}</span> <br />
      <v-icon class="vote-icon"> mdi-arrow-down-bold </v-icon>
    </div>
    <div class="body">
      <h1 class="mb-3">{{ question.title }}</h1>
      <p>{{ question.body }}</p>

      <v-btn color="warning" :to="'/questions/' + id + '/edit'" small>
        <v-icon>mdi-pencil</v-icon> Edit
      </v-btn>

      <v-dialog v-model="dialog" persistent max-width="290">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="error" small v-bind="attrs" v-on="on">
            <v-icon>mdi-trash-can</v-icon> Delete
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
      <h2>
        {{ question.answers }} Answer{{ question.answers != 1 ? 's' : '' }}
      </h2>
    </div>
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
.stats {
  float: left;
  width: 60px;
}
.body {
  overflow: hidden;
}
.question-info {
  text-align: right;
  color: #888888;
  margin-bottom: 5px;
  margin-right: 10px;
}
.vote-icon {
  font-size: 40px;
}
</style>
