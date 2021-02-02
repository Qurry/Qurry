<template>
  <v-form v-model="isFormValid">
    <v-textarea
      v-model.trim="answer.body"
      rows="5"
      label="Body"
      :rules="[rules.required, rules.minLength]"
      auto-grow
      required
      outlined
      color="secondary"
    ></v-textarea>

    <h2>
      Body Preview
      <v-btn icon color="secondary" @click="showBodyPreview = !showBodyPreview">
        <v-icon>{{ showBodyPreview ? 'mdi-eye' : 'mdi-eye-off' }}</v-icon>
      </v-btn>
    </h2>

    <PostContentParser
      v-if="showBodyPreview"
      :content="answer.body"
      mode="body"
      :images="answer.images"
      class="body-preview"
    />

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
  showBodyPreview = true
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
::v-deep .v-textarea textarea {
  line-height: 1.3;
  padding: 5px 0 20px 0;
}
.body-preview {
  border: 3px solid #ddd;
  padding: 5px;
}
</style>
