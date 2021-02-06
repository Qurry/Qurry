<template>
  <v-form v-model="isFormValid">
    <v-textarea
      v-model.trim="question.title"
      rows="1"
      label="Title"
      :rules="[rules.required, rules.minLength]"
      required
      outlined
      auto-grow
      color="secondary"
    ></v-textarea>

    <PostBodyInput v-model="question.body" />

    <h2 class="mt-3">Tags</h2>
    <TagSelection
      v-if="loaded || inCreateMode"
      :selected-tag-ids="question.tagIds"
      @update-selected-tag-ids="updateSelectedTagIds"
    />

    <ImageUpload :images="question.images" />

    <v-btn
      color="secondary"
      :disabled="!isFormValid"
      class="mr-2"
      @click="onSubmit"
    >
      Submit
    </v-btn>
    <v-btn color="gray" @click="onCancel"> Cancel </v-btn>
  </v-form>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'
import { CreateEditQuestion } from './../pages/questions/question.model'

@Component
export default class QuestionForm extends Vue {
  isFormValid = false
  loaded = false

  @Prop()
  question!: CreateEditQuestion

  @Prop()
  inCreateMode!: boolean

  @Watch('question')
  onChildChanged() {
    this.loaded = true
  }

  rules = {
    required: (value: string) => !!value || 'Required',
    minLength: (value: string) => value.length >= 3 || 'At least 3 characters',
  }

  updateSelectedTagIds(selectedTagIds: string[]) {
    this.question.tagIds = selectedTagIds
  }

  onSubmit() {
    this.$emit('submit')
  }

  onCancel() {
    this.$emit('cancel')
  }
}
</script>

<style scoped>
::v-deep .v-textarea textarea {
  line-height: 1.3;
  padding: 5px 0 20px 0;
}
</style>
