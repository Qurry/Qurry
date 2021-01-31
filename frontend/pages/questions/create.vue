<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="mb-5">New Question</h1>
        <QuestionForm
          :question="question"
          @submit="onSubmit"
          @cancel="onCancel"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../../services/QuestionService'
import { CreateEditQuestion } from './question.model'

@Component
export default class QuestionCreate extends Vue {
  question: CreateEditQuestion = {
    title: '',
    body: '',
    tagIds: [],
    images: [],
    documents: [],
  }

  onSubmit() {
    const imageIds = []

    for (const image of this.question.images) {
      imageIds.push(image.id)
    }

    // improve this
    const requestQuestion = {
      title: this.question.title,
      body: this.question.body,
      tagIds: this.question.tagIds,
      imageIds,
      documentIds: [],
    }

    QuestionService.createQuestion(this.$axios, requestQuestion)
      .then((res) => {
        if (res.status === 201) {
          this.$router.push('/questions/' + res.data.questionId)
        } else {
          console.log(res)
        }
      })
      .catch((e) => console.log(e))
  }

  onCancel() {
    this.$router.push('/questions')
  }
}
</script>

<style scoped></style>
