<template>
  <div>
    <p>{{ answer.body }} by {{ answer.user.username }}</p>
    <hr />
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { CreateEditAnswer } from './../pages/questions/question.model'

@Component
export default class QuestionListCard extends Vue {
  @Prop()
  answer!: CreateEditAnswer[]
}
</script>
