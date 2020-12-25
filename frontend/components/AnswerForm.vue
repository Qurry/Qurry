<template>
  <v-form v-model="isFormValid">
    <v-textarea
      v-model.trim="answer.body"
      rows="1"
      label="Answer Body"
      :rules="[rules.required, rules.minLength]"
      auto-grow
      required
      outlined
      color="secondary"
    ></v-textarea>

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

  rules = {
    required: (value: string) => !!value || 'Required',
    minLength: (value: string) =>
      value.length >= 10 || 'At least 10 characters',
  }

  onSubmit() {
    this.$emit('submit')
  }

  onCancel() {
    this.$emit('cancel')
  }
}
</script>

<style lang="scss" scoped>
.post-info {
  font-style: italic;
}
.action-icon {
  cursor: pointer;
}
.toolbar {
  display: inline;
}
</style>
