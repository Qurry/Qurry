<template>
  <v-form v-model="isFormValid">
    <v-textarea
      v-model.trim="question.title"
      rows="1"
      label="Title"
      :rules="[rules.required, rules.minLength]"
      required
      outlined
    ></v-textarea>

    <v-textarea
      v-model.trim="question.body"
      rows="10"
      label="Description"
      :rules="[rules.required, rules.minLength]"
      required
      outlined
    ></v-textarea>

    <v-autocomplete
      v-model="question.tagIds"
      :items="tags"
      chips
      deletable-chips
      multiple
      item-text="name"
      item-value="id"
      label="Tags"
    >
      <template v-slot:selection="data">
        <v-chip
          close
          @click:close="removeTagIdFromQuestionTagIds(data.item.id)"
        >
          <template> {{ data.item.name }} </template>
        </v-chip>
      </template>
      <template v-slot:item="data">
        <template> {{ data.item.name }} </template>
      </template>
    </v-autocomplete>

    <v-btn color="secondary" :disabled="!isFormValid" @click="onSubmit">
      Submit
    </v-btn>
  </v-form>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { CreateEditQuestion } from './../pages/questions/question.model'
import { Tag } from './../pages/tags/tag.model'

@Component
export default class QuestionCreate extends Vue {
  isFormValid = false
  tags: Tag[] = this.$store.state.tags

  @Prop()
  question: CreateEditQuestion

  rules = {
    required: (value: string) => !!value || 'Required',
    minLength: (value: string) => value.length >= 3 || 'At least 3 characters',
  }

  removeTagIdFromQuestionTagIds(tagId: number) {
    const index = this.question.tagIds.indexOf(tagId)
    if (index >= 0) this.question.tagIds.splice(index, 1)
  }

  onSubmit() {
    this.$emit('submit')
  }
}
</script>

<style scoped></style>
