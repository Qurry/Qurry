<template>
  <div>
    <v-form @submit.prevent="onSubmit">
      <v-text-field
        v-model.trim="search.text"
        label="Search"
        append-icon="mdi-magnify"
        outlined
        color="secondary"
      ></v-text-field>

      <TagSelection
        :selected-tag-ids="search.tagIds"
        @update-selected-tag-ids="updateSelectedTagIds"
      />

      <v-btn color="secondary" class="mr-2" type="submit"> Search </v-btn>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { QuestionSearch } from './../pages/questions/question.model'

@Component
export default class QuestionSearchForm extends Vue {
  search: QuestionSearch = {
    text: '',
    tagIds: [],
  }

  updateSelectedTagIds(selectedTagIds: string[]) {
    this.search.tagIds = selectedTagIds
  }

  onSubmit() {
    this.$emit('submit', this.search)
  }
}
</script>

<style scoped></style>
