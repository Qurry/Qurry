<template>
  <v-form v-model="isFormValid">
    <PostBodyInput v-model="answer.body" />

    <ImageUpload :images="answer.images" />

    <v-btn color="secondary" :disabled="!isFormValid" @click="onSubmit">
      Submit
    </v-btn>
    <v-btn color="gray" @click="onCancel"> Cancel </v-btn>
  </v-form>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { CreateEditAnswer } from './../pages/questions/question.model'

@Component
export default class AnswerForm extends Vue {
  isFormValid = false

  @Prop()
  answer!: CreateEditAnswer

  onSubmit() {
    this.$emit('submit')
  }

  onCancel() {
    this.$emit('cancel')
  }
}
</script>

<style lang="scss" scoped></style>
