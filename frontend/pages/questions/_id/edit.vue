<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="mb-5">Edit Question {{ id }}</h1>
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
            label="Body"
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
            label="Select tags"
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
            Save Changes
          </v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../../../services/QuestionService'
import { CreateQuestion } from './../question.model'
import { Tag } from './../../tags/tag.model'

@Component
export default class QuestionCreate extends Vue {
  isFormValid = false
  tags: Tag[] = this.$store.state.tags

  id = this.$route.params.id

  fetch() {
    return Promise.all([
      QuestionService.getQuestion(this.$axios, this.id)
        .then((question) => {
          this.question = {
            title: question.title,
            body: question.body,
            tagIds: question.tagIds,
          }
        })
        .catch((error) => console.log(error)),
    ])
  }

  question: CreateQuestion = {
    title: '',
    body: '',
    tagIds: [],
  }

  rules = {
    required: (value: string) => !!value || 'Required.',
    minLength: (value: string) => value.length >= 3 || 'Min 3 Chars',
  }

  removeTagIdFromQuestionTagIds(tagId: number) {
    const index = this.question.tagIds.indexOf(tagId)
    if (index >= 0) this.question.tagIds.splice(index, 1)
  }

  onSubmit() {
    QuestionService.editQuestion(this.$axios, this.id, this.question)
      .then((_res) => {
        this.$router.push('/questions/' + this.id)
      })
      .catch((e) => console.log(e))
  }
}
</script>

<style scoped></style>
