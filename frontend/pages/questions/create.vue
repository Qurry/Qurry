<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>New Question</h1>
        <v-form>
          <v-text-field
            v-model.trim="question.title"
            label="Title"
            required
          ></v-text-field>

          <v-textarea
            v-model.trim="question.body"
            rows="10"
            label="Body"
          ></v-textarea>

          <v-btn color="primary" @click="onSubmit">Ask Question</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../../services/QuestionService'
// import { PreviewQuestion } from './question.model'

@Component
export default class QuestionCreate extends Vue {
  // Q: Preview, Create, Detail Question or one Question?

  question = {
    title: '',
    body: '',
    tagIds: [],
  }

  onSubmit() {
    QuestionService.createQuestion(this.$axios, this.question)
      .then((res) => {
        console.log(res)
      })
      .catch((e) => console.log(e))
  }
}
</script>

<style scoped></style>
