<template>
  <div>
    <h2 class="mt-5">
      {{ answers.length }} Answer{{ answers.length != 1 ? 's' : '' }}
    </h2>
    <Answer
      v-for="answer in answers"
      :key="answer.id"
      :answer="answer"
      @delete="onDeleteAnswer"
      @update="$emit('update')"
    />
    <div v-if="inCreateMode">
      <h3>New Answer</h3>
      <AnswerForm
        :answer="createAnswer"
        class="my-2"
        @submit="onSubmitCreate"
        @cancel="onCancel"
      />
    </div>
    <div v-else>
      <v-btn color="secondary" class="mt-2" @click="onCreate">
        New Answer
      </v-btn>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { Answer, CreateEditAnswer } from '../pages/questions/question.model'
import QuestionService from './../services/QuestionService'

@Component
export default class AnswerContainer extends Vue {
  inCreateMode = false
  @Prop()
  answers!: Answer[]

  createAnswer: CreateEditAnswer = {
    body: '',
    images: [],
    documents: [],
  }

  onDeleteAnswer(answerId: string) {
    QuestionService.deleteAnswer(this.$axios, answerId)
      .then((res) => {
        if (res.status === 200) {
          this.$emit('update')
          this.$store.commit(
            'snackbar/setSnack',
            'Successfully deleted answer with id ' + res.data.answerId + '.'
          )
        } else {
          console.log(res)
        }
      })
      .catch((e) => console.log(e))
  }

  onCancel() {
    this.inCreateMode = false
  }

  onCreate() {
    this.inCreateMode = true
  }

  onSubmitCreate() {
    QuestionService.createAnswer(
      this.$axios,
      this.createAnswer,
      this.$route.path
    )
      .then((res) => {
        if (res.status === 201) {
          this.inCreateMode = false
          this.createAnswer.body = ''
          this.$emit('update')
        } else {
          console.log(res)
        }
      })
      .catch((e) => console.log(e))
  }
}
</script>

<style scoped></style>
